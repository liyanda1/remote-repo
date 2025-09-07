#ifndef RM_COMMEND_H
#define RM_COMMEND_H
#include "Command.h"

class RmCommand : public Command {
public:
    explicit RmCommand(const std::vector<std::string>& args);
    bool execute(std::map<std::string, std::string>& commandMap) override;
private:
    std::string target_;
};

#endif
