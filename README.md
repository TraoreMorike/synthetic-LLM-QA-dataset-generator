
# OLLAMA Question-Answer Dataset Generator

This script is designed to process text from various file formats (PDF, Excel, Word) and generate questions and answers based on the extracted text. The output is saved in JSON format and converted to CSV.

## Features:

* Extracts text from PDF, Excel, and Word files using their respective libraries.
* Processes the extracted text by splitting it into chunks and generating questions and answers for each chunk.
* Saves the responses in a JSON file and converts it to a CSV file.
* Moves the generated JSON and CSV files to an output directory.

## Requirements:

* Ollama already installed and running 
* Python 3.x
* OpenAI library (for processing text)
* tqdm library (for progress bar)
* csv library (for writing CSV files)
* python_docx (for parsing word documents)
* PyPDF2 (for parsing PDF documents)
* pandas (for parsing Excel and CSV documents)

Install dependencies :
`pip install -r requirements.txt`

 ## Usage :

1. If not already done, create a .env file to add you OPENAI API key and base url.
```sh
# .env file

# Setup your OpenAI API key and base URL HERE :
# You can get your API key from https://platform.openai.com/account/api-keys
# You can get your base URL from https://platform.openai.com/docs/guides/quickstart

# CAUTION : YOUR API KEY IS A SECRET. DO NOT SHARE IT WITH ANYONE.

# When using Ollama locally, you can use the following default values :
OPENAI_API_KEY="ollama"
OPENAI_API_BASE_URL="http://localhost:11434/v1"
```
2. Run the script in the command line: `main.py`
2. The script will extract text from all PDF, Excel, and Word files in the "docs" directory.
3. It will process the extracted text to generate questions and answers for each file.
4. The generated responses will be saved in JSON format and converted to CSV.
5. The output files (JSON and CSV) will be moved to an "output" directory with subdirectories for each input file.

 ## Notes:

* Make sure to have the required libraries installed in your Python environment.
* This script assumes that all input files are in the same directory as the script. You may need to modify the script if you want to process files from different directories.
* The generated questions and answers are based on the text content of each file, so the quality of the output depends on the quality of the extracted text and the model selected.

**License:**
MIT License
