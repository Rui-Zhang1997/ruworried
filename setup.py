from modules.tools import extractor
from modules.tools import parser
import os

CRIME_REPORT_DIR = './crimereports'
PARSED_CRIME_REPORT_DIR = './crimereports/parsed'
CRIME_REPORT_ABS = os.path.abspath(CRIME_REPORT_DIR)
PARSED_CRIME_ABS = os.path.abspath(PARSED_CRIME_REPORT_DIR)
def parse_pdfs():
    extractor.execute(CRIME_REPORT_ABS, PARSED_CRIME_ABS)

if __name__ == '__main__':
    # parse_pdfs()
    parser.parse_html(PARSED_CRIME_REPORT_DIR, 'sept.html')
