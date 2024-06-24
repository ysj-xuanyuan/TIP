import os

def delete_files(directory):
    try:
        for filename in os.listdir(directory):
            # 分离文件名和扩展名
            file_base, file_extension = os.path.splitext(filename)
            
            # 跳过没有扩展名的文件
            if not file_base:
                continue
            
            # 使用 '-' 分割文件名
            parts = file_base.split('-')
            
            # 如果分割后部分为空，跳过
            if not parts:
                continue
            
            # 获取最后一部分
            last_char = parts[-1]

            # 如果最后一个字符不是 '1'、'2'、'7'，则删除文件
            if last_char not in ['1', '2', '7']:
                file_path = os.path.join(directory, filename)
                os.remove(file_path)
                print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    directory_path = input("Please enter the directory path: ")

    if not os.path.isdir(directory_path):
        print(f"The path {directory_path} is not a valid directory.")
    else:
        delete_files(directory_path)
