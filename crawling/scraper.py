import time
import json
import requests
import utils
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
courses_urls = []



try:
    response = requests.get(UIUC_COURSE_WEB_TITLE)
    soup = BeautifulSoup(response.text, 'html.parser')
    print("enter websitte")
    course_urls = utils.find_all_target_courses(soup)
except Exception:
    pass

#  start to scrape each website
for course_url in course_urls:

    try:
        response = requests.get(course_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print("Scraping a new course website: " + course_url)
        print("Found following urls:")
        for a in soup.find_all('a', href=True):
            if utils.is_lecture_slide_url(a['href']):
                print("Found the URL:", a['href'])
        print("===================================================")
    except Exception:
        pass

# while saved_course_page_count < number_of_courses_to_scrape:
#     curr_url = pages_queue.popleft()
#     try:
#         response = requests.get(curr_url)
#         soup = BeautifulSoup(response.text, 'html.parser')
#     except Exception:
#         pass
#
#     name_count = 1
#     for test in soup.find_all('span', {'class': 'ti-write'}):
#         slide_url = test.find_next_sibling()['href']
#         path_name = slide_url.split("/")[-1]
#         # utils.save_slides(UIUC_COURSE_WEB_TITLE + slide_url, path_name)
#         name_count += 1
#         print(UIUC_COURSE_WEB_TITLE + slide_url)
