import heapq
from collections import Counter, defaultdict

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def build(text):
    frequency = Counter(text)
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)
    # 利用堆构建哈夫曼树
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)
    return priority_queue[0]

def coding(node, prefix="", code_map=defaultdict(str)):
    if node is not None:
        if node.char is not None:
            code_map[node.char] = prefix
        coding(node.left, prefix + "0", code_map)
        coding(node.right, prefix + "1", code_map)
    return code_map

def compress_diary(source):
    with open(source, 'r', encoding='utf-8') as file:
        text = file.read()
    root = build(text)
    hfmcode = coding(root)
    encoded_text = ''.join(hfmcode[char] for char in text)
    
    # 增加填充位，保证最后一个字节完整，并且能够解码
    # 计算填充位
    padding = 8 - len(encoded_text) % 8
    # 添加填充位
    encoded_text = f"{padding:08b}" + encoded_text + '0' * padding
    
    # 按字节写入二进制文件（操作系统通常是以字节为单位来处理数据的）
    with open("compressed.bin", "wb") as compressed_file:
        for i in range(0, len(encoded_text), 8):
            byte = encoded_text[i:i+8]
            compressed_file.write(bytes([int(byte, 2)]))
    
    # 哈夫曼编码
    with open("codes.bin", "w", encoding='utf-8') as codes_file:
        for char, code in hfmcode.items():
            codes_file.write(f"{char}:{code}\n")

def decompress_diary(compressed_source, codes_source):
    # 从编码文件中获取编码字典
    with open(codes_source, 'r', encoding='utf-8') as codes_file:
        codes = {line.split(':')[1].strip(): line.split(':')[0] for line in codes_file.readlines()}
    
    # 获取压缩的01串
    with open(compressed_source, 'rb') as compressed_file:
        bit_string = ''
        byte = compressed_file.read(1)
        while byte:
            # ord函数用于获取字符的ASCII码值
            byte = ord(byte)
            #  将整数值 byte 格式化为一个包含 8 位二进制的字符串，确保每个字节都有固定长度的二进制表示
            bits = f"{byte:08b}"
            # 获取压缩后的比特流
            bit_string += bits
            byte = compressed_file.read(1)
        
    # 去除填充位，获得原始比特流
    padding = int(bit_string[:8], 2)
    bit_string = bit_string[8:-padding]

    # 解码
    decoded_text = ''
    temp_code = ''
    for bit in bit_string:
        temp_code += bit
        # 检查当前的临时编码是否在霍夫曼编码字典中
        if temp_code in codes:
            decoded_text += codes[temp_code]
            temp_code = ''

    with open("decompressed.txt", 'w', encoding='utf-8') as output_file:
        output_file.write(decoded_text)