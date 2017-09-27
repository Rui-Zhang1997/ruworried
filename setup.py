from crimereports import extractor

CRIME_REPORT_DIR = './crimereports'
PARSED_CRIME_REPORT_DIR = './crimereports/parsed'
def parse_pdfs():
    extractor.execute(CRIME_REPORT_DIR, PARSED_CRIME_REPORT_DIR)

if __name__ == '__main__':
    parse_pdfs()
