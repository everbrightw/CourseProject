import time
import json
import requests
import urllib.request
from bs4 import BeautifulSoup

def save_slides(url:str, path_name:str):
    urllib.request.urlretrieve(url, path_name)



def get_course_website(course_number, semester) -> str:
    # The last part is hard coded right now for CS357 slides scraping
    return uiuc_courseweb_url_title + "/" + course_number + "/" + semester + "/pages/resources.html"


def is_lecture_slide_url(url: str) -> bool:
    # TODO: find wheather the given url is lecture slide or not
    return True


course = "cs357"
semester = "fa2020"

uiuc_courseweb_url_title = "https://courses.grainger.illinois.edu"

curr_url = get_course_website(course, semester)

try:
    response = requests.get(curr_url)
    soup = BeautifulSoup(response.text, 'html.parser')
except Exception:
    pass

name_count = 1
for test in soup.find_all('span', {'class': 'ti-write'}):
    slide_url = test.find_next_sibling()['href']
    path_name = slide_url.split("/")[-1]
    # save_slides(uiuc_courseweb_url_title + slide_url, path_name)
    name_count += 1
    print(uiuc_courseweb_url_title + slide_url)
