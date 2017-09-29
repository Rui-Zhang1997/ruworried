import os, threading

def parse_pdf(pdf, out):
    print("Extracting %s" % pdf)
    fname = os.path.basename(pdf).split('.')[0] + '.html'
    outf = os.path.join(out, fname)
    os.system('pdf2txt.py %s -o %s' % (pdf, outf))
    print("Extracted %s. Outputted to %s" % (pdf, outf))

def execute(fp, out):
    if fp[0] != '/' or out[0] != '/':
        raise Exception("Must be absolute path")
    print("Extracting .pdf files at %s. Outputting to %s" % (fp, out))
    extractors = [threading.Thread(name='extractor', target=parse_pdf, args=(os.path.join(fp, pdf), out)) for pdf in os.listdir(fp) if '.pdf' in pdf]
    for t in extractors:
        t.start()
    for t in extractors:
        t.join()

if __name__ == '__main__':
    execute('.', 'parsed')
