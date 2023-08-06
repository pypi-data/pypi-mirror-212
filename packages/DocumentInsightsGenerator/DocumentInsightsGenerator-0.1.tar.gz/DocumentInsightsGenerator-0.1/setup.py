from setuptools import setup, find_packages

setup(
    name='DocumentInsightsGenerator',
    version='0.1',
    description='A package to generate comprehensive insights from documents using NLP techniques.',
    long_description=open('README.md').read(),
    url='https://github.com/pritiyadav888/DocumentInsightsGenerator',
    author='Priti Yadav',
    author_email='yadavpriti0210@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'spacy', 
        'requests', 
        'transformers', 
        'scikit-learn',
        'pdfplumber',
        'pytesseract', 
        'pdfminer.six', 
        'Pillow', 
        'docx2txt',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)
