from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.error
import sqlite3
import os

# find the link of detail info of a book
findLink_and_title = re.compile(r'<a href="(.*?)" onclick="(.*?)" title="(.*?)">')
# find the link of cover image of a book
findImg = re.compile(r'<img src="(.*?)" width="90"/>')
# find the rating score of a book
findRating = re.compile(r'<span class="rating_nums">(.*?)</span>')
# find how many people rated a book
findJudgeNum = re.compile(r'(\d*)人评价')
# find the quote of the book\
findInq = re.compile(r'<span class="inq">(.*?)</span>')
# find other information, including author, translator, press and price
findInfo = re.compile(r'<p class="pl">(.*?)</p>')


def main():
    base_url = "https://book.douban.com/top250?start="
    # Get data from url
    data_list = get_data(base_url)

    # Save Data to a SQLite Database
    save_path = "top250books.db"
    save_data(data_list, save_path)


'''
Input: URL. This is just a base url and after that is each page url
Output: data of all related pages
A function to get all processed data from related pages
    - Link of the info of a book
    - Link of the cover of a book
    - Title
    - Rating Score
    - Number of voters
    - Quote
    - Info
'''
def get_data(base_url):
    # To store data from each page
    data_list = []
    for i in range(0, 10):
        url = base_url + str(i * 25)
        # Get each page
        html = get_html(url)
        # Process each page and get data
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("tr", class_="item"):
            data = []
            item = str(item)

            link = re.findall(findLink_and_title, item)[0][0]
            data.append(link)

            imgsrc = re.findall(findImg, item)[0]
            data.append(imgsrc)

            title = re.findall(findLink_and_title, item)[0][2]
            data.append(title)

            rating = re.findall(findRating, item)[0]
            data.append(rating)

            judge = re.findall(findJudgeNum, item)[0]
            data.append(judge)

            inq = re.findall(findInq, item)
            if len(inq) == 0:
                data.append(' ')
            else:
                data.append(inq[0])

            info = re.findall(findInfo, item)[0]
            data.append(info)

            data_list.append(data)
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


def save_data(data_list, save_path):
    # init a database
    if not os.path.exists(save_path):
        init_db(save_path)

    # connect to the database
    conn = sqlite3.connect(save_path)
    cur = conn.cursor()

    for data in data_list:
        for index in range(len(data)):
            if index == 3 or index == 4:
                continue
            data[index] = '"'+data[index]+'"'
        sql = '''
            insert into top250books(
            info_link, img_link, title, rate, num_vote, quote, info)
            values(%s)'''%",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()


'''
create a new database
'''
def init_db(save_path):
    sql = '''
        create table top250books
        (
            id integer primary key autoincrement,
            info_link text,
            img_link text,
            title varchar,
            rate numeric,
            num_vote numeric ,
            quote text,
            info text
        )
    '''
    conn = sqlite3.connect(save_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
    print("Finish Crawling")
