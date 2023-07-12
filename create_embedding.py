import pandas as pd
import openai
import logging
import tiktoken
import json

class EmbeddingCreator:
    def __init__(self, datafile, openai_api_key) -> None:
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',    
            datefmt='%Y-%m-%d %H:%M:%S')
        self.datafile = datafile
        self.embedding_model = "text-embedding-ada-002"
        self.output_file = "output\\data-with-embeddings.json"
        openai.api_key = openai_api_key


    def list_models(self):
        logging.info("Listing models")        
        logging.info(openai.Engine.list())
        
    def load_data(self):
        logging.info("Loading data")
        self.data = pd.read_json(self.datafile, orient="records")
        logging.info("Data loaded")

    def write_to_pretty_json_file(self, filepath, jsondata):
        logging.info(f"Writing to {filepath}")
        with open(filepath, "w") as f:
            json.dump(jsondata, f, indent=4)

    # a function that returns true if the openain.Embedding.create() call returned a valid set of embeddings in its response (response["data"][0]["embedding"])
    def is_valid_embedding(self, response):
        return (response is not None) and ("data" in response) and (len(response["data"]) > 0) and ("embedding" in response["data"][0]) and (len(response["data"][0]["embedding"]) > 0)

    # a function that takes a dataframe and returns a json object oriented as a dict (table)
    def dataframe_to_json(self, df):
        return json.loads(df.to_json(orient="table"))

    def create_embedding(self):
        print("Creating embedding")        
        self.load_data()
        embeddings_list = {}
        first_in_batch_index = 0
        last_row_index = len(self.data) - 1
        input = []
        for index,row in self.data.iterrows():
            title = row["title"]
            filename = row["filepath"]
            tokenlen = row["token-length"]
            logging.info(f"{index} of {last_row_index} Creating content batch with content for title: {title} - {tokenlen} - {filename}")
            input.append(row["content"])
            embeddings_list[index] = []
            if ((index + 1) % 100 == 0) or (index == last_row_index):
                logging.info(f"Creating embeddings for {first_in_batch_index} - {index}")
                response = openai.Embedding.create(model=self.embedding_model, input=input)
                if self.is_valid_embedding(response):
                    num_embeddings = len(response["data"])
                    for i in range(0,num_embeddings):
                        embedding_response = response["data"][i]["embedding"]
                        embeddings_list[first_in_batch_index+i] = embedding_response
                    logging.info(f"got valid response and added {i+1} embeddings")
                else:
                    logging.error(f"Error creating embedding for {title} - {tokenlen}")
                input = []
                first_in_batch_index = index + 1
        self.data["embedding"] = pd.Series(embeddings_list)
        json_data = self.dataframe_to_json(self.data)
        self.write_to_pretty_json_file(self.output_file, json_data)
            


    
     