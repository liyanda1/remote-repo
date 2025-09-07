#include "ShellScriptExecutor.h"
#include <fstream>
#include <sstream>
#include "CpCommand.h"
#include "MkdirCommand.h"
#include "RmCommand.h"


bool ShellScriptExecutor::executeScript(const std::string& filepath) {
    std::ifstream file(filepath);
    if (!file.is_open()) return false;

    std::string line;
    std::map<std::string, std::string> commandMap;
    bool firstLine = true;

    // 注册命令
    CommandFactory::instance().registerCommand("rm", [](const std::vector<std::string>& args) -> std::unique_ptr<Command> {
        return std::make_unique<RmCommand>(args);
    });
    CommandFactory::instance().registerCommand("mkdir", [](const std::vector<std::string>& args) -> std::unique_ptr<Command> {
        return std::make_unique<MkdirCommand>(args);
    });
    CommandFactory::instance().registerCommand("cp", [](const std::vector<std::string>& args) -> std::unique_ptr<Command> {
        return std::make_unique<CpCommand>(args);
    });

    while (std::getline(file, line)) {
        if (line.empty()) continue;

        if (firstLine) {
            firstLine = false;
            if (line != "#!safe_shell") {
                std::cerr << "Invalid shebang: " << line << "\n";
                return false;
            }
            continue;
        }

        if (!parseLine(line, commandMap)) {
            std::cerr << "Failed to parse line: " << line << "\n";
        }
    }
    return true;
}

bool ShellScriptExecutor::parseLine(const std::string& line, std::map<std::string, std::string>& commandMap) {
    if (line[0] == ' ') return true; // 保留空格开头的行为

    std::istringstream iss(line);
    std::string cmd;
    iss >> cmd;

    std::vector<std::string> args;
    std::string arg;
    while (iss >> arg) args.push_back(arg);

    auto command = CommandFactory::instance().create(cmd, args);
    if (!command) {
        std::cerr << "Unknown command: " << cmd << "\n";
        return false;
    }
    return command->execute(commandMap);
}