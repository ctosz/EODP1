"""
COMP20008 Semester 1
Assignment 1 Task 2
"""

import json

import requests
import bs4
from bs4 import BeautifulSoup
import urllib
import unicodedata
import re
import nltk 
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from robots import process_robots, check_link_ok


# Task 2 - Extracting Words from a Page (4 Marks)
def task2(link_to_extract: str, json_filename: str):
    # Download the link_to_extract's page, process it 
    # according to the specified steps and output it to
    # a file with the specified name, where the only key
    # is the link_to_extract, and its value is the 
    # list of words produced by the processing.
    # Implement Task 2 here

    ## 1.1: Remove anything that is not in (div id == mw-content-label)
    ## https://stackoverflow.com/questions/32063985/deleting-a-div-with-a-particular-class-using-beautifulsoup
    page_to_extract = requests.get(link_to_extract)

    soup = BeautifulSoup(page_to_extract.content, 'html.parser') ## Thank you Journey Lu-Spencer Ed#77 
    operational_text = soup.find('div', {'id': 'mw-content-text'})
    
    ## 1.2: Remove 'th' tags with (class == infobox-label)
    ## https://scrapeops.io/python-web-scraping-playbook/python-beautifulsoup-eliminate-span-html-tags/
    th_infobox_label = operational_text.find_all('th', {'class': 'infobox-label'})
    for tag in th_infobox_label:
        tag.decompose()

    ## 1.3: Remove div elements with (class == printfooter)
    div_printfooter = operational_text.find_all('div', {'class': 'printfooter'})
    for tag in div_printfooter:
        tag.decompose()
    
    ## 1.4: Remove div elements with (id == toc) 
    div_toc = operational_text.find_all('div', {'id': 'toc'})
    for tag in div_toc:
        tag.decompose()

    ## 1.5: Remove table elements with (class == ambox)
    table_ambox = operational_text.find_all('table', {'class': 'ambox'})
    for tag in table_ambox:
        tag.decompose()

    ## 1.6: Remove div elements with (class == asbox)
    div_asbox = operational_text.find_all('div', {'class': 'asbox'})
    for tag in div_asbox:
        tag.decompose()
    
    ## 1.7: Remove span elements with (class == mw-editsection)
    span_mw_editsection = operational_text.find_all('span', {'class': 'mw-editsection'})
    for tag in span_mw_editsection:
        tag.decompose()

    ## 1.8: Extract remaining text using space separator 
    ## https://stackoverflow.com/questions/6467043/extracting-element-and-insert-a-space
    clean_text = operational_text.get_text(separator = ' ')


    ## PART 2. Thank you Workshop 5!
    ## 2.1: Casefold and normalise to NFKD 
    ## From Workshop 5
    clean_text_lower = clean_text.lower()
    text_lower_normalised = unicodedata.normalize('NFKD', clean_text_lower)

    ## 2.2: Convert nonalpha to single space: dont replace A-z, spaces, newlines, tabs 
    ## https://www.stechies.com/remove-punctuation-from-string-python/
    ## Step 2.2a: Remove explicitly any punctuation. For some reason going straight to ^A-z\s\t\n didnt exclude some characters
    non_alpha_removed = re.sub(r'[^\w\s\t\n]', ' ', text_lower_normalised)

    ## Step 2.2b: Now remove numbers and non-english 
    non_alpha_removed = re.sub(r'[^A-z]', ' ', non_alpha_removed)

    ## 2.3: Convert all tabs/newlines into single space 
    no_tabs_or_newlines = re.sub(r'[\t\n]', ' ', non_alpha_removed)
    single_spaced = re.sub(r'\s+', ' ', no_tabs_or_newlines)

    ## 2.4: Tokenise - READ AND UNDERSTAND THIS HELPER FUNCTION 
    ## tokenised_text = re.split(r' ', single_spaced) - This version didn't remove empty strings 
    tokenised_text = nltk.word_tokenize(single_spaced)

    ## 2.5: Remove stopwords
    stop_words = set(stopwords.words('english'))
    no_stopwords = []

    for token in tokenised_text:
        if token not in stop_words:
            no_stopwords.append(token)
        else:
            continue
    
    ## print("\ntokens reduced from", str(len(tokenised_text)), "to", str(len(no_stopwords)), "\n")

    ## 2.6: Remove tokens <2 characters 
    tokens_len_above_2 = []
    for token in no_stopwords:
        if len(token) >= 2:
            tokens_len_above_2.append(token)
        else:
            continue

    ## 2.7: Convert tokens to Porter stems - from workshop 5 
    porter_stemmer = PorterStemmer()
    porter_stemmed_tokens = [porter_stemmer.stem(token) for token in tokens_len_above_2]
    
    results = {}
    results[link_to_extract] = porter_stemmed_tokens
    
    ## Output to JSON file 
    with open(json_filename, 'w') as fp:
         json.dump(results, fp)


    return {}
