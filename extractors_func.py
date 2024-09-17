import PyPDF2

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF file.
    """
    pdf_file_obj = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page_obj = pdf_reader.pages[page_num]
        text += page_obj.extract_text()
    pdf_file_obj.close()
    return text



from docx import Document

def extract_text_from_word(file_path):
    """
    Extracts text from a Word file.

    Args:
        file_path (str): The path to the Word file.

    Returns:
        str: The extracted text from the Word file.
    """
    text = ''
    with open(file_path, 'rb') as f:
        docx = Document(f)
        for para in docx.paragraphs:
            text += para.text
    return text

import pandas as pd

def extract_text_from_excel(file_path):
    """
    Extracts text from an Excel file.

    Args:
        file_path (str): The path to the Excel file.

    Returns:
        str: The extracted text from the Excel file.
    """
    excel_file = pd.ExcelFile(file_path)
    text = ''
    for sheet_name in excel_file.sheet_names:
        df = excel_file.parse(sheet_name)
        text += df.to_string()
    return text

def extract_text_from_csv(file_path):
    """
    Extracts text from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        str: The extracted text from the CSV file.
    """
    text = ''
    df = pd.read_csv(file_path)
    text += df.to_string()
    return text
