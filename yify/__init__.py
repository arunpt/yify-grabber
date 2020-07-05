import os
import re
import sys
import logging
import requests
import argparse
import traceback
from bs4 import BeautifulSoup
from zipfile import ZipFile

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('yts')


def scraper(imdb_id):
    if not os.path.isdir("./subtitles"):
        os.makedirs("./subtitles")
    log.info("Connecting to the host...")
    url = f"https://yts-subs.com/movie-imdb{imdb_id}"
    page = BeautifulSoup(requests.get(url).content, 'html.parser')
    content = page.find('div',{"class":"table-responsive"})
    if content:
        log.info("Fetching all languages and its ratings...")
        lang = "English"
        movies = [[movie.find("span",{"class" : "label"}).get_text(), "https://yts-subs.com" + movie.find('a')['href']] \
            for movie in content.find_all("tr",{"class" :"high-rating"}) if \
         movie.find("span",{"class" : "sub-lang"}).get_text() == lang and movie.find("span",{"class" : "label"})]
        list_eng = {movie[1]:int(movie[0])  for movie in movies}
        log.info(f"Selecting top rated {lang} subtitle")
        top_rated = max(list_eng, key=list_eng.get)
        html = BeautifulSoup(requests.get(top_rated).content, 'html.parser')
        file_name = html.find('div', {"class": "col-xs-12","style":"margin-bottom:15px;"}).get_text().strip() 
        dwn_url = html.find('a', {"class": "btn-icon download-subtitle"})['href']    
        dwn_dir = "./subtitles/" + file_name.replace("/"," ") + ".zip"  
        log.info(f"Found {file_name}")
        log.info(f"Downloading to my local")         
        with open(dwn_dir, 'wb') as f:
            f.write(requests.get(dwn_url).content) 
        log.info("Extracting zip...")
        with ZipFile(dwn_dir) as zf:
            zf.extractall("./subtitles")
        log.info("Cleaning caches...")
        os.remove(dwn_dir)
        log.info(f"Done")
    else:
        print("Movie not found")

def main():
    parser = argparse.ArgumentParser(description='YIFY subtitle grabber by W4RR10R',prog='yify')
    parser.add_argument('-n','--name', help="Name of the movie", default=None)
    parser.add_argument('-u','--url', help="Imdb url of the movie", default=None)
    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)
    args = parser.parse_args()
    imdb_id = re.search('/(tt\d{5,7})', requests.get(f"https://www.yifysubtitles.com/search?q={args.name}").text if args.name else args.url)
    if imdb_id:
        try:
            scraper(imdb_id[0])
        except:
            traceback.print_exc()
    else:
        sys.exit("Invalid movie name or URL")

if __name__ == '__main__':
    main()
            
