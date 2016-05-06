from flask import Flask, render_template, redirect, url_for, Response, request, json
from riotAPIwrapper import ritoWrap
from senpai_finder import SenpaiFinder
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

    with open('static/assets/riot_champion_data/lol-champions_6_8_1.json') as riot_champ_file:
        json_data = json.load(riot_champ_file)

    riot_champ_file.close()

    top_champs = rw.request_all_champs(summ_id, region=region)
    league = json.load(open('solo_allchamps_challenger.json'))
    sf = SenpaiFinder(league, top_champs)
    senpaiId, senpai_score_dict = sf.findSenpai()
    summoner_score_dict = sf.generateScoreDict(top_champs)
    return render_template('index.html',
                            username=username,
                            score=rw.request_mastery_score(summ_id, region=region),
                            top_champs=top_champs,
                            riot_champ_file=json_data,
                            senpai=rw.request_name_from_id(senpaiId, region=region)
                            )

if __name__ == '__main__':
    app.run(debug=True)