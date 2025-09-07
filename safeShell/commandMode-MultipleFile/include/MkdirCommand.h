#ifndef MKDIR_COMMEND_H
#define MKDIR_COMMEND_H
#include "Command.h"

class MkdirCommand : public Command {
public:
    explicit MkdirCommand(const std::vector<std::string>& args);
    bool execute(std::map<std::string, std::string>& commandMap) override;
private:
    std::string path_;
    std::string owner_;
    std::string perm_;
};


#endif