/**
 * @file safe_shell.cpp
 * @brief SafeShellInterpreter 类的实现文件
 *
 * 包含了脚本解析、变量替换、命令执行等所有核心逻辑。
 * 注意：编译此文件需要 C++14 标准，并链接文件系统库 (g++ 使用 -lstdc++fs)。
 */
#include "safe_shell.h"
#include "json.hpp" // nlohmann::json 第三方库，用于处理 JSON

#include <iostream>
#include <sstream>      // 用于字符串流处理
#include <fstream>      // 用于文件读写
#include <cstdlib>      // for getenv, system
#include <algorithm>    // for std::all_of
#include <regex>        // for std::regex, 用于变量替换
#include <iomanip>      // for std::setw, 用于格式化 JSON 输出

// POSIX 标准头文件，用于文件权限、所有者等操作
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <pwd.h>
#include <grp.h>

// 严格使用 C++14 兼容的文件系统库 (Technical Specification version)
#include <experimental/filesystem>
namespace fs = std::experimental::filesystem;

// 使用 nlohmann::json 库的别名
using json = nlohmann::json;

// detail 命名空间用于存放不希望暴露给外部的实现细节
namespace detail {
    // 内部数据结构，用于表示一个解析后的命令
    struct Command {
        int line_num;                   // 命令所在的原始行号，便于报错
        std::string name;               // 命令名称, e.g., "rm", "mkdir"
        std::vector<std::string> args;  // 命令的所有参数列表
    };
}

// 静态成员初始化
const std::string SafeShellInterpreter::SHEBANG = "#!safe_shell";

SafeShellInterpreter::SafeShellInterpreter() {
    // 在构造函数中初始化命令分发器
    // 使用 lambda 表达式将成员函数绑定到 map，代码简洁且类型安全
    command_handlers_["rm"]      = [this](const auto& cmd, auto& err) { return this->handle_rm(cmd, err); };
    command_handlers_["mkdir"]   = [this](const auto& cmd, auto& err) { return this->handle_mkdir(cmd, err); };
    command_handlers_["pkill"]   = [this](const auto& cmd, auto& err) { return this->handle_pkill(cmd, err); };
    command_handlers_["json"]    = [this](const auto& cmd, auto& err) { return this->handle_json(cmd, err); };
    command_handlers_["cfgmgr"]  = [this](const auto& cmd, auto& err) { return this->handle_cfgmgr(cmd, err); };
    command_handlers_["reboot"]  = [this](const auto& cmd, auto& err) { return this->handle_reboot(cmd, err); };
    command_handlers_["partctr"] = [this](const auto& cmd, auto& err) { return this->handle_partctr(cmd, err); };
}

SafeShellInterpreter::~SafeShellInterpreter() = default;

// ------------------- 公共入口函数 -------------------

bool SafeShellInterpreter::execute(const std::string& script_content, std::string& error_message) {
    // 每次执行都是一个全新的环境，清空之前的变量
    variables_.clear();

    // --- 阶段一：解析 ---
    // 声明一个用于接收解析结果的命令向量
    std::vector<detail::Command> commands;
    // 调用解析函数，如果失败，则直接返回 false
    if (!parse_script(script_content, commands, error_message)) {
        return false;
    }

    // --- 阶段二：执行 ---
    // 只有在完全解析成功后，才开始执行命令
    return execute_commands(commands, error_message);
}

// ------------------- 解析阶段实现 (C++14 兼容) -------------------

