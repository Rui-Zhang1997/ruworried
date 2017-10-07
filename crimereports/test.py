from tabula import read_pdf
with open('test.txt', 'w') as f:
    f.write(read_pdf('./sept.pdf'))
