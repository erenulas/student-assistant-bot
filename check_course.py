import requests
from bs4 import BeautifulSoup

#   returns the last modification date of a website
def get_course_date(url):
    try:
        #   accesses to the course page and gets the last modification date
        response = requests.get(url)
        last_modified = response.headers.get("Last-Modified", -1)
        return last_modified
    except requests.exceptions.RequestException as e:
        #   enters here if an exception occurs when connecting to the page
        print(e)
        return -1
