
""" 
COMP20008 Semester 1
Assignment 1 Task 3
"""

from typing import Dict, List
import pandas as pd
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
import csv 

from robots import process_robots, check_link_ok


# Task 3 - Producing a Bag Of Words for All Pages (2 Marks)
def task3(link_dictionary: Dict[str, List[str]], csv_filename: str):
    # link_dictionary is the output of Task 1, it is a dictionary
    # where each key is the starting link which was used as the 
    # seed URL, the list of strings in each value are the links 
    # crawled by the system. The output should be a csv which
    # has the link_url, the words produced by the processing and
    # the seed_url it was crawled from, this should be output to
    # the file with the name csv_filename, and should have no extra
    # numeric index.
    # Implement Task 3 here


    ## For each link in the dict (in this case, the 2 seed links), loop through 
    ## their list of links, visit each one, extract Bag of Words

    ## List of lists where each element of the list is another list corresponding to: [link url, bag of words, seed url]
    all_links = []
    

    for seed_link in link_dictionary:
        crawled_links = link_dictionary[seed_link]
    
        for link in crawled_links:
            ## For all visited links 
            bag_of_words = ' '.join(task2_deriv(link)) ## workshop 5 

            ## Add to list of lists all info 
            this_link_info = [link, bag_of_words, seed_link]
            all_links.append(this_link_info)
    


    # Empty dataframe to demonstrate output data format.
    ## pd.dataframe(YOUR list )
    dataframe = pd.DataFrame(all_links, columns = ['link_url', 'words', 'seed_url'])
    dataframe.sort_values(by=['link_url', 'seed_url'], inplace=True)
    #print(dataframe)

    ## dataframe.tocsv 
    dataframe.to_csv(csv_filename, index=False)
    print(dataframe)

    return dataframe




## Modified function from task2 

def task2_deriv(link_to_extract: str) -> List[str]:

    # 1: remove anything that is not in div id = mw-content-label
    # https://stackoverflow.com/questions/32063985/deleting-a-div-with-a-particular-class-using-beautifulsoup
    page_to_extract = requests.get(link_to_extract)

    soup = BeautifulSoup(page_to_extract.content, 'html.parser') ## Thank you Journey Lu-Spencer Ed#77
    operational_text = soup.find('div', {'id': 'mw-content-text'})
    
    ## 2. remove th tags with class = infobox-label 
    ## https://scrapeops.io/python-web-scraping-playbook/python-beautifulsoup-eliminate-span-html-tags/
    th_infobox_label = operational_text.find_all('th', {'class': 'infobox-label'})
    for tag in th_infobox_label:
        tag.decompose()

    ## 3. remove div elements with class = printfooter 
    div_printfooter = operational_text.find_all('div', {'class': 'printfooter'})
    for tag in div_printfooter:
        tag.decompose()
    
    ## 4. remove div elements with id = toc 
    div_toc = operational_text.find_all('div', {'id': 'toc'})
    for tag in div_toc:
        tag.decompose()

    ## 5. remove table elements with class = ambox
    table_ambox = operational_text.find_all('table', {'class': 'ambox'})
    for tag in table_ambox:
        tag.decompose()

    ## 6. remove div elements with class = asbox 
    div_asbox = operational_text.find_all('div', {'class': 'asbox'})
    for tag in div_asbox:
        tag.decompose()
    
    ## 7. remove span elements with class = mw-editsection 
    span_mw_editsection = operational_text.find_all('span', {'class': 'mw-editsection'})
    for tag in span_mw_editsection:
        tag.decompose()

    ## 8. extract remaining text using space separator 
    ## https://stackoverflow.com/questions/6467043/extracting-element-and-insert-a-space
    clean_text = operational_text.get_text(separator = ' ')


    ## PART 2. thank you workshop 5!
    ## MAINLY STEPS 2 & 4 CHANGED COMPARED TO TASK2
    ## 1. casefold and normalise to NFKD 
    ## From Workshop 5
    clean_text_lower = clean_text.lower()
    text_lower_normalised = unicodedata.normalize('NFKD', clean_text_lower)

    ## 2. convert nonalpha to single space: dont replace A-z, spaces, newlines, tabs 
    ## https://www.stechies.com/remove-punctuation-from-string-python/
    ## step 1: remove explicitly any punctuation. for some reason going straight to ^A-z\s\t\n didnt exclude some characters
    non_alpha_removed = re.sub(r'[^\w\s\t\n\\]', ' ', text_lower_normalised)

    ## step 2: now remove numbers and non-english 
    non_alpha_removed = re.sub(r'[^A-z\\]', ' ', non_alpha_removed) # DO NOT remove backslashes 
    ## DO remove underscores 
    non_alpha_removed = re.sub(r'_', ' ', non_alpha_removed);

    ## 3. convert all tabs/newlines into single space 
    no_tabs_or_newlines = re.sub(r'[\t\n]', ' ', non_alpha_removed)
    single_spaced = re.sub(r'\s+', ' ', no_tabs_or_newlines)
    #print(single_spaced)

    ## 4. tokenise - READ AND UNDERSTAND THIS HELPER FUNCTION 
    tokenised_text = re.split(r' ', single_spaced) 
    ## tokenised_text = nltk.word_tokenize(single_spaced)


    ## 5. remove stopwords 
    stop_words = set(stopwords.words('english'))
    no_stopwords = []

    for token in tokenised_text:
        if token not in stop_words:
            no_stopwords.append(token)
        else:
            continue
    
    ## 6. remove tokens <2 characters 
    tokens_len_above_2 = []
    for token in no_stopwords:
        if len(token) >= 2:
            tokens_len_above_2.append(token)
        else:
            continue

    ## 7. convert tokens to Porter stems - from workshop 5 
    porter_stemmer = PorterStemmer()
    porter_stemmed_tokens = [porter_stemmer.stem(token) for token in tokens_len_above_2]
    
    results = {}
    results[link_to_extract] = porter_stemmed_tokens

    return results[link_to_extract]

