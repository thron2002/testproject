import re

def split_and_store_sas_code(sas_code):
    # Define patterns for start and end of logical chunks
    start_patterns = [
        r'^\s*data\s+\w+;',  # Data steps
        r'^\s*proc\s+\w+;',  # Procedures
        r'^\s*%macro\s+\w+\s*\([^)]*\);',  # Macro definitions
    ]

    end_patterns = [
        r'^\s*%mend\s*\w*;',  # Macro end
        r'^\s*run\s*;',  # Run statements
        r'^\s*quit\s*;',  # Quit statements
    ]

    # Comment pattern
    comment_pattern = re.compile(r'^\s*\*.*?;')  # Single-line comments

    # Compile patterns
    start_combined_pattern = re.compile('|'.join(start_patterns), re.IGNORECASE)
    end_combined_pattern = re.compile('|'.join(end_patterns), re.IGNORECASE)

    chunks = []
    current_chunk = []

    lines = sas_code.splitlines()

    for line in lines:

        # Check if line matches end patterns
        if end_combined_pattern.match(line):
            current_chunk.append(line)
            chunks.append("\n".join(current_chunk).strip())
            current_chunk = []
        # Check if line matches start patterns and current chunk is not empty
        elif start_combined_pattern.match(line):
            if current_chunk:
                current_chunk.append(line)

            else:
                current_chunk = [line]

        else:
            current_chunk.append(line)

    # Add any remaining lines as the last chunk
    if current_chunk:
        chunks.append("\n".join(current_chunk).strip())

    # Store chunks in a dictionary
    chunk_dict = {f"Chunk {i}": chunk for i, chunk in enumerate(chunks, 1)}
    return chunk_dict

def read_sas_file(file_path):
    with open(file_path, 'r') as file:
        sas_code = file.read()
    return sas_code

if __name__ == "__main__":
    # Specify the path to your SAS file
    file_path = 'example_copy.sas'
    
    # Read the SAS code from the file
    sas_code = read_sas_file(file_path)
    
    # Split the SAS code into logical chunks and store in a dictionary
    chunk_dict = split_and_store_sas_code(sas_code)
    
    # Print each chunk from the dictionary
    for key, chunk in chunk_dict.items():
        print(f"{key}:\n{chunk}\n{'-'*40}")
