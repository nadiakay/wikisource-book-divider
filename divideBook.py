"""
Wikisource Book Divider

Usage:  python3 divideBook.py <path_to_zipfile>

Takes directories of zipped books as arguments. Divides each book into chapters and scrapes chapter titles from table of contents. Updates chapter links in table of contents to point to respective file. Writes each chapter to a separate html document in the book directory.
"""

import sys
import os
import re
import zipfile
import json
from bs4 import BeautifulSoup


def parse_metadata(path):
    with open(path) as fp:
        soup = BeautifulSoup(fp, "xml")
    title = soup.find('dc:title').contents[0]
    authors = [author.contents[0] for author in soup.find_all('dc:creator')]
    return title, authors


def unzip_book(path):
    dir = os.path.split(path)[0] + os.path.split(path)[1].split('.')[0]
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(dir)
    return dir


def divide_book(path):
    with open(path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    [tag.parent.decompose() for tag in soup.find_all(
        "span", {'data-page-index': True})]

    # todo: move this to a different script
    for img in soup.find_all("img"):
        img["src"] = os.path.join('/assets/book/',
                                  os.path.split(path)[0], os.path.split(img["src"])[1])

    divs = soup.find_all('div', {'class': 'mw-content-ltr'})
    toc_links = divs[0].find_all('a', href=re.compile("#calibre_link"))
    dir = os.path.split(path)[0]
    chapters = []

    try:
        os.mkdir(dir)
    except FileExistsError:
        pass

    for i, div in reversed(list(enumerate(divs, start=0))):
        if i == len(divs) - 1:
            continue

        title = None
        for toc_link in toc_links:
            if toc_link["href"] == "#" + div["id"]:
                title = toc_link.contents[0]
                divs[0].find('a', {'href': toc_link["href"]})[
                    "href"] = "./" + str(i) + ".html"
            else:
                link = div.find(id=toc_link["href"][1:])
                if link != None:
                    divs[0].find('a', {'href': toc_link["href"]})[
                        "href"] = "./" + str(i) + ".html" + "#" + link["id"]

        filename = dir.split('/')[-1] + "/" + str(i) + ".html"
        chapters.append({"title": title, "id": i})
        with open(filename, "w") as file:
            file.write(str(div))
    return chapters


if __name__ == '__main__':
    books = sys.argv[1:]
    for book in books:
        dir = unzip_book(book)
        chapters = list(reversed(divide_book(dir + '/index.html')))
        title, authors = parse_metadata(dir + '/metadata.opf')
        data = {"title": title, "authors": authors,
                "slug": dir, "chapters": chapters}
        os.remove(dir + '/index.html')
        with open(dir + '/data.json', 'w') as f:
            json.dump(data, f)
        print("Extracted chapters:", *chapters, sep="\n")
    sys.exit(0)
