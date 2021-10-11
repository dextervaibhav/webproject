from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
import random
import time
from base64 import b64encode
app = Flask(__name__)
app.secret_key = "themagicofcthkanddetermination"
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='iqdb'

mysql = MySQL(app)
#gv = 1
#points = 0
#ans =[]
@app.route("/")
def index():
    session['gv']=1
    session['points']=0
    session['ans']=None
    session['ts'] = None
    session['te'] = None
    
    return render_template('index.html')

@app.route("/startiq",methods=['POST','GET'])
def startiq():

    #global gv
    #global ans
    #global points
    

    rnd = random.randint(1,10)
       

    if session['gv'] == 11:
        return render_template('result.html', pts=session['points'])
    cur1 = mysql.connection.cursor()
    cur1.execute('SELECT * FROM t'+str(session['gv'])+ ' WHERE c1 = '+str(rnd))

    row = cur1.fetchone()
    image = b64encode(row[1]).decode("utf-8")
    for i in range(2,6):
        if row[i]==row[6]:
            session['ans']=str(i-1)
            break
    return render_template('iqchk.html',row=row,que= session['gv'],im = image)


@app.route("/nextiq",methods=['POST'])
def nexttiq():
    #global gv
    #global ans
    #global points
    session['gv']+=1

    if session['ans']==request.form['exampleRadios']:
        session['points']+=1

    return redirect(url_for('startiq'))

@app.route('/result')
def result():
    return render_template('result.html')

@app.route("/finalpage",methods=['POST'])
def finalpage():
    pts = session['points']

    session['gv'] = None
    session['points'] = None
    session['ans'] = None


    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO pq (email,tid,points) values (%s, %s,%s)',(request.form['email'], request.form['trans'],str(pts)))
    cur.connection.commit()
    return render_template('finalpage.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',threaded=True)