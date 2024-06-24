import os

def get_unique_filenames(folder):
    unique_names = set()
    for filename in os.listdir(folder):
        if not filename.startswith('.'):  # 忽略隐藏文件
            name, ext = os.path.splitext(filename)
            if len(name) >= 8:
                unique_names.add(name[-8:])
    return unique_names

def check_files_exist(base_name, folder):
    indexes = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12]
    required_files = [
        f"{base_name}-{i}.BMP" for i in indexes
    ] + [
        f"{base_name}empty-{i}.BMP" for i in indexes
    ] + [
        f"{base_name}binary-{i}.BMP" for i in indexes
    ] + [f"{base_name}m.txt"]

    missing_files = []
    for file in required_files:
        if not os.path.isfile(os.path.join(folder, file)):
            missing_files.append(file)
    return missing_files

def main():
    folder1 = input("请输入Bag文件夹的路径: ")
    folder2 = input("请输入BMP文件夹的路径: ")

    if not os.path.isdir(folder1) or not os.path.isdir(folder2):
        print("输入的路径无效，请确保路径正确。")
        return

    unique_filenames = get_unique_filenames(folder1)
    # 对 unique_filenames 进行排序
    sorted_filenames = sorted(unique_filenames, key=lambda x: int(x))
    for base_name in sorted_filenames:
        missing_files = check_files_exist(base_name, folder2)
        if missing_files:
            # print(f"对于基本文件名 '{base_name}'，缺少文件: {', '.join(missing_files)}")
            print(f"对于基本文件名 '{base_name}'缺少文件")

if __name__ == "__main__":
    main()
    input("检查完成。按回车键退出...")
