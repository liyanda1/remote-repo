#include <iostream>
#include <vector>
#include <string>

using namespace std;


/* 
cin >> c0000000003f00000000000a68656c6c6f20776f7264c0000000001000000000000a68656c6c6f20776f726400000000000a68656c6c6f20776f7264000000000003545454

cout <<
1:hello word
2:hello word
1:hello word
1:TTT
*/

/* 十六进制字符串转字节数组 */
vector<uint8_t> hexToBytes(const string& str) {
    vector<uint8_t> res;
    for (size_t i = 0; i < str.size(); i += 2) {
        res.push_back(static_cast<uint8_t>(
            stoi(str.substr(i, 2), nullptr, 16)));
    }
    return res;
}

/*
 * 递归解析多级 TLV
 * buffer : 当前层 TLV 数据
 * length : 当前层边界
 * level  : 当前嵌套层级
 */
void parseTLV(const vector<uint8_t>& buffer, int length, int level) {
    int index = 0;

    // 至少要有 T(2) + L(4)
    while (index + 5 < length) {

        /* ---------- 解析 T（2 字节，大端） ---------- */
        uint16_t T = (buffer[index] << 8) | buffer[index + 1];

        /* ---------- 解析 L（4 字节，大端） ---------- */
        uint32_t L =
            (buffer[index + 2] << 24) |
            (buffer[index + 3] << 16) |
            (buffer[index + 4] << 8) |
            buffer[index + 5];

        /* ---------- 越界检查 ---------- */
        if (index + 6 + L > length) {
            return;
        }

        /* ---------- 取出 V ---------- */
        vector<uint8_t> V(
            buffer.begin() + index + 6,
            buffer.begin() + index + 6 + L
        );

        /* ---------- 判断 T 的最高位 ---------- */
        bool isNested = (T & 0x8000) != 0;

        if (isNested) {
            // 容器 TLV，递归解析
            parseTLV(V, L, level + 1);
        }
        else {
            // 叶子 TLV，V 是字符串
            string s;
            for (auto c : V) {
                s.push_back(static_cast<char>(c));
            }
            cout << level << ":" << s << endl;
        }

        /* ---------- 回到当前层，解析下一个 TLV ---------- */
        index += 6 + L;
    }
}

int main() {
    string input;
    cin >> input;

    vector<uint8_t> bytes = hexToBytes(input);

    parseTLV(bytes, bytes.size(), 0);

    return 0;
}
