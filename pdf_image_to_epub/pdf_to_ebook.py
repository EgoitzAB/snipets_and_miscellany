#!usr/bin/python3
from tempfile import TemporaryDirectory
from pathlib import Path

from pytesseract import image_to_string
from pdf2image import convert_from_path
from PIL import Image
import aspose.words as aw

""" Get a image pdf, extract the text with pytesseract and return txt document and epub document."""

out_directory = Path("~").expanduser()
PDF_file = Path(r"Fundamentos.pdf").absolute()
image_file_list = []
text_file = "programing_book.txt"

def convert_pdf_to_images():
    """ Converting to text from pdf image. """
    pdf_pages = convert_from_path(PDF_file, 120)
    return pdf_pages


def save_pages_to_list(pdf_pages):
    """ Paginating and sending to a list."""
    with TemporaryDirectory() as tempdir:
        for page_enumeration, page in enumerate(pdf_pages, start=1):
            filename = f"{tempdir}\page_{page_enumeration:03}.jpg"
            page.save(filename, "JPEG")
            image_file_list.append(filename)


def extract_text():
    """ Opening the listfile images, formatting to strings and making a file."""
    with open(text_file, "a") as output_file:
        for image_file in image_file_list:
            text = str(image_to_string(Image.open(image_file), lang="spa"))
            text = text.replace("-\n", "")
            output_file.write(text)


def txt_to_epub():
    """ Formatting from txt file to epub, I think that can be done earlier but... late for me."""
    document = "programing_book.txt"
    doc = aw.Document(document)
    doc.save("Programing.epub")


if __name__ == "__main__":
    converted_pages = convert_pdf_to_images()
    save_pages_to_list(converted_pages)
    extract_text()
    txt_to_epub()
