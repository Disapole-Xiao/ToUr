import csv

def write_dist_to_file(dist, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in dist:
            writer.writerow(row)

def read_dist_from_file(filename):
    dist = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            dist.append([float(cell) for cell in row])
    return dist

# 示例：将 dist 写入文件
dist = [
    [0, 10, 15],
    [10, 0, 35],
    [15, 35, 0]
]
write_dist_to_file(dist, 'dist.csv')

# 示例：从文件中读取 dist
dist_from_file = read_dist_from_file('dist.csv')
print(dist_from_file)