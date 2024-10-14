""" 
COMP20008 Semester 1
Assignment 1 Task 1
"""
## JUST TO CHECK Elements
from __future__ import print_function

import pandas as pd
import json
from typing import Dict, List

import requests
import bs4
from bs4 import BeautifulSoup
import urllib
from urllib.parse import urlparse
from urllib.parse import urljoin 
from robots import process_robots, check_link_ok
import re 


# A simple page limit used to catch procedural errors.
SAFE_PAGE_LIMIT = 1000


# Task 1 - Get All Links (3 marks)
def task1(starting_links: List[str], json_filename: str) -> Dict[str, List[str]]:
    # Crawl each url in the starting_link list, and output
    # the links you find to a JSON file, with each starting
    # link as the key and the list of crawled links for the
    # value.
    # Implement Task 1 here

    ## Crawlinggggg
    ## Search each seed page, adding any links (<a>) to its corresponding list of urls 

    ## Dictionary where keys are seed URLs and values are their list of successive links found through crawling
    all_visited_links = {}
    num_visited_pages = 0

    for current_seed_link in starting_links:
        #print("CURRENT SEED LINK: " + current_seed_link)

        to_visit = []
        to_visit.append(current_seed_link)

        ## Get domain: code from https://stackoverflow.com/questions/44113335/extract-domain-from-url-in-python
        seed_netloc = urlparse(current_seed_link).netloc
        seed_scheme = urlparse(current_seed_link).scheme
        seed_domain = seed_scheme + "://" + seed_netloc + '/'
        # print(seed_domain) 

        ## Get robots.txt: code from EODP Workshop 4
        robots_item = '/robots.txt'
        robots_url = seed_domain + robots_item
        robots_page = requests.get(robots_url)
        num_visited_pages += 1
        robot_rules = process_robots(robots_page.text)

        valid_urls_on_seed_page = []
        ## Add original seed link here to avoid infinite loops in successive iterations 
        valid_urls_on_seed_page.append(current_seed_link)

        while (to_visit):

            if num_visited_pages == SAFE_PAGE_LIMIT:
                continue 
            
            ## Retrieve text: code from EODP Workshop 3.
            current_link = to_visit.pop(0)
            current_page = requests.get(current_link)
            num_visited_pages += 1

            soup = BeautifulSoup(current_page.text, 'html.parser')
            links_on_page = soup.find_all('a')

            ## From the list of all hyperlinks, add any "valid" (i.e., pass conditions below) links 
            ## to the list of pages to visit, as well as to the list of all URLs connected to the seed URL. 
            for link in links_on_page:
                
                ## From EODP Workshop 4.
                ## No 'href' means the link either doesn't exist, or doesn't lead anywhere.
                if "href" not in link.attrs:
                    continue 

                link_href = link['href']

                ## Check we are allowed to access the page according to robots.txt.
                if not check_link_ok(robot_rules, link_href):
                    continue 
                
                ## Do not include if 'href' contains an "invalid" character as defined below. 
                if (re.search('[#&?]', link_href)):
                    continue
                
                ## Get complete link by concatenating.
                url_of_link = urljoin(current_seed_link, link_href)

                ## Determine the domain of the current page. 
                netloc = urlparse(url_of_link).netloc
                scheme = urlparse(url_of_link).scheme
                domain = scheme + "://" + netloc + '/' 

                ## If the current domain is not the same as the seed domain, discard URL.
                if (domain != seed_domain):
                    continue
                
                ## Ensure the URL is not a duplicate and has not been previously visited. 
                if ((url_of_link not in to_visit) and (url_of_link not in valid_urls_on_seed_page) 
                and (url_of_link != current_seed_link)):

                    to_visit.append(url_of_link)
                    valid_urls_on_seed_page.append(url_of_link)

                    

        #print(*valid_urls_on_seed_page, sep='\n')

        ## All valid URLs have been retrieved - add the seed URL and corresponding list to dictionary
        all_visited_links[current_seed_link] = valid_urls_on_seed_page

    #print(num_visited_pages)

    ## Write dictionary to JSON output file. 
    with open(json_filename, 'w') as fp:
         json.dump(all_visited_links, fp)

    #print(json_filename)

    return all_visited_links





