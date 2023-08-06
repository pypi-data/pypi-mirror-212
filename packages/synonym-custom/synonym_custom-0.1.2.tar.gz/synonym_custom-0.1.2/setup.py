from setuptools import setup
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(

    name='synonym_custom',
    version='0.1.2',
    packages=['synonym_custom'],
    author="Sandeep Chataut",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'openai==0.27.7',
        'requests==2.28.1',
        'spacy==3.5.3',
        'spacy-wordnet==0.1.0',
        'python-dotenv==1.0.0',
        'nltk==3.5',
        'transformers==4.29.2',
        'beautifulsoup4==4.11.1',
    ],
    python_requires='>=3.8',
    
)