from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random
import time
from base64 import b64encode

app = Flask(__name__)
app.secret_key = "themagicofcthkanddetermination"



# gv = 1
# points = 0
# ans =[]
@app.route("/")
def index():
    session['gv'] = 1
    session['points'] = 0
    session['ans'] = None
    session['ts'] = None
    session['te'] = None

    return render_template('index.html')


@app.route("/startiq", methods=['POST', 'GET'])
def startiq():
    # global gv
    # global ans
    # global points

    rnd = random.randint(1, 10)

    if session['gv'] == 11:
        return render_template('result.html', pts=session['points'])
    cur = sqlite3.connect('iqdb.db')
    tmpx = 'SELECT * FROM t' + str(session['gv']) + ' WHERE c1 = ' + str(rnd)
    row = cur.execute(tmpx)
    cur.close()


    image = row[1]
    for i in range(2, 6):
        if row[i] == row[6]:
            session['ans'] = str(i - 1)
            break
    return render_template('iqchk.html', row=row, que=session['gv'], im=image)


@app.route("/nextiq", methods=['POST'])
def nexttiq():
    # global gv
    # global ans
    # global points
    session['gv'] += 1

    if session['ans'] == request.form['exampleRadios']:
        session['points'] += 1

    return redirect(url_for('startiq'))


@app.route('/result')
def result():
    return render_template('result.html')


@app.route("/finalpage", methods=['POST'])
def finalpage():
    pts = session['points']

    session['gv'] = None
    session['points'] = None
    session['ans'] = None
    cur = sqlite3.connect('iqdb.db')
    cur.execute('INSERT INTO pq (email,tid,points) values (%s, %s,%s)',
                (request.form['email'], request.form['trans'], str(pts)))
    cur.commit()
    cur.close()
    return render_template('finalpage.html')


if __name__ == '__main__':
    app.run(debug=True)