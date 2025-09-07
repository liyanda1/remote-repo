#include "SafeShell.h"
// g++ -std=c++14 -o safe_shell main.cpp src/* -I include

int main() {
    ShellScriptExecutor executor;
    if (!executor.executeScript("test_script.sh")) {
        std::cerr << "Script execution failed\n";
        return 1;
    }
    return 0;
}

