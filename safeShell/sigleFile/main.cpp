#include "SafeShell.h"
#include <iostream>

int main() {
    SafeShell shell;
    if (!shell.executeScript("test_script.sh")) {
        std::cerr << "Script execution failed\n";
        return 1;
    }
    return 0;
}

