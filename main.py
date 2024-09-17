import os
import json
import ollama

from extractors_func import *
from json_to_csv import convert_json_to_csv 

from openai import OpenAI
from dotenv import load_dotenv

from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import ProgressBar, radiolist_dialog

template =  {
    "question": " ",
    "answer": " "
}

def call_openai_api(model, messages, max_tokens=2048, temperature=1):
    """
    Calls the OpenAI API with the given parameters.

    Args:
        model (str): The model to use.
        messages (list): The messages to send.
        max_tokens (int): The maximum number of tokens.
        temperature (float): The temperature for the response.

    Returns:
        str: The response text from the API.
    """

    client = OpenAI(
        base_url = os.getenv("OPENAI_API_BASE_URL"),
        api_key= os.getenv("OPENAI_API_KEY"), 
    )

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()

def fix_json(crptd_json, fix_model):
    """
    Fixes a corrupted JSON string by calling the OpenAI API.

    Args:
        crptd_json (str): The corrupted JSON string.

    Returns:
        dict: The fixed JSON data.
    """
    messages = [
        {'role': 'system', 'content': f'You are an API that converts the wrongly formatted JSON into a properly formatted one by following this template: {template}. Only respond with the JSON and no additional text.\n.'},
        {'role': 'user', 'content': 'Wrong JSON: ' + crptd_json}
    ]

    response_text = call_openai_api(fix_model, messages)
    
    try:
        json_data = json.loads(response_text)
        print(json_data)
        return json_data
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        print("The JSON is not valid, reformatting again.")
        return fix_json(crptd_json, fix_model)  # Recursively call fix_json to try again

def generate_questions_answers(text_chunk, qa_model, fix_model):
    """
    Generates questions and answers from a text chunk by calling the OpenAI API.

    Args:
        text_chunk (str): The text chunk to process.

    Returns:
        dict: The generated questions and answers in JSON format.
    """
    messages = [
        {'role': 'system', 'content': 'You are an API that converts bodies of text into a single question and answer into a JSON format. Each JSON should contain a single question with a single answer. Only respond with the JSON and no additional text.\n.'},
        {'role': 'user', 'content': 'Text: ' + text_chunk}
    ]

    response_text = call_openai_api(qa_model, messages, temperature=0.7)
    
    try:
        json_data = json.loads(response_text)
        print(json_data)
        return json_data
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        print("The JSON is not valid, reformatting again.")
        return fix_json(response_text, fix_model)  # Pass the response_text to fix_json

from typing import List

from prompt_toolkit.shortcuts import ProgressBar

from tqdm import tqdm
from typing import List

def process_text(text: str, qa_model: str, fix_model: str, chunk_size: int = 4000) -> List[dict]:
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

    for chunk in tqdm(text_chunks, desc="Processing chunks"):
        response = generate_questions_answers(chunk, qa_model, fix_model)
        if 'question' in response and 'answer' in response:
            all_responses.append({'question': response['question'], 'answer': response['answer']})
    
    return all_responses

"""
# Seek for inputs directory and print error if not found
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
"""

def create_output_directories(files):
    """
    Creates output directories for each file type.
    """
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

from prompt_toolkit.shortcuts import ProgressBar

def extract_text(files, qa_model, fix_model):
    """
    Extracts text from various file types.
    """
    with ProgressBar() as pb:
        for file in pb(files, label="Processing files"):
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
            responses = {"responses": process_text(text, qa_model, fix_model)}
            
            extensions = ['.pdf', '.docx', '.txt', '.csv', '.xlsx']

            # Save the responses to a JSON file and convert it to a CSV file
            for ext in extensions:
                if file.endswith(ext):
                    with open(file.replace(ext, '.json'), 'w') as f:
                        json.dump(responses, f, indent=2)
                    
                    convert_json_to_csv(file.replace(ext, ''))
                    # Move the JSON and CSV files into the output directory
                    os.rename(file.replace(ext, '.json'), f'output/{file.replace(ext, "")}/{file.replace(ext, ".json")}')
                    os.rename(file.replace(ext, '.csv'), f'output/{file.replace(ext, "")}/{file.replace(ext, ".csv")}')

def main():
    
    # Load API key environment variables from the .env file
    load_dotenv()

    # Seek for inputs directory and print error if not found
    if not os.path.exists('docs'):
        print("The 'input' directory is not found. Please create a directory named 'docs' and place the PDF, Execel, Word files in it.")
        exit()
    
    # Change the current working directory to the directory where the files are located
    os.chdir('docs')

    # Seek only supported extensions in the directory
    files = [file for file in os.listdir() if file.endswith('.pdf') or file.endswith('.xlsx') or file.endswith('.docx') or file.endswith('.csv')]

    # Beautifully the list of files
    print("Found :", files ,"in docs directory")

    available_models = ollama.list()

    # Get only the name from the REST API response
    available_models = [model['name'] for model in available_models['models']]
    print("Available models: ", available_models)
    


    # Prompt the user to select the model for Q&A generation
    qa_model = radiolist_dialog(
        title="Select Model",
        text="Please select the model to use for Q&A generation:",
        values=[(model, model) for model in available_models]
    ).run()

    if qa_model is None:
        print("No model selected. Exiting.")
        exit()
    
    # Prompt the user to select the model for fixing JSON
    fix_model = radiolist_dialog(
        title="Select Model",
        text="Please select the model to use for JSON fixing:",
        values=[(model, model) for model in available_models]
    ).run()

    if fix_model is None:
        print("No model selected. Exiting.")
        exit()
    
    # Create subdirectories for each file
    create_output_directories(files)

    # Extract text and process files
    extract_text(files, qa_model, fix_model)

if __name__ == "__main__":      
    main()