import unittest
import markdownrepopreprocessor
import os

class TestMarkdownRepoPreprocessor(unittest.TestCase):
    def setUp(self) -> None:
        self.preprocessor = markdownrepopreprocessor.MarkdownRepoPreprocessor("testdata\\preprocessor")
    def test_split_string_into_parts(self):
        self.assertEqual(self.preprocessor.split_string_into_n_parts("123456789", 3), ["123", "456", "789"])
        self.assertEqual(self.preprocessor.split_string_into_n_parts("123456789", 5), ["12", "34", "56","78","9"])
        self.assertEqual(self.preprocessor.split_string_into_n_parts("The quick brown fox jumped", 6), ['The ', 'quic', 'k br', 'own ', 'fox ', 'jump', 'ed'])
    def test_preprocess_files_in_directory(self):
        files = self.preprocessor.preprocess_files_in_directory()
        self.assertAlmostEqual(len(files), 2)
    def test_standardize_length(self):
        files = self.preprocessor.preprocess_files_in_directory()
        files = self.preprocessor.standardize_length(8000)
        self.assertEqual(len(files[0]["chunks"]), 2)
    def test_write_to_pretty_json(self):
        files = self.preprocessor.preprocess_files_in_directory()
        files = self.preprocessor.standardize_length(8000)
        self.preprocessor.write_to_pretty_json_file("testdata\\preprocessor\\test.json")
        self.assertTrue(os.path.isfile("testdata\\preprocessor\\test.json"))
        

if __name__ == '__main__':
    unittest.main(exit=False)        