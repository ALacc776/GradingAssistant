import cv2
import easyocr

print(easyocr.__version__)
image_path = "handwriting2.png"   

# 1. Load image
img = cv2.imread(image_path)

# 2. Preprocess – high-contrast black strokes on white
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# enlarge a bit to help recognition of chunky strokes
gray = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresh = cv2.threshold(
    blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

# 3. OCR reader
reader = easyocr.Reader(['en'])

# only allow characters you expect:
#allow_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}[](),.+=- "
allow_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}[]"

results = reader.readtext(
    thresh,
    detail=1,
    paragraph=False,
    allowlist=allow_chars,
)

lines = []
for (bbox, text, conf) in results:
    print(f"{conf:0.2f}  ->  {text!r}")
    lines.append((bbox[0][1], text))  # (y, text)

# 4. Roughly sort by vertical position to reconstruct lines
lines_sorted = [t for _, t in sorted(lines, key=lambda x: x[0])]
print("\nCombined (naive join):")
print(" ".join(lines_sorted))
