#!/usr/bin/python3

import re
from bs4 import BeautifulSoup

# TODO: Add support for reading from file
# TODO: Add a better text extraction to be much more readable
# TODO: Add support for reading from URL
# TODO: Update multiline_input to be more generic and move it to commons.py

def multiline_input(pre_text='Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.', delim='> '):
        print(pre_text)

        content = []
        while True:
                try:
                        line = input()
                except EOFError:
                        break
                content.append(line)
        return '\n'.join(content)

print('In the following provide the raw HTML you want to parse -')
contents = multiline_input()
html = BeautifulSoup(contents, 'html.parser')

text = html.text
text = re.sub(r'[\r\n]{2,}', '\n', text)

print(html.text)
