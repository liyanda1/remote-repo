// SafeShell.cpp
#include "SafeShell.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <sys/stat.h>
#include <regex>
#include <cerrno>
#include <cstring>

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
        if (line.empty() || line[0] == '#') continue;

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
            return false;
        }
    }
    return true;
}

bool SafeShell::parseLine(const std::string& line) {
    if (handleAssignment(line)) return true;
    return handleCommand(line);
}

bool SafeShell::handleAssignment(const std::string& line) {
    size_t eq_pos = line.find('=');
    if (eq_pos == std::string::npos) return false;

    std::string key = line.substr(0, eq_pos);
    std::string value = line.substr(eq_pos + 1);

    static const std::regex key_pattern(R"(^[A-Za-z_][A-Za-z0-9_]*$")");
    if (!std::regex_match(key, key_pattern)) {
        std::cerr << "Invalid variable name: " << key << "\n";
        return true;
    }

    variables_[key] = expandVariables(value);
    if (g_dry_run) {
        std::cout << "[DRY-RUN] set " << key << "=" << variables_[key] << "\n";
    }
    return true;
}

bool SafeShell::handleCommand(const std::string& line) {
    auto tokens = tokenizeLine(line);
    if (tokens.empty()) return true;

    std::string cmd = expandVariables(tokens[0]);
    std::vector<std::string> args;
    for (size_t i = 1; i < tokens.size(); ++i) {
        args.push_back(expandVariables(tokens[i]));
    }

    auto it = command_map_.find(cmd);
    if (it == command_map_.end()) {
        std::cerr << "Unknown command: " << cmd << "\n";
        return false;
    }
    return it->second(args);
}

std::vector<std::string> SafeShell::tokenizeLine(const std::string& line) {
    std::istringstream iss(line);
    std::vector<std::string> tokens;
    std::string token;
    while (iss >> token) tokens.push_back(token);
    return tokens;
}

std::string SafeShell::expandVariables(const std::string& input) {
    if (input.find("${") == std::string::npos) return input;

    std::string result;
    std::regex var_pattern(R"(\$\{([^}]+)\})");
    auto begin = input.cbegin();
    auto end = input.cend();
    std::smatch match;

    while (std::regex_search(begin, end, match, var_pattern)) {
        result.append(match.prefix());
        std::string varname = match[1].str();

        auto it = variables_.find(varname);
        if (it != variables_.end()) {
            result.append(it->second);
        } else {
            const char* env = std::getenv(varname.c_str());
            result.append(env ? env : "");
        }

        begin = match.suffix().first;
    }
    result.append(begin, end);
    return result;
}

bool SafeShell::cmdRm(const std::vector<std::string>& args) {
    if (args.empty()) return false;
    if (g_dry_run) {
        std::cout << "[DRY-RUN] rm " << args[0] << "\n";
        return true;
    }
    if (std::remove(args[0].c_str()) != 0) {
        std::cerr << "rm failed: " << strerror(errno) << "\n";
        return false;
    }
    return true;
}

bool SafeShell::cmdMkdir(const std::vector<std::string>& args) {
    if (args.empty()) return false;
    if (g_dry_run) {
        std::cout << "[DRY-RUN] mkdir " << args[0] 
                  << (args.size()>1 ? " "+args[1] : "") 
                  << (args.size()>2 ? " "+args[2] : "") << "\n";
        return true;
    }
    if (mkdir(args[0].c_str(), 0755) != 0 && errno != EEXIST) {
        std::cerr << "mkdir failed: " << strerror(errno) << "\n";
        return false;
    }
    return true;
}

bool SafeShell::cmdCp(const std::vector<std::string>& args) {
    if (args.size() < 2) return false;
    if (g_dry_run) {
        std::cout << "[DRY-RUN] cp " << args[0] << " " << args[1] << "\n";
        return true;
    }
    std::ifstream in(args[0], std::ios::binary);
    if (!in.is_open()) {
        std::cerr << "cp failed: cannot open source file\n";
        return false;
    }
    std::ofstream out(args[1], std::ios::binary);
    if (!out.is_open()) {
        std::cerr << "cp failed: cannot open destination file\n";
        return false;
    }
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
    return true;
}

bool SafeShell::cmdReplace(const std::vector<std::string>& args) {
    if (args.empty()) return false;
    if (g_dry_run) {
        std::cout << "[DRY-RUN] replace " << args[0]
                  << (args.size()>1 ? " "+args[1] : "") << "\n";
        return true;
    }
    return true;
}