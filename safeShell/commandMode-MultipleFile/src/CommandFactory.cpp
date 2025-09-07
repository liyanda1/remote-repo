#include "CommandFactory.h"

CommandFactory& CommandFactory::instance() {
    static CommandFactory inst;
    return inst;
}

void CommandFactory::registerCommand(const std::string& name, Creator creator) {
    registry_[name] = creator;
}

std::unique_ptr<Command> CommandFactory::create(const std::string& name, const std::vector<std::string>& args) {
    auto it = registry_.find(name);
    if (it != registry_.end()) {
        return it->second(args);
    }
    return nullptr;
}