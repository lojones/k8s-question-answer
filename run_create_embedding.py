import create_embedding
import sys
import logging


# get the directory path from the command line
if len(sys.argv) != 3:
    print("Usage: python run_create_embedding.py <filepath> <openai-api-key>")
    exit(1)

logging.basicConfig(
level=logging.INFO, 
format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',    
datefmt='%Y-%m-%d %H:%M:%S')

filepath = sys.argv[1]
openai_api_key = sys.argv[2]

logging.info("Starting...")
logging.info(f"Getting embeddings for this dataset: {filepath}...")

embeddingcreator = create_embedding.EmbeddingCreator(filepath, openai_api_key)

embeddingcreator.create_embedding()

logging.info("Done.")
