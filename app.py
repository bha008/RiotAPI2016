from flask import Flask, render_template, redirect, url_for, g, request, json
from riotAPIwrapper import ritoWrap
from senpai_finder import SenpaiFinder
import os
import time
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



@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))

@app.errorhandler(500)
def internal_error(e):
    return redirect(url_for('home'))

@app.errorhandler(429)
def internal_error(e):
    return redirect(url_for('home'))

@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)

@app.route('/info/<region>/<username>', methods=['GET', 'POST'])
def info(region=None, username=None):
    """
    Displays some data computed from Riot API

    :param region:
    :param username:
    :return:
    """
    if request.method == 'POST':
        new_username = request.form['username']
        new_region = request.form['region']
        return redirect(url_for('info', username=new_username, region=new_region))

    summ_id = str(rw.request_id_from_name(username, region=region))

    with open('static/assets/riot_champion_data/lol-champions_latest.json') as riot_champ_file:
        json_data = json.load(riot_champ_file)

    riot_champ_file.close()

    top_champs = rw.request_all_champs(summ_id, region=region)
    league = json.load(open('solo_allchamps_challenger.json'))

    # TODO Need to  process riot_champ_file in some way.. taking too long to run

    sf = SenpaiFinder(league, top_champs)
    senpaiId, senpai_score_dict = sf.findSenpai()
    summoner_score_dict = sf.generateScoreDict(top_champs)
    t = request.values.get('t', 0)
    return render_template('index.html',
                            username=username,
                            score=rw.request_mastery_score(summ_id, region=region),
                            top_champs=top_champs,
                            riot_champ_file=json_data,
                            senpai=rw.request_name_from_id(senpaiId, region=region),
                            su_score=summoner_score_dict,
                            se_data=senpai_score_dict
                            )

if __name__ == '__main__':
    app.run(debug=True)