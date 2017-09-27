import os, threading

def parse_pdf(pdf, out):
    print("Parsing %s" % pdf)
    os.system('pdf2txt.py %s -o %s/%s' % (pdf, out, pdf.split('.')[0]+'.html'))
    print("Parsed %s" % pdf)

def execute(fp, out):
    print("Parsing .pdf files at %s. Outputting to %s" % (fp, out))
    extractors = [threading.Thread(name='extractor', target=parse_pdf, args=(os.path.join(fp, pdf),out)) for pdf in os.listdir(fp) if '.pdf' in pdf]
    for t in extractors:
        t.start()
    for t in extractors:
        t.join()

if __name__ == '__main__':
    execute('.', 'parsed')
