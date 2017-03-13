"""Scrapes Million Song Dataset Website for categories"""
import bs4 as bs
from urllib import urlopen

def get_possible_categories():
    """ Scrape msd website for categories and descriptions

    http://labrosa.ee.columbia.edu/millionsong/pages/example-track-description

    Returns
    ------
    n/a
    """
    target_url = "https://labrosa.ee.columbia.edu/millionsong/pages/example-track-description"
    sauce = urlopen(target_url).read()
    soup = bs.BeautifulSoup(sauce, "lxml")
    dl_data = soup.find_all("dl")
    for item in dl_data:
        dts = item.find_all("dt")
        dds = item.find_all("dd")
        dts = [dt.string for dt in dts]
        dds = [dd.string for dd in dds]
    for i,(dt,dd) in enumerate(zip(dts,dds)):
        print i,"-",dt,"\n",dd,"\n"
if __name__ == "__main__":
    get_possible_categories()

