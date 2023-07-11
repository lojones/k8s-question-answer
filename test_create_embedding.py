import unittest
import create_embedding

class TestCreateEmbedding(unittest.TestCase):
    def setUp(self) -> None:
        api_key = ""
        self.embedding_creator = create_embedding.EmbeddingCreator("testdata\\preprocessor\\test.json", api_key)

if __name__ == '__main__':
    unittest.main(exit=False)                