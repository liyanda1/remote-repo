#include "safe_shell.h"
#include "json.hpp" // nlohmann::json

#include <iostream>
#include <sstream>
#include <fstream>
#include <cstdlib> // for getenv, system
#include <algorithm>
#include <regex>

// POSIX headers for mkdir, chmod, chown
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <pwd.h>
#include <grp.h>

// For C++17 filesystem. If not available, we use POSIX functions.
#if __has_include(<filesystem>)
#include <filesystem>
namespace fs = std::filesystem;
#else
#include <experimental/filesystem>
namespace fs = std::experimental::filesystem;
#endif

// 使用 nlohmann::json
using json = nlohmann::json;

namespace detail {
    // 内部数据结构，用于表示一个解析后的命令
    struct Command {
        int line_num;
        std::string name;
        std::vector<std::string> args;
    };
}

// ------------------- 静态成员和构造/析构函数 -------------------

const std::string SafeShellInterpreter::SHEBANG = "#!safe_shell";

SafeShellInterpreter::SafeShellInterpreter() {
    // 初始化命令分发器，将命令字符串映射到处理函数
    // 使用 lambda 和 std::bind 将成员函数绑定到 map 中
    command_handlers_["rm"] = [this](const auto& cmd, auto& err) { return this->handle_rm(cmd, err); };
    command_handlers_["mkdir"] = [this](const auto& cmd, auto& err) { return this->handle_mkdir(cmd, err); };
    command_handlers_["pkill"] = [this](const auto& cmd, auto& err) { return this->handle_pkill(cmd, err); };
    command_handlers_["json"] = [this](const auto& cmd, auto& err) { return this->handle_json(cmd, err); };
    command_handlers_["cfgmgr"] = [this](const auto& cmd, auto& err) { return this->handle_cfgmgr(cmd, err); };
    command_handlers_["reboot"] = [this](const auto& cmd, auto& err) { return this->handle_reboot(cmd, err); };
    command_handlers_["partctr"] = [this](const auto& cmd, auto& err) { return this->handle_partctr(cmd, err); };
}

SafeShellInterpreter::~SafeShellInterpreter() = default;

// ------------------- 公共入口函数 -------------------

bool SafeShellInterpreter::execute(const std::string& script_content, std::string& error_message) {
    variables_.clear(); // 每次执行前清空变量

    // 1. 解析阶段
    auto commands_opt = parse_script(script_content, error_message);
    if (!commands_opt) {
        // 解析失败，错误信息已在 parse_script 中设置
        return false;
    }

    // 2. 执行阶段
    return execute_commands(*commands_opt, error_message);
}

// ------------------- 解析阶段实现 -------------------

std::optional<std::vector<detail::Command>> SafeShellInterpreter::parse_script(const std::string& script_content, std::string& error_message) {
    std::stringstream ss(script_content);
    std::string line;
    int line_num = 0;
    std::vector<detail::Command> commands;

    // 1. 校验 Shebang
    if (std::getline(ss, line)) {
        line_num++;
        if (line.find(SHEBANG) != 0) {
            error_message = "Error at line 1: Missing or incorrect shebang. Expected '" + SHEBANG + "'.";
            return std::nullopt;
        }
    } else {
        error_message = "Error: Script is empty.";
        return std::nullopt;
    }

    // 2. 逐行解析
    while (std::getline(ss, line)) {
        line_num++;

        // 移除行首尾空格
        line.erase(0, line.find_first_not_of(" \t\n\r"));
        line.erase(line.find_last_not_of(" \t\n\r") + 1);

        if (line.empty() || line[0] == '#') {
            continue; // 忽略空行和注释
        }

        // 按照要求，命令前不能有空格
        if (line.find_first_of(" \t") == 0) {
             // 暂不执行，可以选择警告或忽略
            continue;
        }

        auto cmd_opt = parse_line(line, line_num, error_message);
        if (error_message.empty() && cmd_opt.has_value()) {
            commands.push_back(cmd_opt.value());
        } else if (!error_message.empty()) {
            // 解析失败
            return std::nullopt;
        }
        // 如果是变量赋值或空行，cmd_opt 为空，继续下一行
    }

    return commands;
}

