#include "SafeShell.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <sys/stat.h>
#include <regex>

bool g_dry_run = true;  // 默认开启 dry-run，调试安全

SafeShell::SafeShell() {
    registerCommands();
}

void SafeShell::registerCommands() {
    command_map_["rm"]      = [this](const std::vector<std::string>& args){ return cmdRm(args); };
    command_map_["mkdir"]   = [this](const std::vector<std::string>& args){ return cmdMkdir(args); };
    command_map_["cp"]      = [this](const std::vector<std::string>& args){ return cmdCp(args); };
    command_map_["json"]    = [this](const std::vector<std::string>& args){ return cmdJson(args); };
    command_map_["cfgmgr"]  = [this](const std::vector<std::string>& args){ return cmdCfgmgr(args); };
    command_map_["reboot"]  = [this](const std::vector<std::string>& args){ return cmdReboot(args); };
    command_map_["partctr"] = [this](const std::vector<std::string>& args){ return cmdPartctr(args); };
    command_map_["replace"] = [this](const std::vector<std::string>& args){ return cmdReplace(args); };
}

bool SafeShell::executeScript(const std::string& filepath) {
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cerr << "Failed to open script: " << filepath << "\n";
        return false;
    }

    std::string line;
    bool firstLine = true;

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

        if (!parseLine(line)) {
            std::cerr << "Failed to execute line: " << line << "\n";
        }
    }
    return true;
}

bool SafeShell::parseLine(const std::string& line) {
    if (line[0] == ' ') return true; // 跳过空格开头的行

    std::istringstream iss(line);
    std::string cmd;
    iss >> cmd;

    std::vector<std::string> args;
    std::string arg;
    while (iss >> arg) args.push_back(arg);

    auto it = command_map_.find(cmd);
    if (it == command_map_.end()) {
        std::cerr << "Unknown command: " << cmd << "\n";
        return false;
    }
    return it->second(args);
}

// ---------------- 命令实现 ----------------

bool SafeShell::cmdRm(const std::vector<std::string>& args) {
    if (args.empty()) return false;
    if (g_dry_run) {
        std::cout << "[DRY-RUN] rm " << args[0] << "\n";
        return true;
    }
    return std::remove(args[0].c_str()) == 0;
}

bool SafeShell::cmdMkdir(const std::vector<std::string>& args) {
    if (args.empty()) return false;
    if (g_dry_run) {
        std::cout << "[DRY-RUN] mkdir " << args[0] 
                  << (args.size()>1 ? " "+args[1] : "") 
                  << (args.size()>2 ? " "+args[2] : "") << "\n";
        return true;
    }
    return mkdir(args[0].c_str(), 0755) == 0 || errno == EEXIST;
}

bool SafeShell::cmdCp(const std::vector<std::string>& args) {
    if (args.size() < 2) return false;
    if (g_dry_run) {
        std::cout << "[DRY-RUN] cp " << args[0] << " " << args[1] << "\n";
        return true;
    }
    std::ifstream in(args[0], std::ios::binary);
    std::ofstream out(args[1], std::ios::binary);
    if (!in.is_open() || !out.is_open()) return false;
    out << in.rdbuf();
    return true;
}

bool SafeShell::cmdJson(const std::vector<std::string>& args) {
    if (args.size() < 4 || args[1] != "setcurrent") return false;
    const std::string& json_path = args[0];
    const std::string& key = args[2];
    const std::string& value = args[3];

    if (g_dry_run) {
        std::cout << "[DRY-RUN] json set " << json_path << " key=" << key << " value=" << value << "\n";
        return true;
    }

    std::ifstream in(json_path);
    if (!in.is_open()) return false;
    std::ostringstream buf;
    buf << in.rdbuf();
    std::string content = buf.str();

    std::regex pattern("\"" + key + "\"\\s*:\\s*[^,}]+");
    std::string replacement = "\"" + key + "\": " + value;
    std::string new_content = std::regex_replace(content, pattern, replacement);

    std::ofstream out(json_path);
    out << new_content;
    return true;
}

bool SafeShell::cmdCfgmgr(const std::vector<std::string>& args) {
    if (args.empty()) return false;
    if (g_dry_run) {
        std::cout << "[DRY-RUN] cfgmgr " << args[0]
                  << (args.size() > 1 ? " " + args[1] : "")
                  << (args.size() > 2 ? " " + args[2] : "") << "\n";
        return true;
    }
    // TODO: 调用实际 cfgmgr API
    return true;
}

bool SafeShell::cmdReboot(const std::vector<std::string>&) {
    if (g_dry_run) {
        std::cout << "[DRY-RUN] reboot\n";
        return true;
    }
    return system("reboot") == 0;
}

bool SafeShell::cmdPartctr(const std::vector<std::string>& args) {
    if (args.empty()) return false;
    if (g_dry_run) {
        std::cout << "[DRY-RUN] partctr " << args[0]
                  << (args.size()>1 ? " "+args[1] : "") << "\n";
        return true;
    }
    // TODO: 调用实际切区接口
    return true;
}

bool SafeShell::cmdReplace(const std::vector<std::string>& args) {
    if (args.empty()) return false;
    if (g_dry_run) {
        std::cout << "[DRY-RUN] replace " << args[0]
                  << (args.size()>1 ? " "+args[1] : "") << "\n";
        return true;
    }
    // TODO: 实现归档包替换
    return true;
}
