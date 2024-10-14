"""
COMP20008 Semester 1
Assignment 1 Task 4
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict
from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer


# Task 4 - Plotting the Most Common Words (2 Marks)
def task4(bow: pd.DataFrame, output_plot_filename: str) -> Dict[str, List[str]]:
    # The bow dataframe is the output of Task 3, it has 
    # three columns, link_url, words and seed_url. The 
    # output plot should show which words are most common
    # for each seed_url. The visualisation is your choice,
    # but you should make sure it makes sense for what it
    # is meant to be.
    # Implement Task 4 here

    most_common_words = {}

    ## Get list of disctinct seed URLs
    seed_urls = bow.seed_url.unique()

    ## Split dataframe according to seed url. Hard coded for 2 seed links as per assignment spec 
    seed_url_1_df = bow[bow["seed_url"] == seed_urls[0]]
    seed_url_2_df = bow[bow["seed_url"] == seed_urls[1]]


    ## From Workshop 5 and https://medium.com/@cristhianboujon/how-to-list-the-most-common-words-from-text-corpus-using-scikit-learn-dad4d0cab41d
    vectorizer1 = CountVectorizer()
    bow1 = vectorizer1.fit_transform(seed_url_1_df["words"]) ## matrix containing frequency of each word on each page 
    sum_words1 = bow1.sum(axis=0) ## single vector where each number corresponds to a word, and is equal to the sum of the word's occurrence in all pages 
    words_freq1 = [(word, sum_words1[0, index]) for word, index in vectorizer1.vocabulary_.items()] 
    words_freq1 = sorted(words_freq1, key=lambda x:x[1], reverse=True)

    ## create dataframe for easier plotting 
    word_freq_df_1 = pd.DataFrame(words_freq1, columns = ['word', 'frequency']).head(10)
    
    ## top 10 most frequent words for url 1 is the top 10 in words_freq1
    top_10_freq_words_1 = [word_freq_tuple[0] for index, word_freq_tuple in enumerate(words_freq1) if index < 10] ## https://stackoverflow.com/questions/14864922/in-python-list-comprehension-is-it-possible-to-access-the-item-index

    ## add to dictionary 
    most_common_words[seed_urls[0]] = top_10_freq_words_1
    
    ## repeat for second URL 
    vectorizer2 = CountVectorizer()
    bow2 = vectorizer2.fit_transform(seed_url_2_df["words"])  
    sum_words2 = bow2.sum(axis=0)  
    words_freq2 = [(word, sum_words2[0, index]) for word, index in vectorizer2.vocabulary_.items()] 
    words_freq2 = sorted(words_freq2, key=lambda x:x[1], reverse=True)
    word_freq_df_2 = pd.DataFrame(words_freq2, columns = ['word', 'frequency']).head(10)

    top_10_freq_words_2 = [word_freq_tuple[0] for index, word_freq_tuple in enumerate(words_freq2) if index < 10]
    most_common_words[seed_urls[1]] = top_10_freq_words_2

    ## now graph them: from workshop 5 
    # Enlarge the figure shape and font size
    plt.rcParams["figure.figsize"] = (35, 8) # Larger figure size
    plt.rc('font', size=14)

    # Basic plot: https://stackoverflow.com/questions/32975744/how-to-set-same-scale-for-subplots
    fig = plt.figure()
    graph_1 = fig.add_subplot(1, 2, 1)
    graph_1.bar(word_freq_df_1['word'], word_freq_df_1['frequency'], color='green', width=0.3, 
            alpha=1, label='Word vs Frequency')

    # other formatting options
    plt.grid()
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title("Ten most common words across pages visited from seed link: " + seed_urls[0])
    plt.legend()

    # show the figure
    plt.savefig(output_plot_filename) 

    ## again for second subplot 
    graph_2 = fig.add_subplot(1, 2, 2, sharey=graph_1)
    graph_2.bar(word_freq_df_2['word'], word_freq_df_2['frequency'], color='blue', width=0.3, 
            alpha=1, label='Token vs Frequency')

    # other formatting options
    plt.grid()
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title("Ten most common words across pages visited from seed link: " + seed_urls[1])
    plt.legend()

    # show the figure
    plt.savefig(output_plot_filename) 
    

    return most_common_words