bool SafeShellInterpreter::parse_script(const std::string& script_content, std::vector<detail::Command>& out_commands, std::string& error_message) {
    // 使用字符串流逐行读取脚本内容
    std::stringstream ss(script_content);
    std::string line;
    int line_num = 0;
    std::vector<detail::Command> parsed_commands;

    // 1. 校验脚本的第一行是否是正确的 Shebang
    if (std::getline(ss, line)) {
        line_num++;
        if (line != SHEBANG) {
            error_message = "Error at line 1: Missing or incorrect shebang. Expected '" + SHEBANG + "'.";
            return false;
        }
    } else {
        error_message = "Error: Script is empty.";
        return false;
    }

    // 2. 逐行解析脚本的剩余部分
    while (std::getline(ss, line)) {
        line_num++;
        
       // 忽略空行和注释行（以'#'开头）
        if (line.empty() || line[0] == '#') {
            continue;
        }
        
        // 核心规则：检查行首字符，如果以空格或制表符开头，则忽略该行
        if (line[0] == ' ' || line[0] == '\t') {
            continue;
        }

        // 移除行尾可能存在的空白字符（如\r），避免影响解析
        line.erase(std::find_if(line.rbegin(), line.rend(), [](unsigned char ch) {
            return !std::isspace(ch);
        }).base(), line.end());

        // 解析当前行
        std::unique_ptr<detail::Command> cmd_ptr;
        if (!parse_line(line, line_num, cmd_ptr, error_message)) {
            // 如果 parse_line 返回 false，说明有语法错误，立即停止整个解析过程
            return false;
        }

        // 如果 cmd_ptr 不为空，说明成功解析出一个命令，将其添加到列表中
        if (cmd_ptr) {
            // 使用 std::move 高效转移 Command 对象的所有权
            parsed_commands.push_back(std::move(*cmd_ptr));
        }
    }

    // 将解析出的所有命令通过输出参数返回
    out_commands = std::move(parsed_commands);
    return true;
}

bool SafeShellInterpreter::parse_line(const std::string& line, int line_num, std::unique_ptr<detail::Command>& out_cmd, std::string& error_message) {
    // 默认不生成命令对象
    out_cmd = nullptr; 

    // 检查是否是变量赋值 (e.g., "VAR=value")
    // 条件：'=' 存在，不在行首，且'='前后没有空格
    size_t equals_pos = line.find('=');
    if (equals_pos != std::string::npos && equals_pos > 0 && line.find(' ', 0, equals_pos) == std::string::npos) {
        std::string var_name = line.substr(0, equals_pos);
        std::string var_value = line.substr(equals_pos + 1);
        
        // 对变量名进行简单校验，只允许字母、数字和下划线
        if (std::all_of(var_name.begin(), var_name.end(), [](char c){ return std::isalnum(c) || c == '_'; })) {
            variables_[var_name] = var_value; // 存入变量 map
            return true; // 变量赋值是合法操作，但不是命令，所以 out_cmd 保持为空
        }
    }
    
    // 如果不是变量赋值，则解析为命令
    std::stringstream line_ss(line);
    auto cmd = std::make_unique<detail::Command>(); // 创建一个命令对象
    cmd->line_num = line_num;

    // 第一个单词是命令名称
    if (!(line_ss >> cmd->name)) {
        return true; // 可能是只有空格的行，虽然前面已过滤，但这里做个保险
    }

    // 后续的单词都是参数
    std::string token;
    while (line_ss >> token) {
        cmd->args.push_back(token);
    }
    
    // 在解析阶段就完成变量替换
    if (!substitute_variables(cmd->args, line_num, error_message)) {
        return false; // 如果变量不存在，则解析失败
    }
    
    // 将成功创建的命令对象通过 out_cmd 返回
    out_cmd = std::move(cmd);
    return true;
}

bool SafeShellInterpreter::substitute_variables(std::vector<std::string>& args, int line_num, std::string& error_message) {
    // 正则表达式匹配 ${VAR} 格式
    std::regex var_regex("\\$\\{([^}]+)\\}");
    
    // 遍历所有参数
    for (auto& arg : args) {
        std::string temp_arg = arg;
        std::string result_arg;
        auto search_start = temp_arg.cbegin();
        std::smatch match;

        // 循环查找一个参数中所有匹配的变量
        while (std::regex_search(search_start, temp_arg.cend(), match, var_regex)) {
            // 添加变量前的部分
            result_arg += match.prefix().str();
            // 提取变量名
            std::string var_name = match[1].str();
            
            // 优先从自定义变量中查找
            auto it = variables_.find(var_name);
            if (it != variables_.end()) {
                result_arg += it->second;
            } else {
                // 如果自定义变量中没有，则从系统环境变量中查找
                const char* env_val = std::getenv(var_name.c_str());
                if (env_val) {
                    result_arg += env_val;
                } else {
                    // 如果都找不到，则报错
                    error_message = "Error at line " + std::to_string(line_num) + ": Variable '" + var_name + "' not found.";
                    return false;
                }
            }
            // 更新下一次搜索的起始位置
            search_start = match.suffix().first;
        }
        // 添加最后一个变量之后的部分
        result_arg += std::string(search_start, temp_arg.cend());
        // 更新原始参数
        arg = result_arg;
    }
    return true;
}

