# Importing the required libraries
#import io
import time
import sys
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

def main():
    # Path of the PDF or image file
    file_path = sys.argv[-1]
    result_text = scan_text(file_path)
    print(result_text)

def scan_text(file_path): 
    

    # Extracting text from PDF
    if file_path.endswith(".pdf"):
        # Converting PDF to image
        pages = convert_from_path(file_path, 500)
        image_counter = 1
        for page in pages:
            filename = "output/page_" + str(image_counter) + ".jpg"
            page.save(filename, "JPEG")
            image_counter += 1

        # Extracting text from image
        file_limit = image_counter - 1

        for i in range(1, file_limit + 1):
            filename = "output/page_" + str(i) + ".jpg"
            text = str(((pytesseract.image_to_string(Image.open(filename), lang='mal'))))
            text = text.replace('-\n', '')
            write_to_file(text)
            return text

    # Extracting text from image
    elif file_path.endswith(".jpg") or file_path.endswith(".jpeg") or file_path.endswith(".png"):
        text = str(((pytesseract.image_to_string(Image.open(file_path), lang='mal'))))
        text = text.replace('-\n', '')
        write_to_file(text)
        return text

    # Invalid file format
    else:
        print("Invalid file format. Please provide a PDF or image file.")

def write_to_file(text):

    current_time = time.strftime("%Y%m%d-%H%M")
    outfile = f"output/{current_time}.txt"

    with open(outfile,"w") as f:
        f.write(text)

if (__name__ == "__main__"):
    main()