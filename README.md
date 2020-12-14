# EducationalWeb

## video introduction
https://youtu.be/rsyHiEcATLI

## how to run

The following instructions have been tested with Python2.7 on Linux and MacOS

1. You should have ElasticSearch installed and running -- https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html

2. Create the index in ElasticSearch by running `python create_es_index.py` from `EducationalWeb/`

3. Download tfidf_outputs.zip from here -- https://drive.google.com/file/d/19ia7CqaHnW3KKxASbnfs2clqRIgdTFiw/view?usp=sharing
   
   Unzip the file and place the folder under `EducationalWeb/static`

4. Download cs410.zip from here -- https://drive.google.com/file/d/1Xiw9oSavOOeJsy_SIiIxPf4aqsuyuuh6/view?usp=sharing
   
   Unzip the file and place the folder under `EducationalWeb/pdf.js/static/slides/`
   
5. Run `python scraper.py` from `CourseProject/crawling/` to scrape lecture slides from the website

6. Then run `python parsePDF` under `EducationalWeb/pdf.js/` to normalize the slides name and save one PDF into a folder with single slides.

7. Run `python getRelatedFiles.py` in `EducationalWeb/pdf.js/static` to get every single slide’s related slides with ranking scores

8. From `EducationalWeb/pdf.js/build/generic/web` , run the following command: `gulp server`

9. In another terminal window, run `python app.py` from `EducationalWeb/`

10. The site should be available at http://localhost:8096/