// ------------------- 执行阶段实现 -------------------

bool SafeShellInterpreter::execute_commands(const std::vector<detail::Command>& commands, std::string& error_message) {
    // 遍历所有已解析的命令并执行
    for (const auto& cmd : commands) {
        // 从命令分发器中查找命令对应的处理函数
        auto it = command_handlers_.find(cmd.name);
        if (it == command_handlers_.end()) {
            // 如果找不到，说明是不支持的命令
            error_message = "Error at line " + std::to_string(cmd.line_num) + ": Unknown command '" + cmd.name + "'.";
            return false;
        }

        // 调用找到的处理函数
        if (!it->second(cmd, error_message)) {
            // 如果处理函数返回 false，说明执行失败，立即停止
            error_message = "Error at line " + std::to_string(cmd.line_num) + ": " + error_message;
            return false;
        }
    }
    // 所有命令都成功执行
    return true;
}

// ------------------- 命令处理器实现 -------------------

bool SafeShellInterpreter::handle_rm(const detail::Command& cmd, std::string& error) {
    // 1. 参数校验
    if (cmd.args.size() != 1) {
        error = "rm command expects 1 argument (path), but got " + std::to_string(cmd.args.size()) + ".";
        return false;
    }
    // 2. 执行操作
    const std::string& path = cmd.args[0];
    std::error_code ec;
    fs::remove_all(path, ec); // remove_all 可以删除文件或递归删除目录
    if (ec) {
        error = "Failed to remove '" + path + "': " + ec.message();
        return false;
    }
    // 3. 打印执行信息（用于演示）
    std::cout << "Executed: rm " << path << std::endl;
    return true;
}

bool SafeShellInterpreter::handle_mkdir(const detail::Command& cmd, std::string& error) {
    // 1. 参数校验
    if (cmd.args.size() != 3) {
        error = "mkdir command expects 3 arguments (path, owner:group, permissions), but got " + std::to_string(cmd.args.size()) + ".";
        return false;
    }
    
    // 2. 提取参数
    const std::string& path = cmd.args[0];
    const std::string& owner_group = cmd.args[1];
    const std::string& perms_str = cmd.args[2];

    // 3. 执行操作
    // 3.1 创建目录 (create_directories 可以递归创建父目录)
    std::error_code ec;
    fs::create_directories(path, ec);
    if (ec) {
        error = "Failed to create directory '" + path + "': " + ec.message();
        return false;
    }
    
    // 3.2 设置权限
    try {
        mode_t perms = std::stoi(perms_str, nullptr, 8); // 权限是8进制数
        if (chmod(path.c_str(), perms) != 0) {
            error = "Failed to set permissions for '" + path + "'.";
            return false;
        }
    } catch (const std::exception& e) {
        error = "Invalid permissions format: " + perms_str;
        return false;
    }

    // 3.3 设置所有者和组
    size_t colon_pos = owner_group.find(':');
    if (colon_pos == std::string::npos) {
        error = "Invalid owner:group format. Expected 'user:group'.";
        return false;
    }
    std::string owner_name = owner_group.substr(0, colon_pos);
    std::string group_name = owner_group.substr(colon_pos + 1);

    struct passwd* pw = getpwnam(owner_name.c_str());
    if (pw == nullptr) {
        error = "User '" + owner_name + "' not found.";
        return false;
    }
    struct group* gr = getgrnam(group_name.c_str());
    if (gr == nullptr) {
        error = "Group '" + group_name + "' not found.";
        return false;
    }
    if (chown(path.c_str(), pw->pw_uid, gr->gr_gid) != 0) {
        error = "Failed to set owner for '" + path + "'. Check permissions.";
        return false;
    }

    // 4. 打印执行信息
    std::cout << "Executed: mkdir " << path << " " << owner_group << " " << perms_str << std::endl;
    return true;
}

