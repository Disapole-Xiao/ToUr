import heapq
from collections import Counter, defaultdict

class HuffmanNode:
    def __init__(self, char: bytes, freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def build(text: bytes):
    """
    根据文本的字节构建哈夫曼树
    """
    frequency = Counter(text)
    priority_queue = [HuffmanNode(bytes([char]), freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)
    return priority_queue[0]


def coding(node: HuffmanNode, prefix="", code_map=defaultdict(str)):
    """
    递归地构建哈夫曼编码表
    """
    if node is not None:
        if node.char is not None:
            code_map[node.char] = prefix
        coding(node.left, prefix + "0", code_map)
        coding(node.right, prefix + "1", code_map)
    return code_map


def build_header(node: HuffmanNode, bits=""):
    """
    递归地构建哈夫曼树的头部信息，使用位来记录节点类型。
    """
    if node is not None:
        if node.char is not None:
            # 叶节点：添加'1'和字节数据
            bits += '1' + f"{ord(node.char):08b}"
        else:
            # 内部节点：添加'0'
            bits += '0'
            bits = build_header(node.left, bits)
            bits = build_header(node.right, bits)
    return bits

def compress(text: str):
    """
    根据文本压缩，并构建头信息
    """
    text_bytes = text.encode('utf-8') # 按照utd-8拆开字符
    print('-----拆解后的文本：', text_bytes)
    print('-----原文本大小', len(text_bytes), 'bytes')
    root = build(text_bytes)
    hfm_code = coding(root)
    print('-----映射字典：', hfm_code)

    text_encoded = ''.join(hfm_code[bytes([char])] for char in text_bytes)
    print('-----01文本：', text_encoded)
    header_encoded = build_header(root)
    print('-----01压缩头：', header_encoded)
    file_encoded = header_encoded + text_encoded
    # 计算填充位
    padding = (8 - len(file_encoded) % 8) % 8
    file_encoded = f'{padding:08b}' + '0' * padding + file_encoded
    # 01 -> 字节
    file_encoded = bytes(int(file_encoded[i:i+8], 2) for i in range(0, len(file_encoded), 8))


    # 将压缩头和压缩文本一起写入文件
    with open("compressed.bin", "wb") as compressed_file:
        compressed_file.write(file_encoded)
    print('-----文件头大小：', (8 + padding + len(header_encoded)) / 8, 'bytes')
    print('-----压缩后文本大小：', len(text_encoded) / 8, 'bytes')
    print('-----压缩后总大小：', len(file_encoded), 'bytes')
        
def rebuild(bits, index=0):
    """
    从位串中递归重建哈夫曼树。
    """
    if index >= len(bits):
        return None, index

    if bits[index] == '0':  # 内部节点
        left_node, index = rebuild(bits, index + 1)
        right_node, index = rebuild(bits, index)
        node = HuffmanNode(None, 0)
        node.left = left_node
        node.right = right_node
        return node, index
    else:  # 叶节点
        # 读取接下来的8位作为字符
        char_code = int(bits[index + 1:index + 9], 2)
        node = HuffmanNode(bytes([char_code]), 0)
        return node, index + 9

def read_bits_from_file(file_path):
    """
    从文件读取字节并转换为位串。
    """
    with open(file_path, "rb") as file:
        bit_string = ''
        byte = file.read(1)
        while byte:
            bit_string += f"{int.from_bytes(byte, 'big'):08b}"
            byte = file.read(1)
    return bit_string

def decompress(compressed_file):
    """
    从压缩文件解压文本。
    """
    # 从文件读取压缩的数据
    bit_string = read_bits_from_file(compressed_file)
    padding = int(bit_string[:8], 2)
    bit_string = bit_string[8 + padding:]
    # 重建哈夫曼树
    tree, header_end_index = rebuild(bit_string)

    # 解析填充信息和文本
    text_bits = bit_string[header_end_index:]

    # 解码文本
    index = 0
    decoded_bytes = []
    node = tree
    while index < len(text_bits):
        if text_bits[index] == '0':
            node = node.left
        else:
            node = node.right

        if node.char is not None:  # 叶子节点
            decoded_bytes.append(node.char[0])
            node = tree  # 返回根节点

        index += 1

    decoded_text = bytes(decoded_bytes).decode('utf-8')
    print('-----解码文本：', decoded_text)

if __name__ == "__main__":
    compress('0你好1')
    decompress("compressed.bin")