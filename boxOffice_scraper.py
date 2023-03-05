import requests
from bs4 import BeautifulSoup
import pandas as pd


header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36", "Accept-Encoding": "gzip, deflate, br", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
url = "https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/?area=XWW&offset=0"
#product = soup.find_all('span' , {'class': 'a-size-base-plus'})

def getUrlData(url):
    request = requests.get(url, headers=header)
    return BeautifulSoup(request.content, 'html.parser')

def getDataColumns(soup, columns):
    columns_data = soup.find_all("span", {'class':''}) 
    for c in columns_data:
        columns.append( c.text)
    return columns

def getMovieData(soup, movie_data):
    table = soup.find_all("table")
    tr_content = table[0].find_all("tr")
    tr_content.pop(0)
    
    #Go through the result set and find the td tag with the movie data
    for tr in tr_content:
        movies = []
        for t in tr.find_all("td"):
            movies.append(t.text)
        movie_data.append(movies)
    
    #print(movie_data)

def getIMDB():
    #Get Columns from Website
    columns = []
    movie_data = []
    
    
    urlNum = 0
    while urlNum !=1000:
        url = f"https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/?area=XWW&offset={urlNum}"
        soup = getUrlData(url)
        if urlNum == 0:
            getDataColumns(soup, columns)
        getMovieData(soup, movie_data)
        urlNum = urlNum + 200

    return pd.DataFrame(data=movie_data, columns=columns)

def main():
    movies_df = getIMDB()
    #movies_df.to_csv("out.csv")


if __name__ == '__main__':
    main()
