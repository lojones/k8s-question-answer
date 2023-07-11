import unittest
import create_embedding

class TestCreateEmbedding(unittest.TestCase):
    def setUp(self) -> None:
        api_key = ""
        self.embedding_creator = create_embedding.EmbeddingCreator("testdata\\preprocessor\\test.json", api_key)

    def test_list_models(self):
        self.embedding_creator.list_models()

    def test_load_data(self):
        self.embedding_creator.load_data()
        self.assertEqual(len(self.embedding_creator.data), 2)

    def test_create_embedding(self):
        self.embedding_creator.create_embedding()
        self.assertEqual(len(self.embedding_creator.data), 2)

if __name__ == '__main__':
    unittest.main(exit=False)                