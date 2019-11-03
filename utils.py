import re
import requests
from lxml import html

valid_link_re = r"(?!file://)(vk.com/|vkontakte.com/).*"


def is_valid_link(link: str) -> bool:
    if re.search(valid_link_re, link):
        return True
    else:
        return False


def is_community_open(link: str) -> bool:
    try:
        page = html.fromstring(requests.get(link).text)
    except requests.exceptions.MissingSchema:
        page = html.fromstring(requests.get("http://" + link).text)

    if len(page.cssselect(".post__anchor") + page.cssselect(".post")) == 0:
        return False
    else:
        return True


def get_current_latest_post(link: str):
    try:
        page = html.fromstring(requests.get(link).text)
    except requests.exceptions.MissingSchema:
        page = html.fromstring(requests.get("http://" + link).text)

    try:
        latest_post_name = (page.cssselect(".post__anchor") + page.cssselect(".post"))[0].attrib["name"]
    except IndexError:
        return "AAAAA"

    return latest_post_name
