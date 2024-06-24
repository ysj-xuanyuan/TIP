'''
剔除输入目录下扩展名为txt的文件
剔除文件名中包含empty、binary的文件
'''

import os
import shutil

def filter_and_move_files(directory):
    # 检查给定的路径是否是一个目录
    if not os.path.isdir(directory):
        print(f"{directory} 不是一个有效的目录。")
        return

    # 创建一个新的目录来存放过滤后的文件
    filtered_dir = os.path.join(directory, "filtered_files")
    os.makedirs(filtered_dir, exist_ok=True)

    # 遍历目录中的文件
    for filename in os.listdir(directory):
        # 获取文件的完整路径
        file_path = os.path.join(directory, filename)
        
        # 过滤条件：扩展名为".txt"且文件名不包含"empty"和"binary"
        if filename.endswith(".txt") or "empty" in filename or "binary" in filename:
            # 将文件移动到新的目录中
            print(filename)
            shutil.move(file_path, filtered_dir)

    print(f"过滤的文件已移动到 {filtered_dir} 目录中。")

if __name__ == "__main__":
    # 输入文件夹路径
    directory_path = input("请输入需要过滤的文件夹路径：")
    filter_and_move_files(directory_path)
    input("处理完成。按回车键退出...")
