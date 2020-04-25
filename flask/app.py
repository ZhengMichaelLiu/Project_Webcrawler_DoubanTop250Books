from flask import Flask, render_template, request
import sqlite3
# render_template is used to render the html file
# request is used to encapsulate the form information from user input
# and pass the info to server
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/books')
def books():
    datalist = []
    conn = sqlite3.connect("top250books.db")
    cur = conn.cursor()
    sql = "select * from top250books"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    conn.close()
    return render_template("books.html", books = datalist)

@app.route('/rate')
def rate():
    score = []
    num = []
    conn = sqlite3.connect("top250books.db")
    cur = conn.cursor()
    sql = "select rate, count(rate) from top250books group by rate"
    data = cur.execute(sql)
    for item in data:
        score.append(item[0])
        num.append(item[1])
    cur.close()
    conn.close()
    return render_template("rate.html", score=score, num=num)

@app.route('/wordcloud')
def wordcloud():
    return render_template("wordcloud.html")

@app.route('/team')
def team():
    return render_template("team.html")

if __name__ == '__main__':
    app.run()




'''
# Werkzeug "tool"
# A comprehensive WSGI web application library.
# routes can not be the same, user access with a unique route
@app.route('/user/<name>')
def hello(name):
    return 'Hello %s!'%name

@app.route('/user/<int:id>')
def hello2(id):
    return 'Hello %d'%id
'''

'''
# the index.html is placed in "templates" folder
@app.route('/')
def render_basic():
    return render_template("index.html")
    
# how to pass a parameter to render_template
@app.route("/")
def hello():
    a = 1
    b = 2
    test_list = [1, 2, 3, 4, 5, 6]
    test_dict = {"first_key" : "first_value", "second_key" : "second_value"}
    return render_template("index.html", a = a,  b = b, test_list = test_list)
    
In html file: 
For single variable {{a}}, {{b}}. Use two big Parenthesis around the variable to display it

For list type variable:
{% for each_data in test_list %}     ------- notice the syntax here. 
    {{ each_data }}
{% endfor %}

For dict type variable:
{% for key,value in test_dict.items() %}     ------- notice the syntax here. 
    {{ key }}
    {{ value }}
{% endfor %}
'''

'''
@app.route('/test/register')
def register():
    return render_template("test/register.html")
    
register.html:
    <form action="{{ url_for('result') }}" method="post>      ----------dynamically find the url of the route
        <p>Name: <input type="text" name="name"></p>
        <p>Age: <input type="text" name="age"></p>
        <p>Gender: <input type="text" name="gender"></p>
        <p>Address: <input type="text" name="address"></p>
        <p><input type="submit" value="submit"></p>
    </form>    

# this route is uesd to accept a form, and the methods must be specified


@app.route('/result', methods=['POST', 'GET'])    -------- specify the methods here
    if request.method == 'POST':
        result = request.form       ------------ request can convert the from into a dict. key, value pairs
        return render_template("test_result.html", result = result)
    else:
        $$$$$$$$$$$$
'''
