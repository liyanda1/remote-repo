#ifndef COMMEND_H
#define COMMEND_H

#include <string>
#include <vector>
#include <memory>
#include <map>
#include <functional>
#include <iostream>

// 命令抽象基类
class Command {
public:
    virtual ~Command() {}
    virtual bool execute(std::map<std::string, std::string>& commandMap) = 0;
};


#endif