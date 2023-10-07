import cv2
import pytesseract

# Path to Tesseract OCR executable
pytesseract.pytesseract_cmd = '/usr/local/bin/tesseract'

# Load the image
img = cv2.imread('/Users/timurmitrofanov/Desktop/111.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

# Tesseract configuration
config = r'--oem 3 --psm 6'

# Print recognized text
print(pytesseract.image_to_string(img, lang='rus', config=config)) # Other languages can be found at https://tesseract-ocr.github.io/tessdoc/Data-Files.html


data = pytesseract.image_to_data(img, lang='rus', config=config)

# Iterate through the data extracted from the image.
for i, el in enumerate(data.splitlines()):
    if i == 0:
        continue
    el = el.split()
    try:
        x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
        cv2.rectangle(img, (x, y), (w + x, h + y), (0, 0, 255), 1)
        cv2.putText(img, el[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, 1)
    except IndexError:
        print("Done")

# Display results
cv2.imshow('Result', img)
cv2.waitKey(0)