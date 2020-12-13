import os
import sys
import re
import shutil

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
            if os.path.isdir(self.source_path + "/" + folders) is False:
                continue
            if folders == ".DS_Store":
                print(folders)
                os.remove(self.source_path + "/" + folders)
            course_name = "cs-" + re.findall(r'\d+', folders)[0]

            # create new folder for each class
            if os.path.isdir(self.tar_path + course_name) is False:
                os.mkdir(self.tar_path + course_name)
            ori_path = os.path.join(self.source_path, folders)

            for pdf in os.listdir(ori_path):
                print(folders, pdf)

                pdf_path = os.path.join(ori_path, pdf)
                f = open(pdf_path, "rb")
                try:
                    input_pdf = PdfFileReader(f)
                except Exception:
                    print("error")
                    continue
                tar = os.path.join(self.tar_path, course_name)

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
                f.close()

        for folders in self.tar_path:
            tar = os.path.join(self.tar_path, folders)
            if os.path.isdir(tar) is False:
                continue
            if os.path.getsize(tar) == 0:
                print(tar)
                shutil.rmtree(tar)


if __name__ == '__main__':
    if len(sys.argv) != 1:
        args = sys.argv
        s = ParsePDF(args[1:])
        s.parse()

    else:
        s = ParsePDF()
        s.parse()
