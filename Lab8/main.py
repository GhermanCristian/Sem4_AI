from PIL import Image

image = Image.open('f1.jpg')
print(image.format)
print(image.mode)
print(image.size)
image.thumbnail((100, 100))
print(image.size)