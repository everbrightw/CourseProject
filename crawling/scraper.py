import time
import json
import requests
import utils
import re
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer
from collections import deque
import httplib2

course = "cs357" # hardcode data



key_words = ['slides', 'slide', 'lecture','lectures','note','notes','resources','resource'] # key words most likely to be a lecture slide

number_of_courses_to_scrape = 10
UIUC_COURSE_WEB_TITLE = "https://courses.grainger.illinois.edu"
SEMESTER = "fa2020"

target_courses = {} # save validated courses to scrape
limitation = "cs" # only scrape cs courses

curr_url = ''
saved_course_page_count = 0;
course_urls = {} # dict that stores key: course_name val: course_url
coure_urls_second_iteration = {}


test_website = "https://courses.engr.illinois.edu/cs357/fa2020"


# utils.save_slides("https://courses.grainger.illinois.edu/CS361/fa2020/slides/CS361_fa20_Lec10_pre.pdf", "cstest", "test.pdf")

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
        # print("Scraping a new course website: " + course_url)
        # print("Found following urls:")
        for a in soup.find_all('a', href=True):
            potential_slides_url = [] #store files that potentially could be lecture slides

            if utils.is_lecture_slide_url(a['href']):
                parsed_course_url = utils.parse_url(course_url, a['href'])
                print("Found the URL:", parsed_course_url)
                potential_slides_url.append(parsed_course_url)

                # save slides to files
                # parsed_course_url = utils.parse_url(course_url, a['href'])
                # parsed_file_name = utils.parse_slide_name(parsed_course_url)
                # utils.save_slides(parsed_course_url, course_name, parsed_file_name)

        coure_urls_second_iteration[course_name] = utils.find_slides_menu(soup, course_url)
        print("===================================================")

    except Exception as e:
        print(str(e))
        pass

del coure_urls_second_iteration['CS 107']
del coure_urls_second_iteration['CS 105']

print("=====================printing course potential slides==============================")
for course_name, course_urls in coure_urls_second_iteration.items():
    print("current course:", course_name, course_urls)
    for course_url in course_urls:
        if not utils.is_lecture_slide_url(course_url) and ".pptx" not in course_url and ".zip" not in course_url: #not a pdf file
            print("should be existed slides?", course_url)
            try:
                response = requests.get(course_url)
                soup = BeautifulSoup(response.text, 'html.parser')
                # print("Scraping a new course website: " + course_url)
                # print("Found following urls:")
                for a in soup.find_all('a', href=True):

                    if utils.is_lecture_slide_url(a['href']) and "handouts" not in a['href']:
                        parsed_course_url = utils.parse_url(course_url, a['href'])
                        # print("Found the URL:", parsed_course_url)
                        coure_urls_second_iteration[course_name].append(parsed_course_url)
                        print("new slides found for:", course_name, parsed_course_url)
                        # save slides to files
                        # parsed_course_url = utils.parse_url(course_url, a['href'])
                        parsed_file_name = utils.parse_slide_name(parsed_course_url)
                        # utils.save_slides(parsed_course_url, course_name, parsed_file_name)
                print("===================================================")

            except Exception as e:
                print(str(e))
                pass

    # print(course_name, course_urls)


for course_name, course_urls in coure_urls_second_iteration.items():
    for course_url in course_urls:
        if ".pdf" in course_url:
            try:
                parsed_file_name = utils.parse_slide_name(course_url)
                utils.save_slides(course_url, course_name, parsed_file_name)
            except Exception as e:
                print(str(e))
                pass
