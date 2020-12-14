import PyPDF2
import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import os
import csv

directory = 'slides'

dict = {}
related_dict = {}

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

# Jaccard similarity
def get_jaccard_sim(lst1, lst2):
    lst3 = intersection(lst1, lst2)
    return float(len(lst3)) / (len(lst1) + len(lst2) - len(lst3))


for course in os.listdir(directory):
    course_dir = os.path.join(directory, course)
    if os.path.isdir(course_dir):
        for folder in os.listdir(course_dir):
            if folder != '.DS_Store':
                slidename = os.path.join(course_dir, folder)
                for filename in os.listdir(slidename):
                    try:
                        fileurl = os.path.join(slidename, filename)
                        #print(os.path.join(slidename, filename))
                    # filename = 'cs357/slide1/slide1-page0.pdf'
                        #print(os.path.join(directory, filename))
                        pdfFileObj = open(os.path.join(slidename, filename),'rb')
                        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

                        num_pages = pdfReader.numPages
                        count = 0
                        text = ""
                        #The while loop will read each page.
                        while count < num_pages:
                            pageObj = pdfReader.getPage(count)
                            count +=1
                            text += pageObj.extractText()

                        if text != "":
                           text = text
                        #If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text.
                        else:
                           text = textract.process(fileurl, method='tesseract', language='eng')

                        #The word_tokenize() function will break our text phrases into individual words.
                        tokens = word_tokenize(text)
                        #We'll create a new list that contains punctuation we wish to clean.
                        punctuations = ['(',')',';',':','[',']',',','?','!', '&', '%', '*',  '#', '$', '+', '``', '.']
                        #We initialize the stopwords variable, which is a list of words like "The," "I," "and," etc. that don't hold much value as keywords.
                        stop_words = stopwords.words('english')
                        #We create a list comprehension that only returns a list of words that are NOT IN stop_words and NOT IN punctuations.
                        keywords = [word.lower() for word in tokens if not word in stop_words and not word in punctuations]

                        dict[filename] = keywords
                    #print(dict)
                    except:
                        pass  # o

related_dict = {}
for key in dict:
    sim = [key.strip('.pdf').replace('----', '##')]
    for key2 in dict:
        jac_sim = get_jaccard_sim(dict[key], dict[key2])
        if jac_sim > 0.3:
            if key2 != key:
                sim.append(key2.strip('.pdf').replace('----', '##'))
                sim.append(jac_sim)

    related_dict[key.strip('.pdf').replace('----', '##')] = sim


# print('related_dict')
# print(related_dict)
    #https://www.geeksforgeeks.org/python-intersection-two-lists/
#reference:https://medium.com/better-programming/how-to-convert-pdfs-into-searchable-key-words-with-python-85aab86c544f

with open('ranking.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for key in related_dict:
        writer.writerow(related_dict[key])

with open('slide_names.txt', 'a') as the_file:
    for key in related_dict:
        the_file.write(key + '\n')
