import os
import xml.etree.ElementTree as ET
'''
将1.96的XML转换成19.7的XML
需要根据1.96以及19.7的offset更新二维坐标点，以及新的裁剪图像尺寸
'''

xml_old = "G:\\测试集\\1.96\\xmls" # 1.96xml
xml_new = "G:\\测试集\\19.7\\xmls" # 19.7xml

offset_path_old = "G:\\测试集\\1.96\\offset.txt"
offset_path_new = "G:\\测试集\\19.7\\offset.txt"


def modify_xml(input_path, output_path, new_width, new_height, offset_old,offset_new):
    tree = ET.parse(input_path)
    root = tree.getroot()
    
    # Modify size
    if new_width!=0 and new_height!=0:
        size = root.find('size')
        size.find('width').text = str(new_width)
        size.find('height').text = str(new_height)
    
    offset_x_old= int(offset_old[2])
    offset_y_old = int(offset_old[3])
    offset_x_new= int(offset_new[2])
    offset_y_new = int(offset_new[3])

    # print(offset_x_new,offset_y_new,offset_x_old,offset_y_old)
    # Modify bndbox for each object
    for i, obj in enumerate(root.findall('object')):
        bndbox = obj.find('bndbox')
        old_bbox = {
            'xmin': int(bndbox.find('xmin').text),
            'ymin': int(bndbox.find('ymin').text),
            'xmax': int(bndbox.find('xmax').text),
            'ymax': int(bndbox.find('ymax').text)
        }
        # 新的坐标加之前的offset，减新的offset
        new_bbox = {
            'xmin': int(old_bbox['xmin'] + offset_x_old - offset_x_new),
            'ymin': int(old_bbox['ymin'] + offset_y_old - offset_y_new),
            'xmax': int(old_bbox['xmax'] + offset_x_old - offset_x_new),
            'ymax': int(old_bbox['ymax'] + offset_y_old - offset_y_new)
        }
        # print(new_bbox)
        bndbox.find('xmin').text = str(new_bbox['xmin'])
        bndbox.find('ymin').text = str(new_bbox['ymin'])
        bndbox.find('xmax').text = str(new_bbox['xmax'])
        bndbox.find('ymax').text = str(new_bbox['ymax'])
    
    # Save the modified XML to the output path
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

def get_offset(path):
    result = {}
    try:
        with open(path, 'r') as file:
            for line in file:
                stripped_line = line.strip()
                if stripped_line:  # 只处理非空行
                    parts = stripped_line.split()
                    key = parts[0]
                    values = parts[1:]
                    result[key] = values
    except FileNotFoundError:
        print(f"文件 {path} 不存在。")
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
    return result

def get_xml(files):
    # 读取裁剪信息
    offsets_old = get_offset(offset_path_old)
    offsets_new = get_offset(offset_path_new)
    # print(offsets)

    # for file in files[:3]:
    for file in files:
            
        # 二维点+offset
        if file[:-4] in offsets_old:
            offset_old = offsets_old[file[:-4]]
        else:
            offset_old = [0,0,0,0]
            print(f'{file} 没有对应的offset_old')
        if file[:-4] in offsets_new:
            offset_new = offsets_new[file[:-4]]
        else:
            offset_new = [0,0,0,0]
            print(f'{file} 没有对应的offset_new')

        # 更新裁剪尺寸    
        new_width = offset_new[1]
        new_height = offset_new[0]

        # XML path
        old_path = os.path.join(xml_old,file)
        new_path = os.path.join(xml_new,file)
        # 将二维框信息写入xml
        modify_xml(old_path, new_path, new_width, new_height, offset_old,offset_new)


if __name__ == '__main__':
    files = os.listdir(xml_old)
    get_xml(files)
