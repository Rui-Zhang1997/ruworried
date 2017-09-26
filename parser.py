from nltk.tokenize import sent_tokenize, word_tokenize
import re

class CrimeEvent:
    def __init__(self, crime_type='', crime_date='', crime_time='', crime_location='', crime_description='', crime_perp_desc=''):
        self.crime_type = crime_type
        self.crime_date = crime_date
        self.crime_time = crime_time
        self.crime_location = crime_location
        self.crime_description = crime_description
        self.crime_perp_desc = crime_perp_desc

# extracts a phrase which contains certain words
class Phrase:
    def __init__(self, word_start=None, word_end=None):
        self.word_start = word_start
        self.length = length

def parse_evt_summary(evt, crime_obj):
    parts = 

def parse_crime_info(crime_info, crime_obj):
    pass

def parse_description(desc, crime_obj):
    pass

def parse_email(email):
    sentences = sent_tokenize(email)[:4]
    intro = sentences[0]
    evt_summary = sentences[1]
    crime_info = sentences[2]
    descrip_info = sentences[3]
    crime = CrimeEvent()
    crime.crime_description = crime_info
    parse_evt_summary(evt_summary, crime)
    parse_crime_info(crime_info, crime)
    parse_description(descrip_info, crime)
    return crime
