#include "RmCommand.h"

namespace {
    bool TRY_RUN = true; // 调试用
}

RmCommand::RmCommand(const std::vector<std::string>& args) {
    if (!args.empty()) target_ = args[0];
}

bool RmCommand::execute(std::map<std::string, std::string>& commandMap) {
    if (target_.empty()) return false;
    if (TRY_RUN) {
        std::cout << "[DRY-RUN] rm " << target_ << "\n";
        return true;
    }
    return std::remove(target_.c_str()) == 0;
}