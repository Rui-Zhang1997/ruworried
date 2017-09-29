from bs4 import BeautifulSoup as bsoup
import os
from os import path
import re

class Crime:
    def __init__(self, crime_id='', crime_type='', report_date='', occur_date='', location='', disposition=''):
        self.crime_id = crime_id
        self.crime_type = crime_type
        self.report_date = report_date
        self.occur_date = occur_date
        self.location = location
        self.disposition = disposition

def parse_html(html_dir, html_file):
    html_path = path.join(html_dir, html_file)
    print("Parsing %s" % html_path)
    soup = bsoup(open(html_path), 'html.parser')
    cIncidentIdPattern = re.compile('[0-9]{2}-[0-9]{6}')
    incident_ids = map(lambda n: n.parent.parent, soup(text=cIncidentIdPattern))
    id_styles = dict()
    for iid in incident_ids:
        elem_style = iid['style']
        style_list = filter(lambda n: len(n) > 0, map(lambda part: part.strip().split(':'), iid['style'].split(';')))
        id_styles[iid.text.strip().split('\n')[0]] = [n for n in style_list if n[0] == 'top'][0]
    rows = dict((top[1], iid) for iid, top in id_styles.items())
    row_data = {}
    styled_divs = soup.findAll('div', {'style': re.compile(r'.*top.*')})
    for div in styled_divs:
        if 'top' in div['style']:
            style_parts = [n for n in div['style'].split(';') if 'top' in n][0].split(':') # extracting the top style value
            top_attr = style_parts[1] # getting the pixel value
            try:
                iid = rows[top_attr] # get the incident id for that row
                if iid not in row_data: # if incident id not in row_data, add it
                    row_data[iid] = []
                row_data[iid].append(div.text.strip()) # add the div to map
            except KeyError:
                pass
    print(row_data)
    
def parse_dir(html_dir):
    for f in os.listdir(html_dir):
        print("FILE", f)
        if '.html' in f:
            parse_html(html_dir, f)
