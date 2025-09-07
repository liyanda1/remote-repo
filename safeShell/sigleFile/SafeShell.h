// SafeShell.h
#ifndef SAFESHELL_H
#define SAFESHELL_H

#include <string>
#include <map>
#include <vector>
#include <functional>

extern bool g_dry_run;  // 全局 dry-run 变量

class SafeShell {
public:
    SafeShell();
    bool executeScript(const std::string& filepath);

private:
    using CommandHandler = std::function<bool(const std::vector<std::string>&)>;
    std::map<std::string, CommandHandler> command_map_;
    std::map<std::string, std::string> variables_;

    void registerCommands();
    bool parseLine(const std::string& line);
    bool handleAssignment(const std::string& line);
    bool handleCommand(const std::string& line);
    std::vector<std::string> tokenizeLine(const std::string& line);
    std::string expandVariables(const std::string& input);

    // 命令实现函数
    bool cmdRm(const std::vector<std::string>& args);
    bool cmdMkdir(const std::vector<std::string>& args);
    bool cmdCp(const std::vector<std::string>& args);
    bool cmdJson(const std::vector<std::string>& args);
    bool cmdCfgmgr(const std::vector<std::string>& args);
    bool cmdReboot(const std::vector<std::string>& args);
    bool cmdPartctr(const std::vector<std::string>& args);
    bool cmdReplace(const std::vector<std::string>& args);
};

#endif // SAFESHELL_H