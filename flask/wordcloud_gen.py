import jieba # separate words
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import sqlite3

# Get all words ready
conn = sqlite3.connect('top250books.db')
cur = conn.cursor()
sql = 'select quote from top250books'
data = cur.execute(sql)
text = ""
for item in data:
    text = text + item[0]

cur.close()
conn.close()

# separate words
separate = jieba.cut(text)
string = ' '.join(separate)
# print(len(string))

img = Image.open(r'./static/assets/img/test.png')
img_array = np.array(img)
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path="msyh.ttc"
)
wc.generate_from_text(string)

# draw
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')
# plt.show()
plt.savefig(r'./static/assets/img/result.png', dpi = 600)