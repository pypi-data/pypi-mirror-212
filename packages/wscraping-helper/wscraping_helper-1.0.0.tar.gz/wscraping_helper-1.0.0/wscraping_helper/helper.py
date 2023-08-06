import requests

def get_html_data(url):

    # Adatok lekérése egy URL címről

    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        return html_content

def toString(data):

    # get all text data and return array

    tomb = []

    for elem in data:

        tomb.append(elem.get_text())

    return tomb

def getAttributes(elements,arg):

    # get attribute value all item and return array

    tomb = []

    for elem in elements:
        tomb.append(elem[arg])

    return tomb

def child_tags(elements,tag):

    # all child selected tag find and return array

    tags = []
    for elem in elements:
        tags_raw = elem.find_all(tag)
        tags.extend(tags_raw)

    return tags