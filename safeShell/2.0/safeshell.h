#ifndef SAFE_SHELL_H
#define SAFE_SHELL_H

#include <string>
#include <vector>
#include <unordered_map>
#include <memory>       // for std::unique_ptr, std::make_unique
#include <functional>   // for std::function

// 前向声明 detail 命名空间中的 Command 结构体
// 这是一种常见的 PIMPL (Pointer to Implementation) 思想的变体，可以隐藏实现细节，降低头文件依赖
namespace detail {
    struct Command;
}

/**
 * @class SafeShellInterpreter
 * @brief 一个安全的、自定义的 shell 脚本解释器
 *
 * 该类负责解析和执行一种自定义的、安全的 shell 脚本。
 * 主要特性包括：
 * 1.  两阶段执行：先完整解析脚本，验证语法，然后一次性执行。解析失败则不执行任何命令。
 * 2.  变量支持：支持通过 VAR=value 形式定义变量，并通过 ${VAR} 在命令参数中使用。
 * 3.  严格的语法：每行一个动作，且命令/动作前不允许有前导空格。
 * 4.  C++14 标准：完全使用 C++14 语法和标准库实现，兼容性好。
 * 5.  高内聚低耦合：通过命令分发器模式将命令的解析与执行解耦。
 */
class SafeShellInterpreter {
public:
    /**
     * @brief 构造函数
     *
     * 初始化命令分发器，将命令名称映射到对应的处理函数。
     */
    SafeShellInterpreter();

    /**
     * @brief 析构函数
     */
    ~SafeShellInterpreter();

    /**
     * @brief 解析并执行脚本
     * @param script_content 包含要执行的脚本内容的字符串
     * @param error_message [输出] 如果执行失败，将包含详细的错误信息
     * @return 如果成功执行则返回 true，否则返回 false
     */
    bool execute(const std::string& script_content, std::string& error_message);

private:
    // ------------------- 解析阶段辅助函数 (C++14 兼容) -------------------

    /**
     * @brief 将整个脚本字符串解析成一个命令对象序列
     * @param script_content 待解析的脚本内容
     * @param out_commands [输出] 解析成功时，填充此命令向量
     * @param error_message [输出] 解析失败时的错误信息
     * @return 解析成功返回 true，失败返回 false
     */
    bool parse_script(const std::string& script_content, std::vector<detail::Command>& out_commands, std::string& error_message);

    /**
     * @brief 解析单行脚本，可能是一个命令或一个变量赋值
     * @param line 要解析的单行字符串
     * @param line_num 当前行号，用于错误报告
     * @param out_cmd [输出] 如果该行解析出一个命令，则填充此智能指针；否则该指针为空
     * @param error_message [输出] 解析失败时的错误信息
     * @return 如果行是合法的（命令、变量赋值、空行、注释），则返回 true；如果存在语法错误，则返回 false
     */
    bool parse_line(const std::string& line, int line_num, std::unique_ptr<detail::Command>& out_cmd, std::string& error_message);

    /**
     * @brief 对命令参数中的 ${VAR} 变量进行替换
     * @param args 要进行替换的参数列表（vector of strings）
     * @param line_num 当前行号，用于错误报告
     * @param error_message [输出] 变量未找到时的错误信息
     * @return 所有变量替换成功返回 true，否则返回 false
     */
    bool substitute_variables(std::vector<std::string>& args, int line_num, std::string& error_message);

    // ------------------- 执行阶段辅助函数 -------------------

    /**
     * @brief 按顺序执行已解析的命令列表
     * @param commands 已通过解析阶段的命令列表
     * @param error_message [输出] 执行失败时的错误信息
     * @return 所有命令执行成功返回 true，否则返回 false
     */
    bool execute_commands(const std::vector<detail::Command>& commands, std::string& error_message);

    // ------------------- 命令处理器 -------------------
    // 每个 handle_... 函数负责一个具体命令的参数校验和执行逻辑，实现单一职责原则
    bool handle_rm(const detail::Command& cmd, std::string& error);
    bool handle_mkdir(const detail::Command& cmd, std::string& error);
    bool handle_pkill(const detail::Command& cmd, std::string& error);
    bool handle_json(const detail::Command& cmd, std::string& error);
    bool handle_cfgmgr(const detail::Command& cmd, std::string& error);
    bool handle_reboot(const detail::Command& cmd, std::string& error);
    bool handle_partctr(const detail::Command& cmd, std::string& error);

private:
    // 脚本必须包含的 Shebang 头部
    static const std::string SHEBANG;

    // 用于存储脚本中定义的自定义变量 (VAR=value)
    std::unordered_map<std::string, std::string> variables_;

    // 命令分发器：将命令字符串映射到其处理函数的 `std::function` 对象
    // 这是实现低耦合的关键，新增命令只需在此 map 中注册新函数即可
    using CommandHandler = std::function<bool(const detail::Command&, std::string&)>;
    std::unordered_map<std::string, CommandHandler> command_handlers_;
};

#endif // SAFE_SHELL_H