import cv2
import pytesseract
import xml.etree.ElementTree as ET
import json

# Path to connect tesseract

# Connecting photo
img = cv2.imread('/Users/timurmitrofanov/Desktop/Herder/TestImage.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Configures Tesseract OCR with specific settings for text extraction.
config = r'--oem 3 --psm 6'
print(pytesseract.image_to_string(img, config=config))

data = pytesseract.image_to_data(img, config=config)

recognized_text = []

# Create XML file
root = ET.Element("document")
page = ET.SubElement(root, "page")

# Iterate through the data extracted from the image.
for i, el in enumerate(data.splitlines()):
    if i == 0:
        continue

    el = el.split()
    try:
        # Creates captions on the picture
        x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
        cv2.rectangle(img, (x, y), (w + x, h + y), (0, 0, 255), 1)
        text = el[11]
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)

        # Add recognized text to the list
        recognized_text.append({"text": text, "x": x, "y": y, "width": w, "height": h})

        # Add recognized text to XML
        word = ET.SubElement(page, "word")
        word.set("x", str(x))
        word.set("y", str(y))
        word.set("width", str(w))
        word.set("height", str(h))
        word.text = text
    except IndexError:
        print("Operation was missed")

# Save recognized text to TXT file
with open("recognized_text.txt", "w") as txt_file:
    for item in recognized_text:
        txt_file.write(f"{item['text']}\n")

# Save recognized text to JSON file
with open("recognized_text.json", "w") as json_file:
    json.dump(recognized_text, json_file, indent=4)

# Save XML to a file
tree = ET.ElementTree(root)
tree.write("recognized_layout.xml")

# Displays results
cv2.imshow('Result', img)
cv2.waitKey(0)