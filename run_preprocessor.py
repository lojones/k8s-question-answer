import markdownrepopreprocessor
import sys
import logging


# get the directory path from the command line
if len(sys.argv) != 2:
    print("Usage: python run_preprocessor.py <directory>")
    exit(1)

logging.basicConfig(
level=logging.INFO, 
format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',    
datefmt='%Y-%m-%d %H:%M:%S')

directory = sys.argv[1]

logging.info("Starting...")
logging.info(f"Collecting markdown files in {directory}...")

preprocessor = markdownrepopreprocessor.MarkdownRepoPreprocessor(directory)

# get all markdown files in the directory
preprocessor.preprocess_files_in_directory()
preprocessor.standardize_length(8000)
preprocessor.write_to_pretty_json_file("output\\preprocessed_output.json")
