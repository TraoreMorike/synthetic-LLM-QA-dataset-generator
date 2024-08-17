from openai import OpenAI
import os
import json
from tqdm import tqdm
import PyPDF2


client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama', 
)



template =  {
    "question": " ",
    "answer": " "
}

single_shot =  {
      "question": "What are the Intellectual Property Rights in the scope of this Agreement?",
      "answer": "The Intellectual Property Rights in the scope of this Agreement include rights associated with works of authorship, including exclusive exploitation rights, copyrights, design rights, moral rights, and mask work rights; trademark, service marks and trade name rights and similar rights; trade secret rights; patent and industrial property rights; other proprietary rights in intellectual property of every kind and nature."
    },

def fix_json (crptd_json):

    messages = [
    {'role': 'system', 'content': f'You are an API that converts the wrongly formatted JSON into a properly fomatted one by following this template : {template} . Only respond with the JSON and no additional text. \n.'},
    {'role': 'user', 'content': 'Wrong JSON: ' + crptd_json}
    ]

    response = client.chat.completions.create(
        model="mistral:latest",
        messages=messages,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=1,

    )


    response_text = response.choices[0].message.content.strip()
    try:
        json_data = json.loads(response_text)
        print(json_data)
        return json_data
    except json.JSONDecodeError:
        print("The JSON is not valid, reformatting again.")
        # fix_json (crptd_json)
        return []


def generate_questions_answers(text_chunk):

    messages = [
    {'role': 'system', 'content': 'You are an API that converts bodies of text into a single question and answer into a JSON format. Each JSON " \
    "should contain a single question with a single answer. Only respond with the JSON and no additional text. \n.'},
    {'role': 'user', 'content': 'Text: ' + text_chunk}
    ]


    response = client.chat.completions.create(
        model="mistral:latest",
        messages=messages,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7,

    )


    response_text = response.choices[0].message.content.strip()
    try:
        json_data = json.loads(response_text)
        print(json_data)
        return json_data
    except json.JSONDecodeError:
        print("Error: Response is not valid JSON.... Trying to fix the JSON.")
        #fix_json(json.loads(response_text))
        return []




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

import docx

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

from typing import List

def process_text(text: str, chunk_size: int = 4000) -> List[dict]:
    """
    Process the given text by splitting it into chunks and generating questions and answers for each chunk.

    Args:
        text (str): The input text to be processed.
        chunk_size (int, optional): The size of each chunk. Defaults to 4000.

    Returns:
        List[dict]: A list of dictionaries containing the generated questions and answers for each chunk.
                   Each dictionary has the keys 'question' and 'answer'.
    """
    text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    all_responses = []
    for chunk in tqdm(text_chunks, desc="Processing chunks", unit="chunk"):
        response = generate_questions_answers(chunk)
        if 'question' in response and 'answer' in response:
            all_responses.append({'question': response['question'], 'answer': response['answer']})
    return all_responses

import csv

def convert_json_to_csv(file):
    """
    Converts a JSON file containing responses to a CSV file.

    Reads the 'responses.json' file, extracts the 'question' and 'answer' fields from each response,
    and writes them to a new CSV file named 'responses.csv'. The 'prompt' field is set to a predefined
    instruction about answering questions related to cybersecurity standard.

    Args:
        None

    Returns:
        None
    """

    # Prompt the user to enter the instruction for the dataset
    instruction = input("Enter the instruction for the dataset: ")
    #instruction = "You will answer questions about cybersecurity standard"

    with open(file + '.json', 'r', encoding='utf-8') as f:
        responses = json.load(f)

    with open(file+ '.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['prompt', 'question', 'answer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for response in responses['responses']:
            if 'question' in response and 'answer' in response:
                writer.writerow({'prompt': instruction, 'question': response['question'], 'answer': response['answer']})

# Seek for PDF inputs directory and print error if not found
if not os.path.exists('inputs'):
    print("The 'inputs' directory is not found. Please create a directory named 'inputs' and place the PDF, Execel, Word files in it.")
    exit()

# Change the current working directory to the directory where the PDF files are located
os.chdir('inputs') 

# List all the files in the directory
files = os.listdir()

# Filter files with only PDF, Excel, and Word extensions
files = [file for file in files if file.endswith('.pdf') or file.endswith('.xlsx') or file.endswith('.docx')]
print(files)

# Create an output directory
if not os.path.exists('outputs'):
    os.makedirs('outputs')

# Create a subdirectory for each PDF file (without the extension)
for file in files:
    if file.endswith('.pdf'):
        directory = file.replace('.pdf', '')
    elif file.endswith('.xlsx'):
        directory = file.replace('.xlsx', '')
    elif file.endswith('.docx'):
        directory = file.replace('.docx', '')
    elif file.endswith('.csv'):
        directory = file.replace('.csv', '')

    if not os.path.exists(f'output/{directory}'):
        os.makedirs(f'output/{directory}')

# Extract text from PDF, Excel, and Word files
for file in files:
    if file.endswith('.pdf'):
        text = extract_text_from_pdf(file)
    elif file.endswith('.xlsx'):
        text = extract_text_from_excel(file)
    elif file.endswith('.docx'):
        text = extract_text_from_word(file)
    elif file.endswith('.csv'):
        text = extract_text_from_csv(file)

    print(f"Extracted text from {file} with a length of {len(text)} characters.")

    # Process the text to generate questions and answers
    responses = {"responses": process_text(text)}
    
    extensions = ['.pdf', '.docx', '.txt']

    # Save the responses to a JSON file and convert it to a CSV file
    for ext in extensions:
        if file.endswith(ext):
            with open(file.replace(ext, '.json'), 'w') as f:
                json.dump(responses, f, indent=2)
            convert_json_to_csv(file.replace(ext, ''))
            print(f"Generated dataset for {file} and saved as {file.replace(ext, '.csv')}")
            
            # Move the JSON and CSV files into the output directory
            os.rename(file.replace(ext, '.json'), f'outputs/{file}/{file.replace(ext, ".json")}')
            os.rename(file.replace(ext, '.csv'), f'outputs/{file}/{file.replace(ext, ".csv")}')
