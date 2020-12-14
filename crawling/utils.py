import urllib
import os.path
from bs4 import BeautifulSoup, SoupStrainer
import re

UIUC_COURSE_WEB_TITLE = "https://courses.grainger.illinois.edu"
slides_elements = ['slides', 'slide', '.pdf']
key_words = ['slides', 'slide', 'lecture','lectures','note','notes','resources','resource', 'schedule']


def parse_slide_name(url):

    return url.rsplit('/', 1)[-1]



def save_slides(url, course_name, file_name):
    # make a final_directory named after the course name and save slides to it
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, course_name)
    if not os.path.exists(final_directory):
       os.makedirs(final_directory)

    urllib.request.urlretrieve(url, course_name + "/" + file_name)


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

def parse_url(title, url):

    # if "https://" or "http://" in url:
    #     return url

    url = url.lower()
    title = title.lower()

    pattern = "http"
    pattern2 = ".html"

    if bool(re.search(pattern, url.lower())):
        return url.replace("..", "")
    if bool(re.search(pattern2, title.lower())):
        #if last is html rmove it
        title = title[0:title.rindex('/')]


    if title[-1] == '/':
        title = title[:-1]  # remove last slash
    if url[0] =='/': # remove second part first slash
        url = url[1:]
    if title.endswith('pages'):
        #if last is html rmove it
        title = title[:-5]
    # remove similar part
    i = 0
    while not url.startswith(title[i:]):
        i += 1

    return (title[:i] + "/" +url).replace("..", "")

def find_all_target_courses(soup: BeautifulSoup) -> dict:
    # return a list of urls that we are going to scrape
    table = soup.find(id='table120208')
    course_urls = {}

    for ele in table.find_all("tr"):

        first_td = ele.find('td')

        course_url_container = ele.find('td', {'class': 'text-center'})

        if course_url_container:
            course_name = first_td.text # unwrapp td content
            course_url = course_url_container.find('a')['href']
            if is_target_course(course_url):
                course_urls[course_name] = course_url

    return course_urls

def find_slides_menu(soup, course_url):
    # print(soup)
    menu_potential_contain_slides = []
    links = soup.find_all('a')
    for link in links:
        for key_word in key_words:
            if key_word in link['href'].lower():
                menu_potential_contain_slides.append(parse_url(course_url, link['href']))
                # print(course_url + link['href'])

    return list(set(menu_potential_contain_slides))
