import urllib

from bs4 import BeautifulSoup


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


def find_all_target_courses(soup: BeautifulSoup) -> list:
    # find all targetd courses url from uiuc grainger course websites
    
    table = soup.find(id='table120208')

    course_urls = []
    for ele in table.find_all("tr"):
        ret.append(ele.find('td'))

        first_td = ele.find('td')

        # if first_td:
        #     # course title
        #     print(first_td.text)
        course_url_container = ele.find('td', {'class': 'text-center'})
        if course_url_container:
            # the container is valid, add urls to courses
            course_urls.append(course_url.find('a')['href'])
