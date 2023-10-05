import cv2
import pytesseract

# Path to connect tesseract
# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Connecting photo
img = cv2.imread('/Users/timurmitrofanov/Desktop/Herder/TestImage.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Configures Tesseract OCR with specific settings for text extraction.
config = r'--oem 3 --psm 6'
# print(pytesseract.image_to_string(img, config=config))

data = pytesseract.image_to_data(img, config=config)

# Iterate through the data extracted from the image.
for i, el in enumerate(data.splitlines()):
	if i == 0:
		continue

	el = el.split()
	try:
		# Creates captions on the picture
		x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
		cv2.rectangle(img, (x, y), (w + x, h + y), (0, 0, 255), 1)
		cv2.putText(img, el[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)

	except IndexError:
		print("Operation was missed")

# Displays results
cv2.imshow('Result', img)
cv2.waitKey(0)
