# -*- coding: utf-8 -*-
import sys
import requests, re
from bs4 import BeautifulSoup
try:
    import urllib.request
except ImportError:
    import urllib2


def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(barLength * iteration // total)
    bar = fill * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


def download(datasetname = "ecco-tcp", dataseturl = "http://www.lib.umich.edu/tcp/docs/texts/ecco/"):
    for url, filename in get_all_data(dataseturl):
        print("Downloading "+filename+":",)
        urllib.request.urlretrieve(url,filename,reporthook)


def get_all_data(dataseturl):
    soup = BeautifulSoup(requests.get(dataseturl).text, "lxml")
    for a in soup.find('table').find_all('a'):
        link = a['href']
        if re.match(r'^xml.*\.zip', link) or 'headers.ecco.zip' in link:
            yield dataseturl + link, link


def reporthook(blocknum, blocksize, totalsize):
    read = blocknum * blocksize
    total = totalsize // blocksize
    if totalsize > 0:
        percent = read * 100 // totalsize
        printProgress(percent, 100,prefix='Progress:',suffix='Complete', barLength=50)


def main():
    download()

if __name__ == "__main__":
    main()
