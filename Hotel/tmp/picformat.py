from PIL import Image
def produceImage(file_in, width, height, file_out):
    image = Image.open(file_in)
    resized_image = image.resize((width, height), Image.ANTIALIAS)
    resized_image.save(file_out)

if __name__ == '__main__':
    file_in = '1寸.jpg'
    width = 180
    height = 240
    file_out = '1.jpg'
    produceImage(file_in, width, height, file_out)