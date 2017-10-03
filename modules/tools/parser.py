from bs4 import BeautifulSoup as bsoup
import os
from os import path
import re
from modules.tools import commons as cms
from modules import definitions

class DateTime:
    def __init__(self, year, month, day, hour, minute):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute

    def compare(self, odt):
        tA = [self.year, self.month, self.day, self.hour, self.minute]
        tB = [odt.year, odt.month, odt.day, odt.hour, odt.minute]
        for i in range(len(tA)):
            if tA[i] != tB[i]:
                return 1 if tA[i] > tB[i] else -1
        return 0

class Crime:
    def __init__(self, crime_id='', crime_type='', report_date=None, occur_date=None, location='', disposition=''):
        self.crime_id = crime_id
        self.crime_type = crime_type
        self.report_date = report_date
        self.occur_date = occur_date
        self.location = location
        self.disposition = disposition

C_INCIDENT_PATTERN = '[0-9]{2}-[0-9]{6}'
def extrapolate_row_data(row_data):
    start_time = None
    end_time = None
    id_ = None
    cause = None
    result = None
    dates = []
    text = []
    print(row_data)
    datePattern = re.compile('^[0-9]{2}/[0-9]{2}/[0-9]{2}.*')
    timePattern = re.compile('.*[0-9]{4}hrs.*')
    idPattern = re.compile(C_INCIDENT_PATTERN)
    row_data = cms.flatten([re.split('\s+', data) for data in row_data])
    row_data = [s.lower() for s in row_data]
    for datum in row_data:
        if idPattern.search(datum):
            id_ = datum.split('\n')[0]
        elif datePattern.search(datum) or timePattern.search(datum):
            dates.append(datum)
        else:
            text.append(datum)
    datetimes = cms.flatten([re.split('\s+', t) for t in dates])
    timestamps = []
    for i in range(0, len(datetimes), 2):
        dd = datetimes[i].split('/')
        dt = datetimes[i+1] # if len(datetimes) > i+1 else '0000'
        timestamps.append(DateTime(dd[2], dd[0], dd[1], dt[0:2], dt[2:4]))
    # orders timestamps
    if len(timestamps) == 2:
        timestamps = timestamps if timestamps[0].compare(timestamps[1]) == -1 else [timestamps[1], timestamps[0]]
    joined_text = ' '.join(text)
    for status in definitions.DEFINITIONS:
        loc = re.search(status, joined_text)

def parse_html(html_dir, html_file):
    html_path = path.join(html_dir, html_file)
    print("Parsing %s" % html_path)
    soup = bsoup(open(html_path), 'html.parser')
    incident_ids = map(lambda n: n.parent.parent, soup(text=re.compile(C_INCIDENT_PATTERN)))
    id_styles = dict()
    for id_ in incident_ids:
        elem_style = id_['style']
        style_list = filter(lambda n: len(n) > 0, map(lambda part: part.strip().split(':'), id_['style'].split(';')))
        id_styles[id_.text.strip().split('\n')[0]] = [n for n in style_list if n[0] == 'top'][0]
    rows = dict((top[1], id_) for id_, top in id_styles.items())
    row_data = {}
    styled_divs = soup.findAll('div', {'style': re.compile(r'.*top.*')})
    for div in styled_divs:
        if 'top' in div['style']:
            style_parts = [n for n in div['style'].split(';') if 'top' in n][0].split(':') # extracting the top style value
            top_attr = style_parts[1] # getting the pixel value
            try:
                id_ = rows[top_attr] # get the incident id for that row
                if id_ not in row_data: # if incident id not in row_data, add it
                    row_data[id_] = []
                row_data[id_].append(div.text.strip()) # add the div to map
            except KeyError:
                pass
    return dict(((id_, extrapolate_row_data(row)) for id_, row in row_data.items()))
    
def parse_dir(html_dir):
    for f in os.listdir(html_dir):
        print("FILE", f)
        if '.html' in f:
            parse_html(html_dir, f)
