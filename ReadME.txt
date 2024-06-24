main.py
实现自动根据binary图像获取二维检测框，并将相关信息写入符合label要求的XML中，用于训练
实现步骤：
准备：将所有的截图文件（包含binary、empty）放在all文件夹下
1、通过TIP_get_category.py获得category.txt
2、查姐将裁剪后的图像和包含裁剪信息的offset.txt
3、在main文件中更新这些文件的路径
4、XML在同级目录下的XML文件夹下存储