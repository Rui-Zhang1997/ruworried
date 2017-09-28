from bs4 import BeautifulSoup as bsoup
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
    soup = bsoup(open(html_path), 'html.parser')
    cIncidentIdPattern = re.compile('[0-9]{2}-[0-9]{6}')
    incident_ids = map(lambda n: n.parent.parent, soup(text=cIncidentIdPattern))
    id_styles = dict()
    for iid in incident_ids:
        elem_style = iid['style']
        style_list = filter(lambda n: len(n) > 0, map(lambda part: part.strip().split(':'), iid['style'].split(';')))
        id_styles[iid.text.strip().split('\n')[0]] = [n for n in style_list if n[0] == 'top' or n[0] == 'left']
   
    assoc_tags = dict()
    for k,v in id_styles.items():
        pattern = r'.*%s:%s.*' % (v[1][0], v[1][1])
        assoc_tags[k] = soup.findAll('div', {'style': re.compile(pattern)})

    for crime_id, items in assoc_tags.items():  
        crime = Crime(crime_id=crime_id)
        data = map(lambda item: item.text.strip(), items)
        for d in data:
            if re.match(cIncidentIdPattern, d):
                continue
            if 

parse_html("../../crimereports", "aug.html")
