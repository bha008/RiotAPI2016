from flask import Flask, render_template, redirect, url_for, Response, request
from riotAPIwrapper import ritoWrap
import os
# ...

app = Flask(__name__)
rw = ritoWrap(os.environ['RIOT_API_KEY'])
# ...

@app.route('/', methods=['GET','POST'])
def home():
    """
    Landing page to prompt user for information



    :return:
    """

    # TODO: Error checking on user input
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        region = request.form['region']
        return redirect(url_for('info', username=username, region=region))

    return render_template('form.html')

@app.route('/info/<region>/<username>')
def info(region=None, username=None):
    """
    Displays some data computed from Riot API

    :param region:
    :param username:
    :return:
    """
    summ_id = str(rw.request_id_from_name(username, region=region))
    return render_template('index.html',
                           username=username,
                           score=rw.request_mastery_score(summ_id, region=region),
                           top_champs=rw.request_top_champs(summ_id, region=region))

if __name__ == '__main__':
    app.run(debug=True)