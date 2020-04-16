import sys
import requests
from lxml import html
from bs4 import BeautifulSoup

USERNAME = "<ENTER YOUR EMAIL>"
PASSWORD = "<ENTER YOUR PASSWORD>"
SCHOOL_ID = "<YOUR STD ID>"

LOGIN_URL = "https://sso.teachable.com/secure/"+SCHOOL_ID+"/users/sign_in?clean_login=true&reset_purchase_session=1"
COURSE_URL = sys.argv[1]
print(COURSE_URL)
f = open("contents.url", "r")

def main():
    session_requests = requests.session()

    # Get login csrf token
    tree = etree.HTML(session_requests.get(COURSE_URL).content)
    authenticity_token = list(set(tree.xpath("//meta[@name='csrf-token']/@content")))[0]
    authenticity_param = list(set(tree.xpath("//meta[@name='csrf-param']/@content")))[0]

    # Create payload
    payload = {
        "user[school_id]": SCHOOL_ID,
        "user[email]": USERNAME, 
        "user[password]": PASSWORD, 
        authenticity_param : authenticity_token
    }

    # Perform login
    result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

    # Scrape url
    c = 0
    inp = f.readline()
    while("END" not in inp):
        if(c%2 == 0):
            print(inp.split('\n')[0])
        else:
            LECTURE_URL = inp.split('\n')[0]
            result = session_requests.get(URL, headers = dict(referer = LECTURE_URL))
            soup = BeautifulSoup(result.content, 'lxml')
            link = soup.find_all('a', class_='download')
            if(len(link) >= 1):
                href = link[0]['href']
                print(href)

        c+=1
        inp = f.readline()
    

if __name__ == '__main__':
    main()
