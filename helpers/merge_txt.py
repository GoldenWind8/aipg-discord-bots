import os

def merge_text_files(directory, output_file):
    # Create or open the output file
    with open(output_file, 'w') as outfile:
        # Iterate over all files in the directory
        for filename in os.listdir(directory):
            # Check if the file is a text file
            if filename.endswith('.txt'):
                # Open the text file
                with open(os.path.join(directory, filename), 'r') as infile:
                    # Read the file's content and write it to the output file
                    outfile.write(infile.read())
                    # Optionally, write a newline after each file's content
                    outfile.write('\n')

# Usage example
directory_path = '../aipg_docs'
output_file_path = 'aipg.txt'
merge_text_files(directory_path, output_file_path)
