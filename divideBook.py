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

"""
unzip_book: takes <book>.htmlz as argument. returns path of book directory
"""


def unzip_book(path):
    dir = os.path.split(path)[0] + os.path.split(path)[1].split('.')[0]
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(dir)
    return dir


"""
strip_tags: takes html fragment as argument. returns detagged soup object.
"""


def strip_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all(True):
        tag.replaceWithChildren()
    return soup


"""
cleanup_book: removes extraneous tags from book and renames internal links to
fit next.js project directory.
takes <book_dir>/index.html as argument.
"""


def cleanup_book(fn):
    s = ""
    with open(fn, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    [tag.parent.decompose()
     for tag in soup.find_all("span", {'data-page-index': True})]

    for img in soup.find_all("img"):
        img["src"] = os.path.join('/assets/book/',
                                  os.path.split(fn)[0], os.path.split(img["src"])[1])
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    return 0


"""
split_book: splits html book from ws-export into files by chapter.
takes <book_dir>/index.html as argument. returns json representation of
chapters.
"""


def split_book(fn):
    with open(fn, 'r', encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    divs = soup.find_all('div', {'class': 'mw-content-ltr'})
    toc_links = divs[0].find_all('a', href=re.compile("#calibre_link"))
    dir = os.path.split(fn)[0]
    try:
        os.mkdir(dir)
    except FileExistsError:
        pass

    chapters = []

    for i, div in reversed(list(enumerate(divs, start=0))):
        if i == len(divs) - 1:
            continue

        title = None
        for toc_link in toc_links:
            if toc_link["href"] == "#" + div["id"]:
                # check if the chapter's parent div matches a table of contents link, and if so get title and rename the toc link
                title = strip_tags(str(toc_link.contents[0]))
                divs[0].find('a', {'href': toc_link["href"]})[
                    "href"] = "./" + str(i)
            else:
                link = div.find(id=toc_link["href"][1:])
                if link != None:
                    # and also check other el's for toc links to subsections
                    divs[0].find('a', {'href': toc_link["href"]})[
                        "href"] = "./" + str(i) + "#" + link["id"]

        filename = dir.split('/')[-1] + "/" + str(i) + ".html"
        chapters.append({"title": str(title), "id": i})
        with open(filename, "w", encoding="utf-8") as file:
            file.write(str(div))
    return chapters


"""
parse_metadata: takes book directory as arg. returns title and authors 
"""


def parse_metadata(path):
    with open(path + '/metadata.opf') as fp:
        soup = BeautifulSoup(fp, "xml")
    title = soup.find('dc:title').contents[0]
    authors = [author.contents[0] for author in soup.find_all('dc:creator')]
    return title, authors


"""
write_json: writes 
takes book directory and json chapters returned from split_book as arguments.
returns json data object.
"""


def write_json(dir, chapters):
    title, authors = parse_metadata(dir)
    data = {"title": str(title), "subjects": [], "authors": authors,
            "slug": dir, "chapters": chapters}
    print("data:", data)
    with open(dir + '/data.json', 'w') as f:
        json.dump(data, f)
    return data


if __name__ == '__main__':
    books = sys.argv[1:]
    for book in books:
        dir = unzip_book(book)
        cleanup_book(dir + '/index.html')
        chapters = list(reversed(split_book(dir + '/index.html')))
        data = write_json(dir, chapters)
        print("data:", data)
        os.remove(dir + '/index.html')
        os.remove(dir + '/metadata.opf')
        print("Extracted chapters:", *chapters, sep="\n")
    sys.exit(0)
