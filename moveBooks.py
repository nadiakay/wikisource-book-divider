"""
Script for moving the files created by divideBook into a next.js project directory structure.

Takes next.js project path as first argument and book directory paths as subsequent arguments. Moves all html files to  ./_book/<book_slug>, images to ./public/assets/book/<book_slug>, stylesheet to ./styles/book/<book_slug>.css, and json data to ./data/book/<book_slug>.json.
"""

import shutil
import sys
import os
import json


def move_book(book, dest, id):
    print("book:", book)
    data = {}
    with open(os.path.join(os.getcwd(), book, "data.json"), 'r') as f:
        print("f:", f)
        data = json.load(f)
    data["id"] = id
    with open(os.path.join(os.getcwd(), book, "data.json"), 'w') as f:
        json.dump(data, f)

    htmldocs = [p for p in os.listdir(book) if os.path.splitext(p)[
        1] == '.html']
    if not os.path.exists(os.path.join(dest, "_book", book)):
        os.mkdir(os.path.join(dest, "_book", book))
    for doc in htmldocs:
        shutil.move(os.path.join(os.getcwd(), book, doc),
                    os.path.join(dest, "_book", book, doc))

    images = [i for i in os.listdir(os.path.join(book, "images"))]
    if not os.path.exists(os.path.join(dest, "public/assets/book", book)):
        os.mkdir(os.path.join(dest, "public/assets/book", book))
    for image in images:
        shutil.move(os.path.join(os.getcwd(), book, "images", image),
                    os.path.join(dest, "public/assets/book", book))

    shutil.move(os.path.join(os.getcwd(), book, "style.css"),
                os.path.join(dest, "styles/book", book + ".css"))

    shutil.move(os.path.join(os.getcwd(), book, "data.json"),
                os.path.join(dest, "data/book", book + ".json"))


if __name__ == '__main__':
    dest = sys.argv[1]
    books = sys.argv[2:]
    for book in books:
        if (os.path.split(book)[0] and os.path.split(book)[1]):
            book = os.path.split(book)[1]
    print("books:", books)
    maxId = 0
    for j in os.listdir(os.path.join(dest, "data/book")):
        with open(os.path.join(dest, "data/book", j), 'r') as f:
            data = json.load(f)
            if(data["id"] > maxId):
                maxId = data["id"]
    for book in books:
        maxId += 1
        move_book(book, dest, maxId)

    sys.exit(0)
