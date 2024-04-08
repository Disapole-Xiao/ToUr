def remove_lines_with_strings(file_path, strings):
    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        if not any(string in line for string in strings):
            modified_lines.append(line)

    with open(file_path, 'w', encoding="utf-8") as file:
        file.writelines(modified_lines)
    
strings = input().split()
file_path = "tool/1.osm"
remove_lines_with_strings(file_path, strings)