import os

# 定义类别名称与前三个字符之间的映射关系
category_map = {
    "PAK": "PaperKnife",
    "PKB": "PaperKnifeBlade",
    "CAK": "Cai-Dao",
    "PBA": "PortableBattery",
    "KNF": "Knife",
    "CLI": "CigaretteLighter",
    "FLI": "FeLighter",
    "PLI": "PlasticLighter",
    "SFK": "SmallFoldingKnife"
}

def get_category_name(code):
    # 根据前三个字符返回对应的类别名称
    return category_map.get(code, None)

def process_filenames(directory, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if 'binary' not in file and 'empty' not in file:
                    category_code = file[:3]
                    category_name = get_category_name(category_code)
                    if category_name:
                        serial_number = file[-12:]
                        outfile.write(f"{category_name},{serial_number}\n")

def main():
    # 提示用户输入文件夹路径
    directory = input("请输入需要处理的文件夹路径: ")
    output_file = 'category.txt'

    # 执行文件处理
    process_filenames(directory, output_file)
    print(f"处理完成，结果已保存到 {output_file}")

if __name__ == '__main__':
    main()
