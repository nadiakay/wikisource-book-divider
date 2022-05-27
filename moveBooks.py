"""
Script for moving the files created by divideBook into a next.js project directory structure
"""

import shutil
import sys
import os

dest = "/Users/nadia/code/free-book-archive"


def move_book(book):
    htmldocs = [p for p in os.listdir(book) if os.path.splitext(p)[
        1] == '.html']

    if not os.path.exists(os.path.join(dest, "_html", book)):
        os.mkdir(os.path.join(dest, "_html", book))

    for doc in htmldocs:
        shutil.move(os.path.join(os.getcwd(), book, doc),
                    os.path.join(dest, "_html", book, doc))
        print("moved " + os.path.join(os.getcwd(), book, doc) +
              " to " + os.path.join(dest, "_html", book, doc))

    images = [i for i in os.listdir(os.path.join(book, "images"))]

    if not os.path.exists(os.path.join(dest, "public/assets", book)):
        os.mkdir(os.path.join(dest, "public/assets", book))

    for image in images:
        shutil.move(os.path.join(os.getcwd(), book, "images", image),
                    os.path.join(dest, "public/assets", book))
        print("moved " + os.path.join(os.getcwd(), book, "images", image) +
              " to " + os.path.join(dest, "public/assets", book))

    shutil.move(os.path.join(os.getcwd(), book, "style.css"),
                os.path.join(dest, "styles", book + ".css"))
    print("moved " + os.path.join(os.getcwd(), book, "style.css") +
          " to " + os.path.join(dest, "styles", book + ".css"))

    shutil.move(os.path.join(os.getcwd(), book, "data.json"),
                os.path.join(dest, "data/book", book + ".json"))
    print("moved " + os.path.join(os.getcwd(), book, "data.json") +
          " to " + os.path.join(dest, "data/book", book + ".json"))


if __name__ == '__main__':
    books = sys.argv[1:]
    for book in books:
        move_book(book)

    sys.exit(0)
