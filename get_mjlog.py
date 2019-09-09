import glob
import gzip
import os
import re
import shutil
import time
import urllib.parse
import urllib.request
import zipfile
from html.parser import HTMLParser
from pathlib import Path

HEADER = {
    'Host': 'e.mjv.jp',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0', 
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'
}
SCRAWDIR = 'scraw/'
TEMPDIR = 'temp/'
HTMLDIR = 'html/'
MJLOGDIR = 'mjlog/'
YEARS = list(range(2013, 2019))

class LogParser(HTMLParser):
    def __init__(self, outfile):
        super().__init__()
        self.outfile = outfile
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    log_url = attr[1]
                    mjlog_url = re.sub(r'\?log=', 'log/?', log_url)
                    self.outfile.write(mjlog_url + '\n')

def main():
    ''' Get mjlog files from scraw zips. '''
    unzip()
    parse()
    crawl()

def crawl():
    ''' Crawl mjlog files from tenhou. '''
    pattern = 'tenhou.net'
    subs = ['e3.mjv.jp', 'e4.mjv.jp', 'e5.mjv.jp', 'k0.mjv.jp', 'e.mjv.jp']
    with open(HTMLDIR + 'raw_urls.txt') as raw_url_file:
        for raw_url in raw_url_file.readlines():
            mjlog_name = raw_url.split('/')[-1][1:-1]
            mjlog_path = MJLOGDIR + mjlog_name + '.mjlog'
            if os.path.exists(mjlog_path):
                continue
            for sub in subs.copy():
                url = re.sub(pattern, sub, raw_url)
                try:
                    req = urllib.request.Request(url=url, headers=HEADER)
                    opener = urllib.request.build_opener()
                    response = opener.open(req)
                    response = gzip.decompress(response.read()).decode('utf-8')
                    with open(mjlog_path, 'w') as outfile:
                        outfile.write(response)
                    time.sleep(1)
                    break
                except urllib.error.HTTPError as e:
                    if e.code == 404:
                        with open('404.log', 'a') as log:
                            log.write('sub: {} mjlog: {}'.format(subs.pop(0), mjlog_name))
                    else:
                        with open('crawl.log', 'a') as log:
                            log.write('exception: {} mjlog: {}'.format(str(e), mjlog_name))
                except BaseException as e:
                    with open('crawl.log', 'a') as log:
                        log.write('exception: {} mjlog: {}'.format(str(e), mjlog_name))

def parse():
    ''' Extract mahjong urls from html files. '''
    with open(HTMLDIR + 'raw_urls.txt', 'w') as outfile:
        parser = LogParser(outfile)
        for html_path in glob.glob(HTMLDIR + '*'):
            with open(html_path, 'r') as html_file:
                parser.feed(html_file.read())

def prepare_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
        return
    files = glob.glob(dir + '*')
    for file_path in files:
        os.remove(file_path)

def unzip():
    ''' Unzip files. '''
    prepare_dir(TEMPDIR)
    for year in YEARS:
        zip_path = '{}scraw{}.zip'.format(SCRAWDIR, year)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(TEMPDIR)
    prepare_dir(HTMLDIR)
    for gz_path in glob.glob(TEMPDIR + '*/*.html.gz', recursive=True):
        gz_name = Path(gz_path).stem
        html_path = HTMLDIR + gz_name
        with gzip.open(gz_path, 'rt') as infile:
            with open(html_path, 'w') as outfile:
                shutil.copyfileobj(infile, outfile)
    print('Finished unzipping.')

if __name__ == '__main__':
    main()
