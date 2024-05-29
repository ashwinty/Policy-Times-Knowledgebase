import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_words_from_json(json_content):
    words = []
    if 'results' in json_content and 'channels' in json_content['results']:
        for channel in json_content['results']['channels']:
            if 'alternatives' in channel:
                for alternative in channel['alternatives']:
                    if 'words' in alternative:
                        for word_info in alternative['words']:
                            words.append(word_info['word'])
    return words

def find_json_objects(text):
    json_objects = []
    start_idx = 0
    brace_count = 0
    in_string = False

    for i, char in enumerate(text):
        if char == '"':
            in_string = not in_string
        if in_string:
            continue
        if char == '{':
            if brace_count == 0:
                start_idx = i
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                json_objects.append(text[start_idx:i + 1])
    return json_objects

def save_words_to_file(words, original_filename, output_directory):
    # Join words into a single string with spaces in between
    content = ' '.join(words)
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    # Determine the new file path
    new_file_path = os.path.join(output_directory, original_filename)
    # Write the content to the new file
    with open(new_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def process_files_in_directory(directory_path, output_directory):
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read().strip()
                    json_strings = find_json_objects(file_content)
                    all_words = []
                    for json_str in json_strings:
                        try:
                            json_content = json.loads(json_str)
                            words = extract_words_from_json(json_content)
                            all_words.extend(words)
                        except json.JSONDecodeError as jde:
                            logging.error(f"Error decoding JSON from file: {filename}. Content: {json_str[:1000]}")
                            logging.error(f"JSONDecodeError: {str(jde)}")
                    # Save the extracted words to a new file in the output directory
                    save_words_to_file(all_words, filename, output_directory)
                    logging.info(f"Successfully processed file: {filename}")
            except Exception as e:
                logging.error(f"An unexpected error occurred while processing file {filename}: {str(e)}")

# Set the path to the directory containing the .txt files and the output directory
directory_path = '/Users/ashwintyagi/Desktop/POCs/POC-5/Text'
output_directory = '/Users/ashwintyagi/Desktop/POCs/POC-5/Text2'

# Process the files and save the cleaned words to new files
process_files_in_directory(directory_path, output_directory)
