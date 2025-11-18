import pytesseract

from PIL import Image

try:
    img = Image.open('handwriting.png')

    text = pytesseract.image_to_string(img)
    print(text)
except FileNotFoundError:
    print("No such file or directory.")
