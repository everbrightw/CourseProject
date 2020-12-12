import urllib

from bs4 import BeautifulSoup
import re

UIUC_COURSE_WEB_TITLE = "https://courses.grainger.illinois.edu"
slides_elements = ['slides', 'slide', '.pdf']


def save_slides(url, path_name):
    urllib.request.urlretrieve(url, path_name)


def get_course_website(course_number, semester) -> str:
    # The last part is hard coded right now for CS357 slides scraping
    return UIUC_COURSE_WEB_TITLE + "/" + course_number + "/" + semester + "/pages/resources.html"


def is_lecture_slide_url(url: str) -> bool:
    # TODO: find wheather the given url is lecture slide or not
    if url[-4:] != ".pdf" or "hw" in url.lower() or "homework" in url.lower() or "mp" in url.lower():
        return False
    return True

def is_target_course(course_url):
    # find onely cs courses
    pattern = "cs[0-4]"
    return bool(re.search(pattern, course_url.lower()))



def find_all_target_courses(soup: BeautifulSoup) -> list:
    # return a list of urls that we are going to scrape
    table = soup.find(id='table120208')
    course_urls = []

    for ele in table.find_all("tr"):

        first_td = ele.find('td')

        course_url_container = ele.find('td', {'class': 'text-center'})
        if course_url_container:
            course_url = course_url_container.find('a')['href']
            if is_target_course(course_url):
                course_urls.append(course_url)


    return course_urls
