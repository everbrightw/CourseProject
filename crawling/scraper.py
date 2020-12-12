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
courses_queue = deque()

try:
    response = requests.get(UIUC_COURSE_WEB_TITLE)
    soup = BeautifulSoup(response.text, 'html.parser')
    print("enter websitte")
    utils.find_all_target_courses(soup)
except Exception:
    pass


print(utils.is_target_course("https://courses.grainger.illinois.edu/cs498DL4/fa2020"))
print(utils.is_target_course("1cs498"))



mylist = ['nowplaying', 'PBS', 'PBS', 'nowplaying', 'job', 'debate', 'thenandnow']
myset = set(mylist)
print(myset)


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
