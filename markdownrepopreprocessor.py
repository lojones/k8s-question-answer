import os
import sys
import re
import logging
import tiktoken
import json
import math

class MarkdownRepoPreprocessor:
    def __init__(self, directory) -> None:
        self.directory = directory
        self.files_detail = []
        self.tiktoken_encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        self.skip_files = [ "CONTRIBUTING.md", "LICENSE.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "output\\website-main\\website-main\\content\\en\\docs\\reference\\instrumentation\\metrics.md"]
        self.chunk_max_tokens = 8000
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',    
            datefmt='%Y-%m-%d %H:%M:%S')
        
    def clone_file_detail(self, file_detail):
        # get all keys of file_detail dict
        new_file_detail = {}
        keys = file_detail.keys()
        for key in keys:
            new_file_detail[key] = file_detail[key]
        return new_file_detail

    def num_tokens(self, string: str) -> int:
        """Count the number of tokens in a string."""
        return len(self.tiktoken_encoding.encode(string))    

    def find_title(self, content, filename):
        #search for the first instance of the string "title: " and then get the text after it until the next newline
        title = re.search(r"^title: (.*)$", content, re.MULTILINE)
        if title:
            return title.group(1)
        else:
            title = re.search(r"^# (.*)$", content, re.MULTILINE)
            if title:
                return title.group(1)
            else:
                # convert filename to title and remove .md extension
                return os.path.splitext(os.path.basename(filename))[0].replace("-", " ").replace("_", " ").title()

    def split_string_into_n_parts(self, s, n):
        chars_per_chunk = round(len(s) / n)
        return [s[i:i+chars_per_chunk] for i in range(0, len(s), chars_per_chunk)]

    # method to take a string and split it into n chunks of roughly equal size but the chunks should only be cut at newlines, not in the middle of words
    def split_string(self, s, n, delimiter):
        # Split string by newlines
        lines = s.split(delimiter)

        # Calculate size of each chunk
        chunk_size = len(lines) // n
        remainder = len(lines) % n

        chunks = []
        i = 0

        # Distribute lines among chunks
        for _ in range(n):
            # Start with chunk_size lines for this chunk
            end = i + chunk_size
            # Distribute remainder among first few chunks
            if remainder > 0:
                end += 1
                remainder -= 1
            chunks.append('\n'.join(lines[i:end]))
            i = end

        return chunks

    
    def standardize_length(self, max_tokens):
        self._standardize_length(max_tokens, "\n")
        # check if any element in self.files_detail has more than max_tokens
        for file_detail in self.files_detail:
            if file_detail["token-length"] > max_tokens:
                self._standardize_length(max_tokens, "\n")
                break
        return self.files_detail
        

   

    def _standardize_length(self, max_tokens, delimiter="\n"):
        logging.info(f"Standardizing length to {max_tokens} tokens...")
        if len(self.files_detail) == 0:
            raise Exception("No files to standardize length of. Run preprocess_files_in_directory() first.")
        files_detail = self.files_detail
        new_files_detail = []
        num_files = len(files_detail)
        i = 0
        for file_detail in files_detail:
            i += 1
            logging.info(f"Standardizing length of file {i} of {num_files}...")
            num_tokens = file_detail["token-length"]
            if num_tokens > max_tokens:
                # split into chunks
                required_chunks = round(num_tokens / max_tokens) + 1
                chunks = self.split_string(file_detail["content"], required_chunks, delimiter)
                for chunk in chunks:
                    new_file_detail = self.clone_file_detail(file_detail)
                    new_file_detail["content"] = chunk
                    new_file_detail["token-length"] = self.num_tokens(chunk)
                    new_files_detail.append(new_file_detail)
                filename = file_detail["filepath"]
                num_tokens = file_detail["token-length"]

                logging.info(f"Splitting {filename} into {len(chunks)} chunks, {num_tokens} tokens total")
            else:
                new_files_detail.append(file_detail)
        self.files_detail = new_files_detail
        
        

        return self.files_detail

    def preprocess_files_in_directory(self):
        logging.info(f"Collecting markdown files in {self.directory}...")  
        files_detail = self.files_detail
        dir = self.directory
        self.files_detail = self._preprocess_files_in_directory(dir, files_detail)
        return self.files_detail


    def _preprocess_files_in_directory(self, dir, files_detail):
        logging.info(f"Collecting markdown files in {dir}...")  
        for root, dirs, filenames in os.walk(dir):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                if filename.endswith(".md") and (filename not in self.skip_files and filepath not in self.skip_files):
                    filesize = os.path.getsize(filepath)
                    filecontent = open(filepath, "r", encoding='utf-8', errors='ignore').read()
                    tokens = self.tiktoken_encoding.encode(filecontent)
                    tokenlength = len(tokens)
                    title = self.find_title(filecontent, filename)
                    files_detail.append({ 
                        "filepath": filepath, 
                        "size": filesize, 
                        "title": title,  
                        "content": filecontent, 
                        "token-length": tokenlength })
                    logging.info(f"{filepath} ({(filesize/1024):.2f} kb, {tokenlength} tokens)")
            for dir in dirs:
                self._preprocess_files_in_directory(dir, files_detail)
        return files_detail

    def write_to_pretty_json_file(self, filepath):
        with open(filepath, "w") as f:
            json.dump(self.files_detail, f, indent=4)





