from bs4 import  BeautifulSoup
import re
import urllib.request
import urllib.error
import sqlite3
import os

def main():
    base_url = "https://book.douban.com/top250?start="
    # Get data from url
    data = get_data(base_url)

    # Save Data to a SQLite Database
    save_path = "top250books.db"
    save_data(data, save_path)


'''
Input: URL. This is just a base url and after that is each page url
Output: data of all related pages
A function to get all processed data from related pages
'''
def get_data(base_url):
    # To store data from each page
    data_list = []
    for i in range(0, 9):
        url = base_url + str(i * 25)
        # Get each page
        html = get_html(url)



    return data_list


'''
Input: url
Output: html page
A function to get html page
'''
def get_html(url):
    # Define a new header send to server.
    # To avoid anti-crawler test
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 OPR/67.0.3575.137"
    }
    request = urllib.request.Request(url, headers=header)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e.reason):
            print((e.reason))
    return html


def save_data(data, save_path):
    pass


if __name__ == "__main__":
    main()
    print("Finish Crawling")