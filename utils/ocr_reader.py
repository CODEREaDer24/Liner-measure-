import pytesseract
import cv2

def extract_ab_from_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    data = pytesseract.image_to_string(gray)
    ab_pairs = []

    for line in data.split("\n"):
        if line.strip() and any(c.isdigit() for c in line):
            parts = line.split()
            try:
                a = int(parts[0].replace("'", "").replace('"', ''))
                b = int(parts[1].replace("'", "").replace('"', ''))
                ab_pairs.append((a, b))
            except:
                continue

    return ab_pairs