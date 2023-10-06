import cv2
import pytesseract

# Path to Tesseract OCR executable
pytesseract.pytesseract_cmd = '/usr/local/bin/tesseract'

pytesseract.pytesseract.tessdata_dir_config = '--tessdata-dir "/usr/local/share/tessdata"'

# Load the image
img = cv2.imread('/Users/timurmitrofanov/Desktop/photo_2022-10-03_18-31-07.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

# Tesseract configuration
config = r'--oem 3 --psm 6'

# # Perform text recognition
print(pytesseract.image_to_string(img, lang='rus', config=config)) 

# Other languages can be found at https://tesseract-ocr.github.io/tessdoc/Data-Files.html
# Use the following command in Terminal in order to add new language: sudo mv /Users/Path_to_eng.traineddata /usr/local/share/tessdata/

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



############
# Save recognized text to a TXT file
with open("recognized_text.txt", "w", encoding="utf-8") as txt_file:
    txt_file.write(recognized_text)

# Extract layout information
data = pytesseract.image_to_data(img, lang='rus', config=config)
recognized_layout = []

# Save recognized layout to a JSON file
with open("recognized_layout.json", "w", encoding="utf-8") as json_file:
    json.dump(recognized_layout, json_file, ensure_ascii=False, indent=4)

# Create XML file for layout information
root = ET.Element("document")
page = ET.SubElement(root, "page")

# Iterate through recognized layout and add to XML
for item in recognized_layout:
    word = ET.SubElement(page, "word")
    word.set("x", str(item["x"]))
    word.set("y", str(item["y"]))
    word.set("width", str(item["width"]))
    word.set("height", str(item["height"]))
    word.text = item["word"]

# Save XML layout information to a file
tree = ET.ElementTree(root)
tree.write("recognized_layout.xml", encoding="utf-8")