std::optional<detail::Command> SafeShellInterpreter::parse_line(const std::string& line, int line_num, std::string& error_message) {
    // 检查是否是变量赋值
    size_t equals_pos = line.find('=');
    if (equals_pos != std::string::npos && equals_pos > 0 && line[equals_pos - 1] != ' ' && line[equals_pos + 1] != ' ') {
        std::string var_name = line.substr(0, equals_pos);
        std::string var_value = line.substr(equals_pos + 1);
        // 简单校验变量名
        if (std::all_of(var_name.begin(), var_name.end(), [](char c){ return std::isalnum(c) || c == '_'; })) {
            variables_[var_name] = var_value;
            return std::nullopt; // 变量赋值不是一个命令
        }
    }
    
    // 解析为命令
    std::stringstream line_ss(line);
    std::string token;
    detail::Command cmd;
    cmd.line_num = line_num;

    if (!(line_ss >> cmd.name)) {
        return std::nullopt; // 空行或只有空格的行
    }

    while (line_ss >> token) {
        cmd.args.push_back(token);
    }
    
    // 替换变量
    if (!substitute_variables(cmd.args, line_num, error_message)) {
        return std::nullopt;
    }

    return cmd;
}

bool SafeShellInterpreter::substitute_variables(std::vector<std::string>& args, int line_num, std::string& error_message) {
    std::regex var_regex("\\$\\{([^}]+)\\}");
    for (auto& arg : args) {
        std::smatch match;
        std::string temp_arg = arg;
        std::string result_arg;
        
        auto search_start = temp_arg.cbegin();
        while (std::regex_search(search_start, temp_arg.cend(), match, var_regex)) {
            result_arg += match.prefix();
            std::string var_name = match[1].str();
            
            // 优先从自定义变量中查找
            auto it = variables_.find(var_name);
            if (it != variables_.end()) {
                result_arg += it->second;
            } else {
                // 否则从环境变量中查找
                const char* env_val = std::getenv(var_name.c_str());
                if (env_val) {
                    result_arg += env_val;
                } else {
                    error_message = "Error at line " + std::to_string(line_num) + ": Variable '" + var_name + "' not found.";
                    return false;
                }
            }
            search_start = match.suffix().first;
        }
        result_arg += std::string(search_start, temp_arg.cend());
        arg = result_arg;
    }
    return true;
}


// ------------------- 执行阶段实现 -------------------

bool SafeShellInterpreter::execute_commands(const std::vector<detail::Command>& commands, std::string& error_message) {
    for (const auto& cmd : commands) {
        auto it = command_handlers_.find(cmd.name);
        if (it == command_handlers_.end()) {
            error_message = "Error at line " + std::to_string(cmd.line_num) + ": Unknown command '" + cmd.name + "'.";
            return false;
        }
        // 执行对应的命令处理器
        if (!it->second(cmd, error_message)) {
            // 附加行号信息
            error_message = "Error at line " + std::to_string(cmd.line_num) + ": " + error_message;
            return false;
        }
    }
    return true;
}

// ------------------- 命令处理器实现 -------------------

bool SafeShellInterpreter::handle_rm(const detail::Command& cmd, std::string& error) {
    if (cmd.args.size() != 1) {
        error = "rm command expects 1 argument (path), but got " + std::to_string(cmd.args.size()) + ".";
        return false;
    }
    const std::string& path = cmd.args[0];
    std::error_code ec;
    fs::remove_all(path, ec);
    if (ec) {
        error = "Failed to remove '" + path + "': " + ec.message();
        return false;
    }
    std::cout << "Executed: rm " << path << std::endl;
    return true;
}

