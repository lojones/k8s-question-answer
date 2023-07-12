import unittest
from unittest.mock import patch, Mock
import create_embedding

class TestCreateEmbedding(unittest.TestCase):
    def setUp(self) -> None:
        api_key = "sk-1234567890"
        self.embedding_creator = create_embedding.EmbeddingCreator("testdata\\preprocessor\\test.json", api_key)
        self.embedding_creator.output_file = "testdata\\preprocessor\\test-output-data-with-embeddings.json.json"

    def test_load_data(self):
        self.embedding_creator.load_data()
        self.assertEqual(len(self.embedding_creator.data), 4)

    @patch("create_embedding.openai.Embedding.create")
    def test_create_embedding(self, mock_create):
        mock_create.return_value = {"data": [
                                {"embedding": [1,2,3]},
                                {"embedding": [1,2,3]},
                                {"embedding": [1,2,3]},
                                {"embedding": [1,2,3]}]}

        self.embedding_creator.create_embedding()
        self.assertEqual(len(self.embedding_creator.data), 4)
        for i in range(0,4):
            self.assertEqual(self.embedding_creator.data.loc[i]["embedding"], [1, 2, 3])

if __name__ == '__main__':
    unittest.main(exit=False)                