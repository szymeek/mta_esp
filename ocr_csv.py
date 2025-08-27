import csv
import os

def append_ocr_result_to_csv(cycle_number, position, character, confidence):
    filename = 'ocr_results.csv'
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['cycle', 'position', 'character', 'confidence']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header if file doesn't exist
        if not file_exists:
            writer.writeheader()
        
        # Append the OCR result
        writer.writerow({
            'cycle': cycle_number,
            'position': position,
            'character': character,
            'confidence': confidence
        })
