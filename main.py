from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# 输入图片文件夹和输出PDF文件名
input_folder = 'assets/'
output_pdf = 'output.pdf'

# 获取所有图片文件
image_files = [f for f in os.listdir(input_folder) if f.endswith('.png') or f.endswith('.jpg')]

# 每页包含的图片数量
images_per_page = 6

# 创建一个PDF文件
c = canvas.Canvas(output_pdf, pagesize=letter)

# 定义每张图片的宽度和高度
# 计算每张图片的宽度和高度以适应页面大小
page_width, page_height = letter
img_width = page_width / 3  # 一页有三列
img_height = page_height / 2  # 一页有两行

# 定义分割线的高度和颜色
line_height = 10  # 分割线高度
line_color = (0, 0, 0)  # 分割线颜色，黑色

# 定义当前页面上的图片计数器
image_counter = 0

# 循环遍历所有图片
for img_path in image_files:
    img = Image.open(os.path.join(input_folder, img_path))

    # 计算图片的宽高比以决定如何缩放
    img_width_orig, img_height_orig = img.size
    aspect_ratio = img_width_orig / img_height_orig

    # 计算缩放比例以适应页面大小
    if aspect_ratio > 1:
        img_width = page_width / 3  # 一页有三列
        img_height = img_width / aspect_ratio
    else:
        img_height = page_height / 2  # 一页有两行
        img_width = img_height * aspect_ratio

    # 计算图片的位置
    x = (image_counter % 3) * img_width
    y = page_height - ((image_counter // 3) * img_height) - img_height

    # 绘制图片
    c.drawImage(os.path.join(input_folder, img_path), x, y, width=img_width, height=img_height)

    # 绘制分割线
    y -= line_height
    c.setStrokeColorRGB(*line_color)
    c.line(x, y, x + img_width, y)

    image_counter += 1

    if image_counter == images_per_page:
        c.showPage()  # 创建新的PDF页
        image_counter = 0

# 保存PDF文件
c.save()
