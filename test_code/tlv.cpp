#include <iostream>
#include <vector>
#include <string>

using namespace std;

/*
 * 将十六进制字符串转换为字节数组
 * 例如："313233" -> [0x31, 0x32, 0x33]
 */
vector<uint8_t> hexToBytes(const string& hex) {
    vector<uint8_t> bytes;
    for (size_t i = 0; i < hex.size(); i += 2) {
        bytes.push_back(
            static_cast<uint8_t>(stoi(hex.substr(i, 2), nullptr, 16))
        );
    }
    return bytes;
}

/*
 * 判断一段数据是否“看起来像 TLV”
 * 用于做题的结构合法性判断
 */
bool looksLikeTLV(const vector<uint8_t>& data) {
    if (data.size() < 3) return false;

    int len = data[1] | (data[2] << 8);
    return (3 + len <= (int)data.size());
}

/*
 * 递归解析 TLV（核心函数）
 * buffer：当前层 TLV 数据
 * length：当前层边界
 */
void parseTLV(const vector<uint8_t>& buffer, int length, string& result) {

    // 递归终止条件
    if (length < 3) return;

    int index = 0;

    // 遍历本层所有 TLV
    while (index + 2 < length) {

        // 读取 Tag
        uint8_t tag = buffer[index];

        // 读取 Length（小端序）
        int len = buffer[index + 1] | (buffer[index + 2] << 8);

        // TLV 越界校验
        if (index + 3 + len > length) {
            return;
        }

        // 取出 Value
        vector<uint8_t> value(
            buffer.begin() + index + 3,
            buffer.begin() + index + 3 + len
        );

        // 如果 value 还能解析成 TLV，递归
        if (looksLikeTLV(value)) {
            parseTLV(value, len, result);
        } 
        // 否则认为是最内层字符串
        else {
            for (uint8_t c : value) {
                result.push_back(static_cast<char>(c));
            }
        }

        // 回溯：跳到下一个 TLV
        index += 3 + len;
    }
}

int main() {
    string input;
    cin >> input;

    // 十六进制转字节数组
    vector<uint8_t> bytes = hexToBytes(input);

    string result;
    parseTLV(bytes, bytes.size(), result);

    cout << result << endl;
    return 0;
}



// 解法2
#include <bits/stdc++.h>

using namespace std;


vector<int> hexToBytes(const string &str)
{
    vector<int> res;
    for (size_t i = 0; i < str.size(); i += 2) {
        int tmp = stoi(str.substr(i, 2), nullptr, 16);
        res.push_back(tmp);
    }
    return res;
}

bool looklikeTLV(vector<int> &values)
{
    if (values.size() < 3) {
        return false;
    }
    int l = values[1] | (values[2] << 8);
    if (l + 3 <= values.size()) {
        return true;
    }
    return false;
}

void parseTLV(const vector<int> &bytes, int len, vector<pair<int, string>> &res)
{
    if (len < 3) {
        return;
    }
    
    int index = 0;
    
    while (index + 2 < len) {
        auto tag = bytes[index];
        int l = bytes[(index + 1)] | (bytes[(index + 2)] << 8);
        
        if (index + 3 + l > len) {
            return;
        }
        
        vector<int> values(bytes.begin() + index + 3, bytes.begin() + index + 3 + l);
        
        if (looklikeTLV(values)) {
            parseTLV(values, l, res);
        } else {
            pair<int, string> tmp;
            tmp.first = tag;
            for (const auto &item : values) {
                tmp.second.push_back(static_cast<char>(item));
            }
            res.push_back(tmp);
        }
        index = index + 3 + l;
    }
}

int main () {
    
    const string str = "010A0011020041421202003334";
    vector<int> bytes = hexToBytes(str);
    vector<pair<int, string>> res;
    parseTLV(bytes, bytes.size(), res);
    
    
    for (const auto &item : res) {
        cout << item.first << " " << item.second;
        cout << endl;
    }
    return 0;
}