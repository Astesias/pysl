from PIL import Image
from pysl import easy_request
from io import BytesIO

# a=Image.open('/Desktop/Image/1.png')
# # a.show()


# im = Image.open(r"/Desktop/Image/1.png")
# # 复制一张图片副本
# im_copy = im.copy()
# # 对副本进行裁剪
# im_crop = im_copy.crop((0, 0, 200, 100))
# # 创建一个新的图像作为蒙版，L模式，单颜色值
# image_new = Image.new('L', (200, 100), 200)
# # 将裁剪后的副本粘贴至副本图像上，并添加蒙版
# im_copy.paste(im_crop, (100, 100, 300, 200), mask=image_new)
# # 显示粘贴后的图像
# im_copy=im_copy.rotate(Image.ROTATE_270)
# im_copy.show()


response=easy_request('https://api.yimian.xyz/img',pic=True).content
print(type(response))
img=Image.open(BytesIO(response))
img.show()
