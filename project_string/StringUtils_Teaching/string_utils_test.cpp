#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "string_utils.h"

using namespace testing;
using namespace std;

// 测试EndsWith函数
TEST(StringUtilsTest, EndsWithNormalCase) {
    // 测试功能：验证正常后缀检查
    // 前置条件：有效输入字符串
    // 测试因子：后缀长度小于字符串长度
    EXPECT_TRUE(StringUtils::EndsWith("hello_world", "world"));
    EXPECT_FALSE(StringUtils::EndsWith("hello_world", "word"));
}

TEST(StringUtilsTest, EndsWithEmptySuffix) {
    // 测试功能：空后缀处理
    // 前置条件：后缀为空字符串
    // 预期结果：应返回true（任何字符串都以空字符串结尾）
    EXPECT_TRUE(StringUtils::EndsWith("hello", ""));
}

TEST(StringUtilsTest, EndsWithLongerSuffix) {
    // 测试功能：后缀比原字符串长
    // 前置条件：后缀长度 > 字符串长度
    // 测试因子：边界条件
    // 预期结果：应抛出异常或崩溃（实际会引发未定义行为）
    EXPECT_THROW(StringUtils::EndsWith("hi", "hello"), std::out_of_range);
}

// 测试Split函数
TEST(StringUtilsTest, SplitNormalCase) {
    // 测试功能：正常分割操作
    // 前置条件：有效输入
    // 测试因子：分隔符存在
    vector<string> expected = {"a", "b", "c"};
    EXPECT_EQ(StringUtils::Split("a,b,c", ','), expected);
}

TEST(StringUtilsTest, SplitEmptyInput) {
    // 测试功能：空输入处理
    // 前置条件：空字符串输入
    // 测试因子：边界条件
    // 预期结果：应返回空vector（实际会返回包含空字符串的vector）
    EXPECT_TRUE(StringUtils::Split("", ',').empty());
}

// 测试ReplaceSubstring函数
TEST(StringUtilsTest, ReplaceValidSubstring) {
    // 测试功能：正常替换操作
    // 前置条件：有效索引
    // 测试因子：常规替换
    EXPECT_EQ(StringUtils::ReplaceSubstring("hello world", 6, 5, "there"), "hello there");
}

TEST(StringUtilsTest, ReplaceInvalidPosition) {
    // 测试功能：越界起始位置
    // 前置条件：起始位置 > 字符串长度
    // 测试因子：错误处理
    // 预期结果：应抛出异常（实际会引发未定义行为）
    EXPECT_THROW(StringUtils::ReplaceSubstring("hello", 10, 2, "!!"), std::out_of_range);
}

// 测试IsValidPassword函数
TEST(StringUtilsTest, ValidPassword) {
    // 测试功能：有效密码检查
    // 前置条件：符合规则的密码
    EXPECT_TRUE(StringUtils::IsValidPassword("Pass123"));
}

TEST(StringUtilsTest, NullPassword) {
    // 测试功能：空指针处理
    // 前置条件：nullptr输入
    // 测试因子：错误处理
    // 预期结果：应返回false或抛出异常（实际会导致段错误）
    EXPECT_FALSE(StringUtils::IsValidPassword(nullptr));
}

TEST(StringProcessorTest, CopyToBuffer_BufferTooSmall_ShouldFail) {
    StringProcessor processor;
    char buffer[5];

    // 注意：这里故意触发越界
    EXPECT_DEATH(processor.copyToBuffer("1234567890", buffer, sizeof(buffer)), ".*");
}

TEST(StringProcessorTest, CopyToBuffer_NullBuffer_ShouldFail) {
    StringProcessor processor;

    // 空指针测试
    EXPECT_DEATH(processor.copyToBuffer("abc", nullptr, 10), ".*");
}

// 使用gmock模拟复杂依赖
class MockValidator {
public:
    virtual bool Validate(const string&) const = 0;
    virtual ~MockValidator() = default;
};

class MockValidatorMock : public MockValidator {
public:
    MOCK_METHOD(bool, Validate, (const string&), (const, override));
};

TEST(StringUtilsTest, PasswordWithMock) {
    // 测试功能：与外部验证器集成
    // 前置条件：创建mock对象
    MockValidatorMock mockValidator;
    EXPECT_CALL(mockValidator, Validate("Pass123"))
        .WillOnce(Return(true));
    
    // 执行步骤：调用真实函数并使用mock验证
    bool result = StringUtils::IsValidPassword("Pass123");
    
    // 预期结果：集成正确
    EXPECT_TRUE(result);
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}