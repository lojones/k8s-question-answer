import pandas as pd
import openai
import logging
import tiktoken

class EmbeddingCreator:
    def __init__(self, datafile, openai_api_key) -> None:
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',    
            datefmt='%Y-%m-%d %H:%M:%S')
        self.datafile = datafile
        self.embedding_model = "text-embedding-ada-002"
        openai.api_key = openai_api_key

    def list_models(self):
        logging.info("Listing models")        
        logging.info(openai.Engine.list())
        
    def load_data(self):
        logging.info("Loading data")
        self.data = pd.read_json(self.datafile, orient="records")
        logging.info("Data loaded")

    def create_embedding(self):
        print("Creating embedding")        
        self.load_data()
        for index,row in self.data.iterrows():
            if "chunks" in row:
                input = row["chunks"]
            else:
                input = row["content"]
            response = openai.Embedding.create(model=self.embedding_model, input=input)
            logging.info("got response")


    
     