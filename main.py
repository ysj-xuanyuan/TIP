import os
import cv2
import xml.etree.ElementTree as ET

'''
生成TIP合成数据对应的XML
根据TIP合成数据的中间过程：empty/binary进行阈值分割，再根据裁剪的offset对分割后得到的二维框进行修正
将裁剪后图像尺寸、lable、以及二维坐标按规定格式写入XML
'''

# root_dir = "./all"
root_dir = "E:\\tip\\4generate\\4gen\\all"
xml_dir = "./XML_4_19.7"
# xml_dir = "./XML"
tmp_xml = "1.xml"
offset_path = "./offset/offset_4_19.7.txt"
label_path = "./category/category_4.txt"

def find_files(root_dir):
    '''
    输出所有需要处理的文件名
    return list
    ['01014157-1.BMP', '01014157-10.BMP', '01014157-11.BMP', '01014157-12.BMP', '01014157-2.BMP']
    '''
    bmp_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.BMP') and 'binary' not in file and 'empty' not in file:
                bmp_files.append(file)
    return bmp_files

def get_one_2d_point(path,min_size = 10 ,max_size = 900,add_edge = 5):
    '''
    min_size:预测的框大小小于10，舍弃
    max_size:预测的框大小大于900，舍弃
    add_edge:得到的二维框添加5个像素的容错
    '''
    # 读取彩色图像
    # print(path)
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    # cv2.imwrite("gray_image.jpg", gray)
    # cv2.imwrite("binary_image.jpg", binary)

    # 寻找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 获取轮廓的最小外接矩形
    min_rect = [cv2.boundingRect(contour) for contour in contours]
    # print(min_rect)
    # 返回最小外接矩形的左上和右下两个点的坐标，并根据裁剪偏移量调整坐标
    min_rect_points = []
    for rect in min_rect:
        x, y, w, h = rect
        if (w >= min_size or h >= min_size) and w <= max_size and h <= max_size :
            pt1 = [x - add_edge, y - add_edge]
            pt2 = [x + w + add_edge, y + h + add_edge]
            min_rect_points.append(pt1)
            min_rect_points.append(pt2)
    
    return min_rect_points

def process_one_xml(BMPname , new_width , new_height , point2d , label , output_file):
    # 解析XML文件
    tree = ET.parse(tmp_xml)
    root = tree.getroot()

    # 修改filename
    filename = root.find('filename')
    if filename is not None:
        filename.text = BMPname

    # 修改size
    size = root.find('size')
    if size is not None:
        width = size.find('width')
        height = size.find('height')
        if width is not None:
            width.text = str(new_width)
        if height is not None:
            height.text = str(new_height)


    # 寻找<object>元素并修改其中的数据
    for obj in root.findall('object'):
        name = obj.find('name')
        if name is not None :
            name.text = label
        bndbox = obj.find('bndbox')
        if bndbox is not None:
            xmin = bndbox.find('xmin')
            ymin = bndbox.find('ymin')
            xmax = bndbox.find('xmax')
            ymax = bndbox.find('ymax')
            if xmin is not None:
                xmin.text = str(point2d[0][0])
            if ymin is not None:
                ymin.text = str(point2d[0][1])
            if xmax is not None:
                xmax.text = str(point2d[1][0])
            if ymax is not None:
                ymax.text = str(point2d[1][1])

    # 将修改后的XML保存到新文件中
    tree.write(output_file)

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

def get_label(file_path):
    # 初始化一个空字典
    result_dict = {}
    
    # 打开并读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        # 按行读取文件内容
        lines = file.readlines()
    
    # 遍历每一行
    for line in lines:
        # 去掉行尾的换行符和空格
        line = line.strip()
        # 按逗号分割每行的内容
        value, key = line.split(',')
        key = key.replace('.bag', '')
        # 将键值对加入字典
        result_dict[key] = value
    
    return result_dict


def get_xml(files):
    # 读取裁剪信息
    offsets = get_offset(offset_path)
    # print(offsets)
    # 读取label信息
    labels =get_label(label_path)
    # for file in files[:5]:
    for file in files:
        # 每次循环开始初始化信息
        # offset_x = 0
        # offset_y = 0
        # label = ""

        # 获取二维框
        binary_name = file.replace("-","binary-")
        # binary_name = file.replace("-","empty-") # empty的效果好一点
        # print(file)
        binary_path = os.path.join(root_dir,binary_name)
        point2d = get_one_2d_point(binary_path)
        # print(f'point2d : {point2d}')

        # 如果是空托盘，就跳出本次循环
        if len(point2d) == 0:
            print(f'{file} is empty bag')
            continue
        elif len(point2d) != 2:
            #解决在empty图像中物体被错误分成两块的情况,其他情况暂不处理
            # 提取所有x和y坐标
            x_coords = [point[0] for point in point2d]
            y_coords = [point[1] for point in point2d]

            # 找到x和y的最大最小值
            min_x = min(x_coords)
            max_x = max(x_coords)
            min_y = min(y_coords)
            max_y = max(y_coords)
            point2d[0][0] = min_x
            point2d[0][1] = min_y
            point2d[1][0] = max_x
            point2d[1][1] = max_y

        # elif len(point2d) != 2:
        #     print(file)
        #     print(f'point2d : {point2d}')
        #     print('=================',len(point2d),'=======================')
        #     # 提取所有x和y坐标
        #     x_coords = [point[0] for point in point2d[-4:]]
        #     y_coords = [point[1] for point in point2d[-4:]]

        #     # 找到x和y的最大最小值
        #     min_x = min(x_coords)
        #     max_x = max(x_coords)
        #     min_y = min(y_coords)
        #     max_y = max(y_coords)
        #     point2d[0][0] = min_x
        #     point2d[0][1] = min_y
        #     point2d[1][0] = max_x
        #     point2d[1][1] = max_y
            

        # 二维点+offset
        if file[:-4] in offsets:
            offset = offsets[file[:-4]]
        else:
            print(f'{file} 没有对应的offset')
            continue
        # print(offset)
        new_width = offset[1]
        new_height = offset[0]
        offset_x = int(offset[2])
        offset_y = int(offset[3])
        point2d[0][0] = point2d[0][0]-offset_x
        point2d[0][1] = point2d[0][1]-offset_y
        point2d[1][0] = point2d[1][0]-offset_x
        point2d[1][1] = point2d[1][1]-offset_y
        # print(f'point2d offset : {point2d}')

        # 获取label
        if file[:8] in labels:
            label = labels[file[:8]]
        else:
            print(f'{file} 没有对应的label')
            continue

        # XML path
        xml_path = os.path.join(xml_dir,file[:-4]+".xml")
        # 将二维框信息写入xml
        process_one_xml(file[:-4] , new_width , new_height  , point2d , label ,xml_path)


if __name__ == '__main__':
    files = find_files(root_dir)
    # print(files)
    get_xml(files)

