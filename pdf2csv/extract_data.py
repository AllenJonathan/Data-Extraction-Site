import pytesseract
from PIL import Image
import io
from pdf2image import convert_from_bytes


def pdf_to_csv(file_bytes, file_type=None):
    # Install both and copy PATH
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    poppler_path = r'C:\\Program Files\\poppler-23.05.0\\Library\\bin'

    # Load the image
    if file_type == 'pdf':
        image = convert_from_bytes(file_bytes, dpi=360, poppler_path=poppler_path)[0]
    else:
        image = Image.open(io.BytesIO(file_bytes))

    # Use OCR to extract text
    data = pytesseract.image_to_data(image, lang='eng')

    extracted_data = extract_data(data)

    # Delete footer data
    for i in range(len(extracted_data) - 1, -1, -1):
        if len(extracted_data[i]) == 1:
            del extracted_data[i]
        elif len(extracted_data[i]) > 3:
            break

    return extracted_data


def extract_data(data):
    """extracts the necessary information"""
    cleaned_data = []
    cell = []
    cell_data = ''
    table = False

    lines = data.split("\n")
    for i in range(1, len(lines)):
        if i == len(lines) - 1:
            if table:
                return cleaned_data
            else:
                return []
        info = lines[i].split("\t")
        if i < len(lines) - 2:
            next_info = lines[i + 1].split("\t")
            if next_info[11] == " ":
                next_info = None
        else:
            next_info = None
        if info[5].isdigit() and info[5] != "0" and info[11] != " ":
            # if word exists
            if float(info[10]) < 50 or "|" in info[11]:
                continue
            if ":" in info[11] and not table:
                cell_data += info[11][:-1]
                cell.append(cell_data.strip())
                cell_data = ""
            elif next_info and "|" in next_info[11]:
                cell_data += info[11]
                cell.append(cell_data.strip())
                cell_data = ""
            elif next_info and len(next_info[11].strip()) > 0 and int(next_info[6]) - (
                    int(info[6]) + int(info[8])) > int(info[9]):
                table = True
                cell_data += info[11]
                cell.append(cell_data.strip())
                cell_data = ""
            else:
                cell_data += info[11] + " "
        else:
            # row
            if len(cell_data.strip()) > 0:
                cell.append(cell_data.strip())
                cleaned_data.append(cell)
                cell = []
                cell_data = ''
