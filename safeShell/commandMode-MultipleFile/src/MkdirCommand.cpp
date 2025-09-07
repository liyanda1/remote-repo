#include "MkdirCommand.h"
#include <sys/stat.h>

namespace {
    bool TRY_RUN = true; // 调试用
}

MkdirCommand::MkdirCommand(const std::vector<std::string>& args) {
    if (!args.empty()) path_ = args[0];
    if (args.size() > 1) owner_ = args[1];
    if (args.size() > 2) perm_ = args[2];
}

bool MkdirCommand::execute(std::map<std::string, std::string>& commandMap) {
    if (path_.empty()) return false;
    if (TRY_RUN) {
        std::cout << "[DRY-RUN] mkdir " << path_ << " " << owner_ << " " << perm_ << "\n";
        return true;
    }
    return mkdir(path_.c_str(), 0755) == 0 || errno == EEXIST;
}