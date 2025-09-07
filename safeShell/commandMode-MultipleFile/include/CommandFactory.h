#ifndef COMMEND_FACTORY_H
#define COMMEND_FACTORY_H
#include "Command.h"

// 工厂函数注册表
class CommandFactory {
public:
    using Creator = std::function<std::unique_ptr<Command>(const std::vector<std::string>&)>;
    static CommandFactory& instance();

    void registerCommand(const std::string& name, Creator creator);
    std::unique_ptr<Command> create(const std::string& name, const std::vector<std::string>& args);

private:
    std::map<std::string, Creator> registry_;
};

#endif