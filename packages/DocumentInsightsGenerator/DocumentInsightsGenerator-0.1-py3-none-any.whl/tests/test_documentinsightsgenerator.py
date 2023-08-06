import unittest
from unittest.mock import patch, MagicMock
from DocumentInsightsGenerator.documentinsightsgenerator import DocumentInsightsGenerator

class TestDocumentInsightsGenerator(unittest.TestCase):
    
    def setUp(self):
        self.dig = DocumentInsightsGenerator(api_key="your_api_key") 

    def test_load_pdf(self):
        # Let's assume 'sample.pdf' is a simple PDF file located in the same directory as this test.
        self.dig.load_document('sample.pdf')

        # You could check if some known content from the 'sample.pdf' file exists in 'self.dig.doc_text'.
        self.assertIn("expected content", self.dig.doc_text)

    @patch('docx2txt.process')
    def test_load_word_doc(self, mock_process):
        # Mock the 'process' method from 'docx2txt' to return a known string.
        mock_process.return_value = "expected content"
        
        self.dig.load_document('sample.docx')
        
        # Check if 'doc_text' is the string we have set in the mock method.
        self.assertEqual(self.dig.doc_text, "expected content")

    def test_load_document_unsupported_format(self):
        with self.assertRaises(ValueError):
            self.dig.load_document('unsupported_format.txt')

    def test_generate_insights(self):
        # Load a known document
        self.dig.load_document('sample.pdf')

        # Generate insights
        self.dig.generate_insights()

        # As it's complicated to know the exact outcome (it depends on the model used and the document content),
        # it's good enough to test if 'insights' is not empty.
        self.assertTrue(self.dig.insights)

    @patch('requests.post')
    def test_answer_question(self, mock_post):
        # Mock the 'post' method from 'requests' to return a Mock object with a known 'json' method.
        mock_post.return_value.json.return_value = {
            'choices': [{'text': 'Expected answer'}]
        }
        mock_post.return_value.status_code = 200

        self.dig.doc_text = 'document text'
        answer = self.dig.answer_question('What is the document about?')

        # Check if the answer is the one we have set in the mock method.
        self.assertEqual(answer, 'Expected answer')

    @patch('requests.post')
    def test_answer_question_error_response(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {
            'error': {
                'message': 'Error message from API'
            }
        }

        self.dig.doc_text = 'document text'
        answer = self.dig.answer_question('What is the document about?')

        self.assertIsNone(answer)

    def test_find_page_number(self):
        self.dig.doc_text = "Page 1\n\n\nPage 2\n\n\nPage 3"
        page_number = self.dig.find_page_number("Page 2")

        self.assertEqual(page_number, 2)

    def test_find_nearest_heading(self):
        self.dig.doc_text = "Page 1\n\n\nPage 2\n\n\nPage 3"

        with patch.object(self.dig, "get_page_text") as mock_get_page_text:
            mock_get_page_text.return_value = [
                {"text": "Some text"},
                {"text": "Expected heading"},
                {"text": "Other text"}
            ]

            heading = self.dig.find_nearest_heading(2)

            self.assertEqual(heading, "Expected heading")

    def test_extract_document_info(self):
        self.dig.doc_text = "Page 1\n\n\nPage 2\n\n\nPage 3"

        # Mock the 'find_nearest_heading' method
        with patch.object(self.dig, "find_nearest_heading") as mock_find_nearest_heading:
            mock_find_nearest_heading.side_effect = ["Expected title", "Expected author", "Expected purpose"]

            # Mock 'find_key_points', 'generate_summary' and 'find_references' methods
            with patch.object(self.dig, "find_key_points") as mock_find_key_points, \
                 patch.object(self.dig, "generate_summary") as mock_generate_summary, \
                 patch.object(self.dig, "find_references") as mock_find_references:
                mock_find_key_points.return_value = ["Key point 1", "Key point 2"]
                mock_generate_summary.return_value = "Expected summary"
                mock_find_references.return_value = ["Reference 1", "Reference 2"]

                info = self.dig.extract_document_info()

                # Verify the results
                expected_info = {
                    'Title': 'Expected title',
                    'Author': 'Expected author',
                    'Purpose': 'Expected purpose',
                    'Key Points': ['Key point 1', 'Key point 2'],
                    'Summary': 'Expected summary',
                    'References': ['Reference 1', 'Reference 2']
                }
                self.assertEqual(info, expected_info)

    def test_get_page_text(self):
        with patch('pdfplumber.open') as mock_pdfplumber_open:
            mock_pdfplumber_open.return_value.__enter__.return_value.pages = [
                MagicMock(), MagicMock()
            ]
            mock_pdfplumber_open.return_value.__enter__.return_value.pages[0].extract_words.return_value = 'Expected words'
            
            self.dig.doc_text = "Some bytes"
            result = self.dig.get_page_text(1)

            self.assertEqual(result, 'Expected words')

    def test_find_references(self):
        self.dig.doc_text = 'Sample document text'
        with patch.object(self.dig, "find_reference") as mock_find_reference:
            mock_find_reference.side_effect = ["Page 1, Section: Introduction", "Page 2, Section: Conclusion"]

            references = self.dig.find_references()

            self.assertEqual(references, ["Page 1, Section: Introduction", "Page 2, Section: Conclusion"])


if __name__ == "__main__":
    unittest.main()
