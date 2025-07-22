
#include "string_utils.h"
#include <cstring>
#include <sstream>
#include <stdexcept>
#include <algorithm>

using namespace std;

bool StringUtils::EndsWith(const std::string& str, const std::string& suffix) {
    if (suffix.size() > str.size()) {
        return false; // 后缀比原字符串长，直接返回false
    }
    return str.compare(str.size() - suffix.size(), suffix.size(), suffix) == 0;
}

vector<string> StringUtils::Split(const std::string& str, char delimiter) {
    vector<string> tokens;
    if (str.empty()) {
        return tokens; // 空输入返回空vector
    }
    stringstream ss(str);
    string token;

    while (getline(ss, token, delimiter)) {
        tokens.push_back(token);
    }
    return tokens;
}

string StringUtils::ReplaceSubstring(const std::string& str, size_t start, size_t length, const std::string& replacement) {
    if (start > str.size()) {
        throw out_of_range("Start index out of range");
    }
    size_t effective_length = min(length, str.size() - start);
    string result = str;
    result.replace(start, effective_length, replacement);
    return result;
}

bool StringUtils::IsValidPassword(const char* password) {
    if (password == nullptr) {
        return false; // 空指针无效
    }
    bool hasUpper = false, hasDigit = false;

    for (size_t i = 0; i < strlen(password); i++) {
        if (isupper(password[i])) hasUpper = true;
        if (isdigit(password[i])) hasDigit = true;
    }

    return hasUpper && hasDigit;
}

void StringUtils::copyToBuffer(const std::string& src, char* buffer, size_t bufferSize) {
    if (buffer == nullptr) {
        throw invalid_argument("Buffer is null");
    }
    if (src.size() + 1 > bufferSize) {
        throw out_of_range("Buffer size too small for copy");
    }
    std::memcpy(buffer, src.c_str(), src.size());
    buffer[src.size()] = '\0';
}
