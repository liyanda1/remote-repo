#ifndef STRING_UTILS_H
#define STRING_UTILS_H

#include <string>
#include <vector>

class StringUtils {
public:
    // 检查字符串是否以指定后缀结尾
    static bool EndsWith(const std::string& str, const std::string& suffix);
    // 分割字符串
    static std::vector<std::string> Split(const std::string& str, char delimiter);
    // 替换子字符串
    static std::string ReplaceSubstring(const std::string& str, size_t start, size_t length, const std::string& replacement);
    // 检查字符串是否符合密码规则
    static bool IsValidPassword(const char* password);
// 3. 将字符串拷贝到缓冲区（有潜在越界风险）
    static void copyToBuffer(const std::string& src, char* buffer, size_t bufferSize);
};

#endif // STRING_UTILS_H