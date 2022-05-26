"""
Wikisource Book Divider

Usage:  python3 divideBook.py <path_to_zipfile>

Takes directories of zipped books as arguments. Divides each book into chapters and scrapes chapter titles from table of contents. Updates chapter links in table of contents to point to respective file. Writes each chapter to a separate html document in the book directory.
"""

import sys
import os
import re
import zipfile
from bs4 import BeautifulSoup


def unzip_book(path):
    dir = os.path.split(path)[0] + os.path.split(path)[1].split('.')[0]
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(dir)
    return dir


def divide_book(path):
    with open(path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    divs = soup.find_all('div', {'class': 'mw-content-ltr'})
    toc_links = divs[0].find_all('a', href=re.compile("#calibre_link"))
    dir = os.path.split(path)[0]

    try:
        os.mkdir(dir)
    except FileExistsError:
        pass

    for i, div in reversed(list(enumerate(divs, start=0))):
        title = None
        for link in toc_links:
            if link["href"] == "#" + div["id"]:
                title = link.contents[0]
                divs[0].find('a', {'href': link["href"]})[
                    "href"] = "./" + str(i) + ".html"
        print("title:", title)

        filename = dir.split(
            '/')[-1] + "/" + str(i) + ".html"
        doc = '<head><meta charset="utf-8">'
        if(title):
            doc += '<title>' + title + '</title>'
        doc += '</head><body>' + str(div) + '</body>'
        with open(filename, "w") as file:
            file.write(doc)

    return len(divs)


if __name__ == '__main__':
    paths = sys.argv[1:]
    for path in paths:
        dir = unzip_book(path)
        count = divide_book(dir + '/index.html')
        print("Extracted " + str(count) + " chapters")
    sys.exit(0)
