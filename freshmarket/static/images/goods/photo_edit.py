from PIL import Image
import os

print("提示:输出和输入路径都是以 .jpg  或者  .png 结尾的路径，对于输出路径来说，相当于是定义一个新的名字")

def resize_image(input_path, output_path, new_width, new_height):
    try:
        # 打开图片
        image = Image.open(input_path)
        
        # 调整图片大小
        resized_image = image.resize((new_width, new_height))
        
        # 保存调整大小后的图片
        resized_image.save(output_path)
        print("图片调整大小成功！")
    except ValueError as e:
        print(f"错误：{e}")
        print("请确保输入的图片格式是Pillow支持的格式（如.jpg、.png等）")

input_image_path = input("请输入图片路径:")
output_image_path = input("请输入输出路径:")
new_width = int(input("请输入宽度:"))
new_height = int(input("请输入高度:"))

# 检查输入路径是否存在
if not os.path.exists(input_image_path):
    print("错误：输入的图片路径不存在！")
elif os.path.exists(output_image_path):
    print("错误：输出路径已存在！")
else:
    resize_image(input_image_path, output_image_path, new_width, new_height)
