#include "string_utils.h"
#include <cstring>
#include <sstream>
#include <stdexcept>

using namespace std;

bool StringUtils::EndsWith(const std::string& str, const std::string& suffix) {
    // 问题1：未检查suffix长度是否大于str长度
    return str.compare(str.length() - suffix.length(), suffix.length(), suffix) == 0;
}

vector<string> StringUtils::Split(const std::string& str, char delimiter) {
    // 问题2：未处理空输入
    vector<string> tokens;
    stringstream ss(str);
    string token;
    
    while (getline(ss, token, delimiter)) {
        tokens.push_back(token);
    }
    return tokens;
}

string StringUtils::ReplaceSubstring(const std::string& str, size_t start, size_t length, const std::string& replacement) {
    // 问题3：未校验start和length的有效性
    string result = str;
    result.replace(start, length, replacement);
    return result;
}

bool StringUtils::IsValidPassword(const char* password) {
    // 问题4：未检查空指针
    bool hasUpper = false, hasDigit = false;
    
    for (size_t i = 0; i < strlen(password); i++) {
        if (isupper(password[i])) hasUpper = true;
        if (isdigit(password[i])) hasDigit = true;
    }
    
    return hasUpper && hasDigit;
}

void StringUtils::copyToBuffer(const std::string& src, char* buffer, size_t bufferSize) {
    // ❌ BUG：未检查 buffer 是否为 nullptr
    // ❌ BUG：未检查 src.size() 是否大于 bufferSize
    std::memcpy(buffer, src.c_str(), src.size());
    buffer[src.size()] = '\0';  // 可能越界
}