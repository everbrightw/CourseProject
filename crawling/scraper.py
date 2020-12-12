import time
import json
import requests
import utils
import urllib.request
from bs4 import BeautifulSoup

slides_elements = ['slides', 'slide', '.pdf']

UIUC_COURSE_WEB_TITLE = "https://courses.grainger.illinois.edu"
SEMESTER = "fa2020"
target_courses = {}
course = "cs357" # hardcode data


curr_url = utils.get_course_website(course, SEMESTER)

try:
    response = requests.get(curr_url)
    soup = BeautifulSoup(response.text, 'html.parser')
except Exception:
    pass

name_count = 1
for test in soup.find_all('span', {'class': 'ti-write'}):
    slide_url = test.find_next_sibling()['href']
    path_name = slide_url.split("/")[-1]
    # utils.save_slides(UIUC_COURSE_WEB_TITLE + slide_url, path_name)
    name_count += 1
    print(UIUC_COURSE_WEB_TITLE + slide_url)
