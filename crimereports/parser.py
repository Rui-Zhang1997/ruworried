from bs4 as BeautifulSoup as bsoup
from os import path

def parse_html(html_dir, html_file):
    html_path = path.join(html_dir, html_file)
    soup = bsoup(open(html_path), 'html.parser')
