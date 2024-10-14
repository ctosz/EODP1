"""
COMP20008 Semester 1
Assignment 1 Task 5
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sklearn as sklearn
from typing import Dict, Union, List
import seaborn as sns


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans 
from sklearn.decomposition import PCA
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import MinMaxScaler


# Task 5 - Dimensionality Reduction (3 marks)
def task5(bow_df: pd.DataFrame, tokens_plot_filename: str, distribution_plot_filename: str) -> Dict[str, Union[List[str], List[float]]]:
    # bow_df is the output of Task 3, for this task you 
    # should generate a bag of words, normalisation of the 
    # data perform PCA decomposition to 2 components, and 
    # then plot all URLs in a way which helps you answer
    # the discussion questions. If you would like to verify 
    # your PCA results against the sample data, you can return
    # the PCA weights - containing the list of most positive
    # weighted words, most negatively weighted words and the 
    # weights in the PCA decomposition for each respective word.
    # Implement Task 5 here

    result_dict = {} 
    values_for_first_greatest_variance_pc = {}
    values_for_second_greatest_variance_pc = {}

    ## get bag of words for all words across all pages 
    vectorizerBow = CountVectorizer()
    bow = vectorizerBow.fit_transform(bow_df['words'])
    bow_clean_df = pd.DataFrame(bow.toarray(), columns=vectorizerBow.get_feature_names_out())

    ## normalise 
    n_scaler = Normalizer(norm='max')
    scaled_data = n_scaler.fit_transform(bow_clean_df)
    scaled_df = pd.DataFrame(scaled_data, columns=vectorizerBow.get_feature_names_out())

    ## PCA 
    sklearn_pca = PCA(n_components=2)
    pca_applied = sklearn_pca.fit_transform(scaled_data)
    pca_applied_df = pd.DataFrame(pca_applied)

    ## 5B: plot distributions 
    ## https://stackoverflow.com/questions/14885895/color-by-column-values-in-matplotlib
    ## Workshop 5
    plt.rcParams["figure.figsize"] = (10, 7) # Larger figure size
    plt.rc('font', size=14)

    sns.scatterplot(x=pca_applied[:,0], y=pca_applied[:,1], hue=bow_df['seed_url'], s=50)
    plt.grid()
    plt.xlabel('First Principal Component')
    plt.ylabel('Second Pincipal Component')
    plt.title("Distribution of articles retrieved from each seed url")
    plt.legend(prop={'size': 9})
    plt.savefig(distribution_plot_filename)

    
    ## from now on: 5A
    ## https://www.youtube.com/watch?v=QdBy02ExhGI 
    ## https://stackoverflow.com/questions/42422201/most-important-original-features-of-principal-component-analysis
    vocab = vectorizerBow.get_feature_names_out()
    word_weights_principal_components_df = pd.DataFrame(sklearn_pca.components_,columns=vocab,index = ['PC-0','PC-1'])
    word_weights_principal_component_0_df = pd.DataFrame([word_weights_principal_components_df.iloc[0]])
    word_weights_principal_component_1_df = pd.DataFrame([word_weights_principal_components_df.iloc[1]])

    # https://www.geeksforgeeks.org/get-a-specific-row-in-a-given-pandas-dataframe/
    top10_pos_word_weights_principal_component_0_df = word_weights_principal_component_0_df.sort_values(by=['PC-0'], ascending=False, axis=1).iloc[: , :10]

    top10_neg_word_weights_principal_component_0_df = word_weights_principal_component_0_df.sort_values(by=['PC-0'], ascending=True, axis=1).iloc[: , :10]
    
    top10_pos_word_weights_principal_component_1_df = word_weights_principal_component_1_df.sort_values(by=['PC-1'], ascending=False, axis=1).iloc[: , :10]

    top10_neg_word_weights_principal_component_1_df = word_weights_principal_component_1_df.sort_values(by=['PC-1'], ascending=True, axis=1).iloc[: , :10]


    ## set dictionary to all values found 
    values_for_first_greatest_variance_pc["positive"] = list(top10_pos_word_weights_principal_component_0_df.columns)
    values_for_first_greatest_variance_pc["negative"] = list(top10_neg_word_weights_principal_component_0_df.columns)
    values_for_first_greatest_variance_pc["positive_weights"] = list(top10_pos_word_weights_principal_component_0_df.iloc[0])
    values_for_first_greatest_variance_pc["negative_weights"] = sorted(list(top10_neg_word_weights_principal_component_0_df.iloc[0]), reverse=True)

    result_dict["0"] = values_for_first_greatest_variance_pc

    values_for_second_greatest_variance_pc["positive"] = list(top10_pos_word_weights_principal_component_1_df.columns)
    values_for_second_greatest_variance_pc["negative"] = list(top10_neg_word_weights_principal_component_1_df.columns)
    values_for_second_greatest_variance_pc["positive_weights"] = list(top10_pos_word_weights_principal_component_1_df.iloc[0])
    values_for_second_greatest_variance_pc["negative_weights"] = sorted(list(top10_neg_word_weights_principal_component_1_df.iloc[0]), reverse=True)

    result_dict["1"] = values_for_second_greatest_variance_pc

    ## print all tokens and their weights 
    ## From Workshop 5
    # Enlarge the figure shape and font size
    plt.rcParams["figure.figsize"] = (39, 14) # Larger figure size
    plt.rc('font', size=14)

    # Basic plot: https://stackoverflow.com/questions/32975744/how-to-set-same-scale-for-subplots
    fig = plt.figure()
    graph_1 = fig.add_subplot(2, 2, 1)
    graph_1.bar(values_for_first_greatest_variance_pc['positive'], values_for_first_greatest_variance_pc['positive_weights'], color='green', width=0.2, 
            alpha=1)

    # other formatting options
    plt.grid()
    plt.xlabel('Token')
    plt.ylabel('Weight')
    plt.title("Top 10 positively weighted tokens for first Principal Component")

    # show the figure
    plt.savefig(tokens_plot_filename) 

    ## again for second subplot 
    graph_2 = fig.add_subplot(2, 2, 2, sharey=graph_1)
    graph_2.bar(values_for_first_greatest_variance_pc['negative'], values_for_first_greatest_variance_pc['negative_weights'], color='green', width=0.2, 
            alpha=1)

    # other formatting options
    plt.grid()
    plt.xlabel('Token')
    plt.ylabel('Weight')
    plt.title("Top 10 negatively weighted tokens for first Principal Component")

    # show the figure
    plt.savefig(tokens_plot_filename) 

    ## again for third subplot 
    graph_3 = fig.add_subplot(2, 2, 3, sharey=graph_1)
    graph_3.bar(values_for_second_greatest_variance_pc['positive'], values_for_second_greatest_variance_pc['positive_weights'], color='blue', width=0.2, 
            alpha=1)

    # other formatting options
    plt.grid()
    plt.xlabel('Token')
    plt.ylabel('Weight')
    plt.title("Top 10 positively weighted tokens for second Principal Component")

    # show the figure
    plt.savefig(tokens_plot_filename) 

    ## again for fourth subplot 
    graph_4 = fig.add_subplot(2, 2, 4, sharey=graph_1)
    graph_4.bar(values_for_second_greatest_variance_pc['negative'], values_for_second_greatest_variance_pc['negative_weights'], color='blue', width=0.2, 
            alpha=1)

    # other formatting options
    plt.grid()
    plt.xlabel('Token')
    plt.ylabel('Weight')
    plt.title("Top 10 negatively weighted tokens for second Principal Component")

    # show the figure
    plt.savefig(tokens_plot_filename)


    return result_dict
 
