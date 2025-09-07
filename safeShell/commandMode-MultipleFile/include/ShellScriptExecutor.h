#ifndef SHELL_SCRIPT_EXECUTOR_H
#define SHELL_SCRIPT_EXECUTOR_H
#include "Command.h"
#include "CommandFactory.h"

// 脚本执行器
class ShellScriptExecutor {
public:
    ShellScriptExecutor() {}
    bool executeScript(const std::string& filepath);

private:
    bool parseLine(const std::string& line, std::map<std::string, std::string>& commandMap);
};

#endif