Document Insights Generator
The Document Insights Generator is a Python package that uses natural language processing (NLP) techniques to extract valuable insights from text documents. The tool supports PDF and Word (.docx) documents.

Features
Text extraction from PDF and DOCX documents.
Keyword extraction using TF-IDF.
Named Entity Recognition (NER) using dslim/bert-base-NER transformer model.
Topic modeling using Latent Dirichlet Allocation (LDA).
Answers questions about the document content using GPT-2 model from the OpenAI API.
Provides references based on the document's content.
Installation
You can install the Document Insights Generator from PyPI:

bash
Copy code
pip install documentinsightsgenerator
This will also install the required dependencies.

Usage
Here is a basic example of using the Document Insights Generator:

python
Copy code
from documentinsightsgenerator import DocumentInsightsGenerator

# Initialize the DocumentInsightsGenerator with the API key
dig = DocumentInsightsGenerator(api_key="your-openai-api-key")

# Load a document
dig.load_document("path/to/your/document.pdf")

# Ask a question about the document
answer = dig.answer_question("What is the main topic of the document?")
print(f"Answer: {answer}\n")
For more detailed examples, please refer to the examples directory.

Contributing
We welcome contributions! Please see our contributing guidelines for more details.

License
This project is licensed under the terms of the MIT license. See LICENSE for more information.

