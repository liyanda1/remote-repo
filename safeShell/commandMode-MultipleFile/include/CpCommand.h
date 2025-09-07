#ifndef Cp_COMMEND_H
#define Cp_COMMEND_H
#include "Command.h"

class CpCommand : public Command {
public:
    explicit CpCommand(const std::vector<std::string>& args);
    bool execute(std::map<std::string, std::string>& commandMap) override;
private:
    std::string src_;
    std::string dst_;
};

#endif
