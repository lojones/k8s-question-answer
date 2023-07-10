import os
import sys
import re
import logging
import tiktoken


logging.basicConfig(level=logging.INFO)
tiktoken_encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
total_files = 0
total_filesize = 0
total_tokens = 0
biggest_token_length = 0
biggest_token_length_file = ""
skip_files = [ "CONTRIBUTING.md", "LICENSE.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "output\\website-main\\website-main\\content\\en\\docs\\reference\\instrumentation\\metrics.md"]

# get the directory path from the command line
if len(sys.argv) != 2:
    print("Usage: python preprocess-data.py <directory>")
    exit(1)

directory = sys.argv[1]

def add_files_in_directory(dir, files_detail):
    global total_files
    global total_filesize
    global total_tokens
    global biggest_token_length
    global biggest_token_length_file
    logging.info(f"Collecting markdown files in {dir}...")  
    for root, dirs, filenames in os.walk(dir):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            if filename.endswith(".md") and (filename not in skip_files and filepath not in skip_files):
                filesize = os.path.getsize(filepath)
                filecontent = open(filepath, "r", encoding='utf-8', errors='ignore').read()
                tokens = tiktoken_encoding.encode(filecontent)
                tokenlength = len(tokens)
                files_detail[filepath] = { "size": filesize, "content": filecontent, "tokens": tokens, "token-length": tokenlength }
                logging.info(f"{filepath} ({(filesize/1024):.2f} kb, {tokenlength} tokens)")
                total_files += 1
                total_filesize += filesize
                total_tokens += tokenlength
                if tokenlength > biggest_token_length:
                    biggest_token_length = tokenlength
                    biggest_token_length_file = filepath
        for dir in dirs:
            add_files_in_directory(dir, files_detail)

logging.info("Starting...")
logging.info(f"Collecting markdown files in {directory}...")

# get all markdown files in the directory
files_detail = {}
add_files_in_directory(directory, files_detail)
print(f"Totals: {total_files} files, {(total_filesize/1024):.2f} kb, {total_tokens} tokens, biggest token length: {biggest_token_length} for {biggest_token_length_file}")
