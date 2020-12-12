UIUC_COURSE_WEB_TITLE = "https://courses.grainger.illinois.edu"

def save_slides(url:str, path_name:str):
    urllib.request.urlretrieve(url, path_name)

def get_course_website(course_number, semester) -> str:
    # The last part is hard coded right now for CS357 slides scraping
    return UIUC_COURSE_WEB_TITLE + "/" + course_number + "/" + semester + "/pages/resources.html"


def is_lecture_slide_url(url: str) -> bool:
    # TODO: find wheather the given url is lecture slide or not
    return True
