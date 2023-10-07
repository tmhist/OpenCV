import cv2
import pytesseract
import json
import xml.etree.ElementTree as ET

# Path to Tesseract OCR executable
pytesseract.pytesseract_cmd = '/usr/local/bin/tesseract'

pytesseract.pytesseract.tessdata_dir_config = '--tessdata-dir "/usr/local/share/tessdata"'

# Load the image
img = cv2.imread('/Users/path/image.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

# Tesseract configuration
config = r'--oem 3 --psm 6'

# Perform text recognition
result_text = pytesseract.image_to_string(img, lang='rus', config=config)

# Save the result to a text file
with open('result.txt', 'w', encoding='utf-8') as file:
    file.write(result_text)

# Other languages can be found at https://tesseract-ocr.github.io/tessdoc/Data-Files.html
# Use the following command in Terminal in order to add new language: sudo mv /Users/Path_to_eng.traineddata /usr/local/share/tessdata/

data = pytesseract.image_to_data(img, lang='rus', config=config)

# Create a dictionary to store the results
result_dict = {
    "text": result_text,  # Распознанный текст
    "layout": []  # Здесь мы будем хранить информацию о разметке (layout)
}

# Create a list to store the layout information
layout_info = []

# Iterate through the data extracted from the image.
for i, el in enumerate(data.splitlines()):
    if i == 0:
        continue
    el = el.split()
    try:
        x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
        cv2.rectangle(img, (x, y), (w + x, h + y), (0, 0, 255), 1)
        cv2.putText(img, el[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, 1)
        text = el[11]
        layout_info.append({
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "text": text
        })
    except IndexError:
        print("Done")

# Save the results as JSON
with open('layout.json', 'w', encoding='utf-8') as json_file:
    json.dump(layout_info, json_file, ensure_ascii=False, indent=4)

# Create the root element for the XML tree
root = ET.Element("layout_info")

# Iterate through the data extracted from the image.
for i, el in enumerate(data.splitlines()):
    if i == 0:
        continue
    el = el.split()
    try:
        x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
        text = el[11]
        
        # Create an element for each layout item
        layout_item = ET.SubElement(root, "layout_item")
        ET.SubElement(layout_item, "x").text = str(x)
        ET.SubElement(layout_item, "y").text = str(y)
        ET.SubElement(layout_item, "width").text = str(w)
        ET.SubElement(layout_item, "height").text = str(h)
        ET.SubElement(layout_item, "text").text = text
    except IndexError:
        print("Done")

# Create an ElementTree object
tree = ET.ElementTree(root)

# Save the layout information as XML
tree.write('layout.xml', encoding='utf-8')

# Display results
cv2.imshow('Result', img)
cv2.waitKey(0)