from bs4 import BeautifulSoup as bsoup
import os
from os import path
import re
from modules.tools import commons as cms
from modules import definitions as dfs

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
    def __init__(self, crime_id='', crime_type='', report_time=None, occur_time=None, location='', status=''):
        self.crime_id = crime_id
        self.crime_type = crime_type
        self.report_time = report_time
        self.occur_time = occur_time
        self.location = location
        self.status = status

C_INCIDENT_PATTERN = '[0-9]{2}-[0-9]{6}'
def extrapolate_row_data(row_data):
    print(row_data)
    datePattern = re.compile('^[0-9]{2}/[0-9]{2}/[0-9]{2}.*')
    timePattern = re.compile('.*[0-9]{4}(hrs|Hrs).*')
    idPattern   = re.compile(C_INCIDENT_PATTERN)
    id_ = []
    for d in row_data:
        if idPattern.search(d):
            id_ += d.split('\n')
    del row_data[row_data.index('\n'.join(id_))]
    incident_count = len(id_)
    crime = Crime()
    crime.crime_id = id_[0]
    if incident_count > 1: # processes 1-to-many
        texts = []
        dates = []
        for d in row_data:
            if datePattern.search(d):
                dates.append(d)
            else:
                texts.append(d)
        dates = cms.flatten([date.split('\n') for date in dates])
        texts = cms.flatten([text.split('\n') for text in texts])
        dt_tuples = [(d,t) for d,t in zip(dates,texts)]
        for dt_tuple in dt_tuples:
            date = dt_tuple[0].split(' ')
            times_list = date[:4]
            # sorting datetimes to determine report status
            # joins both strings together and removes all nonnumeric characters
            print("TL", times_list)
            dt1 = re.sub('[^0-9]', '', ''.join(times_list[:2]).lower())
            dt2 = re.sub('[^0-9]', '', ''.join(times_list[2:4]).lower()) if len(times_list) > 2 else None
            # converts them to DateTime object
            dts = [DateTime(dt[:2], dt[2:4], dt[4:6], dt[6:8], dt[8:]) if dt else None for dt in [dt1, dt2]]
            # sorts them based on latest to earliest
            dts = dts if not dts[0] or not dts[1] and dts[0].compare(dts[1]) == 1 else [dts[1], dts[0]]
            crime.report_time = dts[0]
            crime.occur_time = dts[1]
            crime.crime_type = dt_tuple[1]
            # attempts to extract information regarding location and status
            text = ' '.join(date[4:]).lower()
            # parsing crime by type
            for status in dfs.STATUSES:
                def_range = re.search(status, text)
                if def_range:
                    crime.status = text[def_range.start():def_range.end()]
                    crime.location = text[:def_range.start()]
                    break # if one is found, then break for everything else
    elif incident_count == 1: # processes 1-to-1
        data = cms.flatten([rd.split(' ') for rd in row_data])
        dtdata, texts = cms.categorize(data, lambda n: datePattern.search(n) or timePattern.search(n))
        dtdata = cms.flatten(dtdata)
        dt_tuples = [(dtdata[i], dtdata[i+1]) for i in range(0, len(dtdata), 2)]
        dt1 = re.sub('[^0-9]', '', ''.join(dt_tuples[0]))
        dt2 = re.sub('[^0-9]', '', ''.join(dt_tuples[1])) if len(dt_tuples) > 1 else None
        dt_sorted = [DateTime(dt[:2], dt[2:4], dt[4:6], dt[6:8], dt[8:]) if dt else None for dt in [dt1, dt2]]
        dt_sorted = dt_sorted if (not dt_sorted[0]) or (not dt_sorted[1]) or dt_sorted[0].compare(dt_sorted[1]) == 1 else [dt_sorted[1], dt_sorted[0]]
        crime.report_time = dt_sorted[0]
        crime.occur_time = dt_sorted[1]
        for text in texts:
            for status in dfs.STATUSES:
                if status in text:
                    crime.status = status
            if not crime.status or crime.status.strip() == '':
                crime.crime_type = text
    print(crime.__dict__)
    print()
    return None

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
