from flask import Flask, render_template, redirect, url_for, Response, request, json
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
    with open('static/assets/riot_champion_data/lol-champions_6_8_1.json') as riot_champ_file:
        json_data = json.load(riot_champ_file)
        # print 'keys in temp:', json_data.keys()
        # print(json_data['data']['35'].get('image'))
        # print(json_data['data'][champ_id0]['image'].get('full'))
        # print(json_data['keys'].get(champ_id0))
        # print(json_data['keys'].get(champ_id1))
        # print(json_data['keys'].get(champ_id2))
        #
        # champ_name_0 = json_data['keys'].get(champ_id0)
        # #champ_name_png_0 = 'http://ddragon.leagueoflegends.com/cdn/6.8.1/img/champion/' + \
        # #                   json_data['data'][champ_id0]['image'].get('full') + \
        # #                    '.png'
        # champ_name_png_0 = json_data['data'][champ_id0]['image'].get('full')
        #
        # champ_name_1 = json_data['keys'].get(champ_id1)
        # champ_name_png_1 = json_data['data'][champ_id1]['image'].get('full')
        #
        # champ_name_2 = json_data['keys'].get(champ_id2)
        # champ_name_png_2 = json_data['data'][champ_id2]['image'].get('full')

    riot_champ_file.close()

    return render_template('index.html',
                           username=username,
                           score=rw.request_mastery_score(summ_id, region=region), 
						   top_champs=rw.request_top_champs(summ_id, region=region),
                           riot_champ_file=json_data
                           )

if __name__ == '__main__':
    app.run(debug=True)