bool SafeShellInterpreter::handle_mkdir(const detail::Command& cmd, std::string& error) {
    if (cmd.args.size() != 3) {
        error = "mkdir command expects 3 arguments (path, owner:group, permissions), but got " + std::to_string(cmd.args.size()) + ".";
        return false;
    }
    const std::string& path = cmd.args[0];
    const std::string& owner_group = cmd.args[1];
    const std::string& perms_str = cmd.args[2];

    // 1. 创建目录
    std::error_code ec;
    fs::create_directories(path, ec);
    if (ec) {
        error = "Failed to create directory '" + path + "': " + ec.message();
        return false;
    }
    
    // 2. 解析并设置权限
    try {
        mode_t perms = std::stoi(perms_str, nullptr, 8); // 8进制
        if (chmod(path.c_str(), perms) != 0) {
            error = "Failed to set permissions for '" + path + "'.";
            return false;
        }
    } catch (const std::exception& e) {
        error = "Invalid permissions format: " + perms_str;
        return false;
    }

    // 3. 解析并设置所有者
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

    std::cout << "Executed: mkdir " << path << " " << owner_group << " " << perms_str << std::endl;
    return true;
}

bool SafeShellInterpreter::handle_pkill(const detail::Command& cmd, std::string& error) {
    if (cmd.args.size() != 2) {
        error = "pkill command expects 2 arguments (process_name, signal), but got " + std::to_string(cmd.args.size()) + ".";
        return false;
    }
    // 注意：直接调用 system 是不安全的。在生产环境中，应该使用更安全的方式，
    // 例如解析信号并使用 kill() API。这里为了演示而简化。
    // 同时需要对参数进行严格的清理，防止命令注入。
    std::string process_name = cmd.args[0];
    std::string signal = cmd.args[1];
    
    // 基本的清理：只允许字母、数字和下划线
    if (process_name.find_first_not_of("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_") != std::string::npos ||
        signal.find_first_not_of("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") != std::string::npos) {
        error = "Invalid characters in pkill arguments.";
        return false;
    }

    std::string command_str = "pkill -" + signal + " " + process_name;
    int ret = system(command_str.c_str());
    if (ret != 0) {
        // pkill 在找不到进程时也会返回非0，这不一定是错误
        std::cout << "Executed: " << command_str << " (process may not have been running)" << std::endl;
    } else {
        std::cout << "Executed: " << command_str << std::endl;
    }

    return true;
}

bool SafeShellInterpreter::handle_json(const detail::Command& cmd, std::string& error) {
    if (cmd.args.size() != 4 || cmd.args[1] != "set") {
        error = "json command format is 'json <file> set <key> <value>', but got invalid format.";
        return false;
    }
    const std::string& file_path = cmd.args[0];
    const std::string& key = cmd.args[2];
    const std::string& value_str = cmd.args[3];

    try {
        // 1. 读取和解析 JSON 文件
        std::ifstream f(file_path);
        if (!f.is_open()) {
            error = "Cannot open JSON file: " + file_path;
            return false;
        }
        json data = json::parse(f);
        f.close();

        // 2. 修改字段值 (支持简单的 a.b.c 形式的 key)
        json::json_pointer ptr("/" + std::regex_replace(key, std::regex("\\."), "/"));
        data[ptr] = value_str; // nlohmann/json 会自动处理类型

    	// 尝试将字符串转换为数字或布尔值
        try {
            if (value_str.find('.') != std::string::npos) {
                data[ptr] = std::stod(value_str);
            } else {
                data[ptr] = std::stoll(value_str);
            }
        } catch (const std::invalid_argument&) {
            if (value_str == "true") data[ptr] = true;
            else if (value_str == "false") data[ptr] = false;
            else data[ptr] = value_str; // 保持为字符串
        }

        // 3. 写回文件
        std::ofstream o(file_path);
        o << std::setw(4) << data << std::endl;

    } catch (json::parse_error& e) {
        error = "JSON parse error in '" + file_path + "': " + e.what();
        return false;
    } catch (json::exception& e) {
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