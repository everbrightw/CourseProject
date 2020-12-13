import time
import json
import requests
import utils
import re
import urllib.request
from bs4 import BeautifulSoup
from collections import deque
course = "cs357" # hardcode data



slides_elements = ['slides', 'slide', '.pdf'] # should be prioritized in order to find correct slides urls

number_of_courses_to_scrape = 10
UIUC_COURSE_WEB_TITLE = "https://courses.grainger.illinois.edu"
SEMESTER = "fa2020"

target_courses = {} # save validated courses to scrape
limitation = "cs" # only scrape cs courses

curr_url = ''
saved_course_page_count = 0;
course_urls = {}





# utils.save_slides("https://www.cs.colorado.edu/~martin/SLP/Updates/1.pdf", "cs458", "test.pdf")

try:
    response = requests.get(UIUC_COURSE_WEB_TITLE)
    soup = BeautifulSoup(response.text, 'html.parser')
    print("enter website")
    course_urls = utils.find_all_target_courses(soup)
except Exception:
    pass

#  start to scrape each website
for course_name, course_url in course_urls.items():

    try:
        response = requests.get(course_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print("Scraping a new course website: " + course_url)
        print("Found following urls:")
        for a in soup.find_all('a', href=True):
            if utils.is_lecture_slide_url(a['href']):
                print("Found the URL:", utils.parse_url(course_url, a['href']))
                # save slides to files
                parsed_course_url = utils.parse_url(course_url, a['href'])
                parsed_file_name = utils.parse_slide_name(parsed_course_url)
        
                # utils.save_slides(parsed_course_url, course_name, parsed_file_name)
        print("===================================================")

    except Exception as e:
        print(str(e))
        pass
