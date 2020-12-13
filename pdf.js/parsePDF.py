import os
import sys

from PyPDF2 import PdfFileWriter, PdfFileReader
"""
usage: 
"python parsePDF" will parse all pdfs under raw_slides
"python parsePDF cs-425 cs-411" will parse all specified folders under raw_slides
"""


class ParsePDF:
    def __init__(self, all_tar=None):
        self.source_path = "./static/raw_slides"
        self.tar_path = "./static/slides/"
        self.all_tar = all_tar
        if all_tar is None:
            self.all_tar = os.listdir(self.source_path)

    def parse(self):
        for folders in self.all_tar:
            if folders == ".DS_Store":
                continue
            # create new folder for each class
            if os.path.isdir(self.tar_path + "cs-"+folders[-3:]) is False:
                os.mkdir(self.tar_path + "cs-"+folders[-3:])
            ori_path = os.path.join(self.source_path, folders)

            for pdf in os.listdir(ori_path):
                pdf_path = os.path.join(ori_path, pdf)
                input_pdf = PdfFileReader(open(pdf_path, "rb"))
                tar = os.path.join(self.tar_path, "cs-"+folders[-3:])

                # truncate name
                if pdf[-4:] == ".pdf":
                    pdf = pdf[:-4]

                # create a folder for each to-be-parsed pdf
                tar = os.path.join(tar, pdf+".txt")
                if os.path.isdir(tar) is False:
                    os.mkdir(tar)

                print(input_pdf.numPages, pdf_path)
                for page in range(input_pdf.numPages):
                    output = PdfFileWriter()
                    output.addPage(input_pdf.getPage(page))

                    one_page = os.path.join(tar, "cs-%s----%s.txt----slide%d.pdf" % (folders[-3:], pdf, page))
                    with open(one_page, "wb") as outputStream:
                        output.write(outputStream)


if __name__ == '__main__':
    if len(sys.argv) != 1:
        args = sys.argv
        s = ParsePDF(args[1:])
        s.parse()

    else:
        s = ParsePDF()
        s.parse()
