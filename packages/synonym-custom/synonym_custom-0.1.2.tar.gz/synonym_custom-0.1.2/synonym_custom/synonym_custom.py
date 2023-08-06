#!/usr/bin/env python

import os
import openai
import requests
from bs4 import BeautifulSoup
import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from dotenv import load_dotenv

load_dotenv()  
from transformers import (
    TokenClassificationPipeline,
    AutoModelForTokenClassification,
    AutoTokenizer,
)
from transformers.pipelines import AggregationStrategy
import numpy as np

nlp = spacy.load('en_core_web_sm')


class Synonym_Generator():
    def __init__(self, api_key=None):
        openai.api_key = api_key

    
    def setOpenApiKey(self,api_key):
        openai.api_key= api_key
    
    def dictionary_syn(self, word): #using dictionary to generate synonyms
        url = "https://www.thesaurus.com/browse/" + word
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        synonyms = []
        synonym_tags = soup.find_all("a", {"class": ["css-1kg1yv8 eh475bn0", "css-1n6g4vv eh475bn0"]})

        for tag in synonym_tags:
            synonym = tag.text.strip()
            synonyms.append(synonym)

        return synonyms
    
    def spacy_syn(self, word): #using spacy to generate synonyms
        nlp = spacy.load('en_core_web_sm')
        nlp.add_pipe(WordnetAnnotator(nlp.lang), after='tagger')
        token = nlp(word)[0]

        if token.pos_ == 'NOUN':
            pos = 'n'
        elif token.pos_ == 'VERB':
            pos = 'v'
        elif token.pos_ == 'ADJ':
            pos = 'a'
        elif token.pos_ == 'ADV':
            pos = 'r'
        else:
            return []

        synonyms = []
        for syn in token._.wordnet.synsets():
            for lemma in syn.lemma_names():
                if lemma != word:
                    synonyms.append(lemma)

        return synonyms

    def openai_api(self, input_sentence, target_words):   #using openai to generate synonyms
        synonyms_list = []

        for target_word in target_words:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Generate 5 synonyms for the word '{target_word}' in the sentence: '{input_sentence}'",
                max_tokens=50,
                temperature=0.6,
                stop=None,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                best_of=1,
            )

            synonyms = response.choices[0].text.strip().split("\n")
            synonyms_list.extend(synonyms)
        
        return synonyms_list
    
    def extract_keywords_openai(self, text):   #using openai to generate keywords
        prompt = f"Extract the keywords from the following text:\n\n{text}\n\nKeywords:"

        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            temperature=0.5,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.8,
            presence_penalty=0.0,
            seed=42
        )

        keywords = response.choices[0].text.strip().split(',')
        keyphrases = [phrase.strip() for phrase in keywords][:15]
        
        return keyphrases
    def extract_keywords_spacy(self, sentence):    #using spacy to generate keywords
        doc = nlp(sentence)
        keywords = []
        seen_keywords = set()
    
        for token in doc:
            if token.is_stop or token.is_punct:
                continue
            if token.pos_ in ['NOUN', 'PROPN', 'VERB', 'ADJ'] and token.lemma_ not in seen_keywords:
                keywords.append(token.lemma_)
                seen_keywords.add(token.lemma_)
    
        return keywords
    def extract_keywords_nltk(self, sentence):     #using nltk to generate keywords
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(sentence)
        keywords = []
        seen_keywords = set()

        pos_tags = pos_tag(tokens)  # Perform POS tagging

        for token, tag in pos_tags:
            token_lower = token.lower()
            if (
                token_lower not in stop_words
                and token_lower not in seen_keywords
                and token_lower != 'although'
                and tag != 'CC'
                and token.isalpha()  # Exclude tokens that are not alphabetic
            ):
                keywords.append(token_lower)
                seen_keywords.add(token_lower)

        return keywords
    def extract_keywords_trans(self, text):    #using transformer to generate keywords
        model_name = "ml6team/keyphrase-extraction-kbir-inspec"
        # Load model and tokenizer
        model = AutoModelForTokenClassification.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Define keyphrase extraction pipeline
        extractor = TokenClassificationPipeline(
            model=model,
            tokenizer=tokenizer,
            framework="pt",  # Optional: Specify the framework (e.g., "pt" for PyTorch) if needed
        )

        # Perform keyphrase extraction
        keyphrases = extractor(
            text,
            aggregation_strategy=AggregationStrategy.SIMPLE,
              # Optional: Adjust the maximum length if needed
        )

        # Extract and format keyphrases
        keyphrases = np.unique([result.get("word").strip() for result in keyphrases])[:15]

        return keyphrases


# if __name__ == "__main__":
#     text = "Although biofilms have been observed early in the history of microbial research, their impact has only recently been fully recognized. Biofilm infections, which contribute to up to 80% of human microbial infections, are associated with common human disorders, such as diabetes mellitus and poor dental hygiene, but also with medical implants. The associated chronic infections such as wound infections, dental caries and periodontitis significantly enhance morbidity, affect quality of life and can aid development of follow-up diseases such as cancer. Biofilm infections remain challenging to treat and antibiotic monotherapy is often insufficient, although some rediscovered traditional compounds have shown surprising efficiency. Innovative anti-biofilm strategies include application of anti-biofilm small molecules, intrinsic or external stimulation of production of reactive molecules, utilization of materials with antimicrobial properties and dispersion of biofilms by digestion of the extracellular matrix, also in combination with physical biofilm breakdown. Although basic principles of biofilm formation have been deciphered, the molecular understanding of the formation and structural organization of various types of biofilms has just begun to emerge. Basic studies of biofilm physiology have also resulted in an unexpected discovery of cyclic dinucleotide second messengers that are involved in interkingdom crosstalk via specific mammalian receptors. These findings even open up new venues for exploring novel anti-biofilm strategies."
    
#     # syn_gen = Synonym_Generator(os.getenv('OPENAI_API_KEY'))
#     syn_gen = Synonym_Generator()
#     extracted_keywords = syn_gen.extract_keywords_trans(text,"ml6team/keyphrase-extraction-kbir-inspec")
#     print("Extracted Keywords:", extracted_keywords)


#     synonyms_dict = {}
#     for keyword in extracted_keywords:
#         # synonym_list = syn_gen.openai_api(text, [keyword])
#         # synonyms_dict[keyword] = synonym_list
#         synonym_list = syn_gen.dictionary_syn(keyword)
#         synonyms_dict[keyword] = synonym_list

#     print("Synonyms of extracted keywords:")
#     for keyword, synonyms in synonyms_dict.items():
#         print(f"{keyword}: {synonyms}")
