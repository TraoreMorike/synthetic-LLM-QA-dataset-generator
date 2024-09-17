import csv
import json

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
    #instruction = input("Enter the instruction for the dataset: ")
    instruction = "You will answer questions about cybersecurity"

    with open(file + '.json', 'r', encoding='utf-8') as f:
        responses = json.load(f)

    with open(file+ '.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['prompt', 'question', 'answer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for response in responses['responses']:
            if 'question' in response and 'answer' in response:
                writer.writerow({'prompt': instruction, 'question': response['question'], 'answer': response['answer']})
