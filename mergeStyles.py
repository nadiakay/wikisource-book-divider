"""
Script for merging css sheets into single nested sheet with a 
distinct parent class for each sheet.

Usage: python3 mergeStyles.py <dir>
Takes parent <dir> as argument. Merges all .css sheets in <dir>
"""

from os import listdir, path
import sys
import json

def mergeSheets(dir, ss):
  css = ""
  for s in ss:
    with open(path.join(dir, 'styles/book', s["fn"]), 'r') as f:
      css = css + "._" + str(s["id"]) + " {\n\t" + str(f.read()) + "}\n\n"
  return css


if __name__ == '__main__':
  dir = sys.argv[1]
  ss = []
  for s in listdir(path.join(dir, 'styles/book')):
    d = path.join(dir, 'data/book', path.splitext(s)[0] + '.json')
    with open(d, 'r') as f:
      data = json.load(f)
    ss.append({"fn": s, "id": data["id"]})
  css = mergeSheets(dir, ss)
  with open(path.join(dir, 'styles/books.css'), 'w') as f:
    f.write(str(css))
  sys.exit(0)