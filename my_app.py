from flask import Flask, render_template
import requests
import pandas as pd
from flask_mysqldb import MySQL
import yaml

#create app object
app = Flask(__name__)

#connect with configuration file and db
db=yaml.load(open('db.yaml'))
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']
mysql=MySQL(app)

@app.route('/')
def index():
    #create request to tmdb api
    response = requests.get("https://api.themoviedb.org/3/movie/now_playing?api_key=bbb0e77b94b09193e6f32d5fac7a3b9c&region=GR")
    dt = response.json()
    #create df with response results
    df = pd.json_normalize(dt['results'])
    #keep only necessary columns
    data = df[["id", "original_title", "title","overview"]]
    values=data.values.tolist()
    cur=mysql.connection.cursor()
    query="INSERT INTO now_playing (movie_id, original_title, title, overview) VALUES (%s, %s, %s, %s)"
    #execute multiple insert queries
    cur.executemany(query,values)
    mysql.connection.commit()

    return render_template('index.html',movies=values)

if __name__ == '__main__':
    app.run(debug=True)