bool SafeShellInterpreter::handle_pkill(const detail::Command& cmd, std::string& error) {
    // 1. 参数校验
    if (cmd.args.size() != 2) {
        error = "pkill command expects 2 arguments (process_name, signal), but got " + std::to_string(cmd.args.size()) + ".";
        return false;
    }
    
    // 2. 参数清理 (非常重要，防止命令注入)
    std::string process_name = cmd.args[0];
    std::string signal = cmd.args[1];
    if (process_name.find_first_not_of("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_") != std::string::npos ||
        signal.find_first_not_of("ABCDEFGHIJKLMNOPQRSTUVWXYZ") != std::string::npos) {
        error = "Invalid characters in pkill arguments. Only alphanumeric characters are allowed.";
        return false;
    }

    // 3. 执行操作
    // 警告：直接调用 system() 存在安全风险。在生产环境中应使用更安全的 exec 系列函数或直接调用 kill() API。
    // 这里为了简化演示而使用 system()。
    std::string command_str = "pkill -" + signal + " " + process_name;
    int ret = system(command_str.c_str());
    
    // pkill 在找不到进程时也会返回非0，这通常不应视为致命错误。
    if (ret != 0) {
        std::cout << "Executed: " << command_str << " (process may not have been running or another issue occurred)" << std::endl;
    } else {
        std::cout << "Executed: " << command_str << std::endl;
    }

    return true;
}

bool SafeShellInterpreter::handle_json(const detail::Command& cmd, std::string& error) {
    // 1. 参数校验
    if (cmd.args.size() != 4 || cmd.args[1] != "set") {
        error = "json command format is 'json <file> set <key> <value>', but got invalid format.";
        return false;
    }

    // 2. 提取参数
    const std::string& file_path = cmd.args[0];
    const std::string& key = cmd.args[2];
    const std::string& value_str = cmd.args[3];

    try {
        // 3.1 读取和解析 JSON 文件
        std::ifstream f(file_path);
        if (!f.is_open()) {
            error = "Cannot open JSON file: " + file_path;
            return false;
        }
        json data = json::parse(f);
        f.close();

        // 3.2 修改字段值
        // 使用 json_pointer 支持用 "." 分隔的路径，如 "a.b.c"
        json::json_pointer ptr("/" + std::regex_replace(key, std::regex("\\."), "/"));
        
        // 尝试自动转换值的类型（数字,布尔,字符串）
        try {
            if (value_str.find('.') != std::string::npos) data[ptr] = std::stod(value_str); // 浮点数
            else data[ptr] = std::stoll(value_str); // 整数
        } catch (const std::invalid_argument&) {
            if (value_str == "true") data[ptr] = true;
            else if (value_str == "false") data[ptr] = false;
            else data[ptr] = value_str; // 保持为字符串
        }

        // 3.3 写回文件 (使用 std::setw(4) 进行格式化美观输出)
        std::ofstream o(file_path);
        o << std::setw(4) << data << std::endl;

    } catch (json::parse_error& e) {
        error = "JSON parse error in '" + file_path + "': " + e.what();
        return false;
    } catch (json::exception& e) { // 捕获 nlohmann::json 的其他异常，如 key 不存在
        error = "JSON operation error: " + std::string(e.what());
        return false;
    } catch (...) {
        error = "An unknown error occurred during JSON operation.";
        return false;
    }

    std::cout << "Executed: json " << file_path << " set " << key << " " << value_str << std::endl;
    return true;
}

// ------------------- 模拟/占位处理器 -------------------
// 在实际系统中，这些函数将调用相应的系统 API 或命令

bool SafeShellInterpreter::handle_cfgmgr(const detail::Command& cmd, std::string& error) {
    if (cmd.args.size() < 2) {
        error = "cfgmgr requires at least 2 arguments.";
        return false;
    }
    // 模拟执行
    std::cout << "Executed: cfgmgr";
    for(const auto& arg : cmd.args) std::cout << " " << arg;
    std::cout << std::endl;
    return true;
}

bool SafeShellInterpreter::handle_reboot(const detail::Command& cmd, std::string& error) {
    if (!cmd.args.empty()) {
        error = "reboot command expects 0 arguments.";
        return false;
    }
    // 模拟执行
    std::cout << "Executed: reboot" << std::endl;
    // 在真实系统中: system("reboot");
    return true;
}

bool SafeShellInterpreter::handle_partctr(const detail::Command& cmd, std::string& error) {
    if (cmd.args.size() != 2) {
        error = "partctr command expects 2 arguments.";
        return false;
    }
    // 模拟执行
    std::cout << "Executed: partctr " << cmd.args[0] << " " << cmd.args[1] << std::endl;
    return true;
}