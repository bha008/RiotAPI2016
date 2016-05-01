from flask import Flask, render_template, redirect, url_for, Response
from riotAPIwrapper import ritoWrap
import os
# ...

app = Flask(__name__)
rw = ritoWrap(os.environ['RIOT_API_KEY'])
# ...

@app.route('/')
def home():
    return render_template('index.html', score=rw.request_mastery_score('19659789'))
    # return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)