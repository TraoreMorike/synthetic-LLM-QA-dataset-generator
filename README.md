
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

1. Run the script in the command line: `synth-openai.py`
2. The script will extract text from all PDF, Excel, and Word files in the "inputs" directory.
3. It will process the extracted text to generate questions and answers for each file.
4. The generated responses will be saved in JSON format and converted to CSV.
5. The output files (JSON and CSV) will be moved to an "outputs" directory with subdirectories for each input file.

 ## Notes:

* Make sure to have the required libraries installed in your Python environment.
* This script assumes that all input files are in the same directory as the script. You may need to modify the script if you want to process files from different directories.
* The generated questions and answers are based on the text content of each file, so the quality of the output depends on the quality of the extracted text and the model selected.

  ## TODO :
* Use argparse to easily select LLM model,tuning parameter and chunk size.
* Use arparse to pass OpenAI api key.
* Add license (currently MIT).

**License:**
TODO
