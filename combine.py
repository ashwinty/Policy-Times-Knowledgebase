import os
import csv

# Function to read content from a txt file
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to get all txt files in a folder
def get_txt_files(folder_path):
    txt_files = []
    for file in os.listdir(folder_path):
        if file.endswith('.txt'):
            txt_files.append(file)
    return txt_files

# Folder path containing txt files
folder_path = '/Users/ashwintyagi/Desktop/POCs/POC-5/Text2'

# Output CSV file path
output_csv_file = 'output.csv'

# Write data to CSV
with open(output_csv_file, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['name', 'content', 'link', 'date'])
    
    txt_files = get_txt_files(folder_path)
    for txt_file in txt_files:
        file_name = os.path.splitext(txt_file)[0]
        file_path = os.path.join(folder_path, txt_file)
        content = read_txt_file(file_path)
        writer.writerow([file_name, content, ''])
