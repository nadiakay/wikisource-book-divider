"""
Script for moving the files created by divideBook into a next.js project directory structure
"""

import shutil
import sys
import os


def move_book(book, dest):
    htmldocs = [p for p in os.listdir(book) if os.path.splitext(p)[
        1] == '.html']

    if not os.path.exists(os.path.join(dest, "_book", book)):
        os.mkdir(os.path.join(dest, "_book", book))

    for doc in htmldocs:
        shutil.move(os.path.join(os.getcwd(), book, doc),
                    os.path.join(dest, "_book", book, doc))
        print("moved " + os.path.join(os.getcwd(), book, doc) +
              " to " + os.path.join(dest, "_book", book, doc))

    images = [i for i in os.listdir(os.path.join(book, "images"))]

    if not os.path.exists(os.path.join(dest, "public/assets/book", book)):
        os.mkdir(os.path.join(dest, "public/assets/book", book))

    for image in images:
        shutil.move(os.path.join(os.getcwd(), book, "images", image),
                    os.path.join(dest, "public/assets/book", book))
        print("moved " + os.path.join(os.getcwd(), book, "images", image) +
              " to " + os.path.join(dest, "public/assets/book", book))

    shutil.move(os.path.join(os.getcwd(), book, "style.css"),
                os.path.join(dest, "styles/book", book + ".css"))
    print("moved " + os.path.join(os.getcwd(), book, "style.css") +
          " to " + os.path.join(dest, "styles/book", book + ".css"))

    shutil.move(os.path.join(os.getcwd(), book, "data.json"),
                os.path.join(dest, "data/book", book + ".json"))
    print("moved " + os.path.join(os.getcwd(), book, "data.json") +
          " to " + os.path.join(dest, "data/book", book + ".json"))


if __name__ == '__main__':
    dest = sys.argv[1]
    books = sys.argv[2:]
    for book in books:
        move_book(book, dest)

    sys.exit(0)
