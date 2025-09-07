#include "CpCommand.h"
#include <fstream>

namespace {
    bool TRY_RUN = true; // 调试用
}

CpCommand::CpCommand(const std::vector<std::string>& args) {
    if (args.size() >= 2) {
        src_ = args[0];
        dst_ = args[1];
    }
}

bool CpCommand::execute(std::map<std::string, std::string>& commandMap) {
    if (src_.empty() || dst_.empty()) return false;
    if (TRY_RUN) {
        std::cout << "[DRY-RUN] cp " << src_ << " " << dst_ << "\n";
        return true;
    }
    std::ifstream in(src_, std::ios::binary);
    std::ofstream out(dst_, std::ios::binary);
    out << in.rdbuf();
    return in.good() && out.good();
}