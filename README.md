# wikisource-book-divider
Python script for extracting chapters from a wikisource exported book as separate html documents. For use with htmlz files from [Wikisource Export](https://ws-export.wmcloud.org/) ([GitHub](https://github.com/wikimedia/ws-export)).

Usage:  `python3 divideBook.py <path_to_zipfile>`

Takes directories of zipped books as arguments. Divides each book into chapters and scrapes chapter titles from table of contents. Writes each chapter to a separate html document in the book directory.
