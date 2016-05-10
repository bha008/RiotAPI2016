# RiotAPI2016
# Riot API 2016 Challenge LoL Senpai Finder
## Created by:
Brendan Ha and Brian Ho

# [Here's the app!](http://lolsenpaifinder.herokuapp.com/)

## Goals:
LoL Senpai Finder compares your summoner mastery data and matches you with a player with similar playstyle in the Challenger tier, or as we call it, your [LoL Senpai](http://lolsenpaifinder.heroku.com/). 

After finding out who your LoL Senpai is, you can use that information to learn more about their playstyle and why it matches yours. You can use your LoL Senpai information to watch their streams and be a better carry, support, tank or etc. We want you to become better LoL players, and even surpass your Lol Senpai!

We leveraged Riot’s API and datasets to visualize data and create comparison charts. 

## Data Sets:
Our main datasets were pulled from Riot’s public api. We used a few of the API’s including [championmastery](https://developer.riotgames.com/api/methods#!/1071), [lol-static-data-v1.2](https://developer.riotgames.com/api/methods#!/1055/3633). Below is a detailed explanation of what how we used each dataset. 
#### championmastery
Champion mastery data was an interesting dataset to work with. Although it provides an interesting insight on the strengths of certain players, we felt that it does not provide enough relatable information. In our solution at a more interactive use of mastery data, we first collected the mastery information from the top 200 players in Challenger league. Then, as each search is run by the end user, the query’s mastery information is compared to the collected data to find the most similar play style in terms of champions mastered.
#### lol-static-data-v1.2
In order to speed up load times of our webpage, we downloaded the champion data from lol-static-data-v1.2 and used the champions’ ID as keys. In this dataset, we are using the champion id key to obtain the image name and tags (i.e. fighter, assassin, etc) associated with the champion. For example, to get the name of Ahri’s image, we would look in the api and find that ahri’s image is labeled ‘Ahri.png’. We use this information and insert it to ddragon.leagueoflegends.com/tool and point it to the appropriate url. In this case for Ahri’s champion icon, we point ddragon to: http://ddragon.leagueoflegends.com/cdn/6.9.1/img/champion/Ahri.png 

## Algorithm:
#### Preprocessing:
The mastery data collected from the desired summoner as well as each Challenger is first preprocessed so that it can be represented as a number. In our solution, we determined the total mastery points to be as follows: 
```
championMastery = (masteryLevel * 10000 + pointsSinceLastLevel) / totalMasteryPoints
```
We are aware that this is not the exact number of points that each summoner has earned in total for the specific champion. The points per level is scaled up to compensate for a model that has not been provided in the API.

After we have preprocessed data for both the target summoner and a corresponding Challenger, we calculated a similarity metric with the following function:
```
Similarity = 1 / ( sum( summonerScores - senpaiScores)^2 + 1)
```
Using this function, we establish a numerical metric for measuring how close two summoner’s mastery levels are to each other. As more corresponding champion mastery points are near each other, the similarity metric will be closer to 1. As the points diverge, the metric will be closer to 0.

Using a linear search, we find the Challenger with the most similarity and return that summoner.
## Data Visualization:
Lol Senpai utilizes [charts.js](http://www.chartjs.org/) to visualize the similarity data, and bootstrap’s [carousel](https://getbootstrap.com/examples/carousel/) to visualize the champions.
## Technologies:
In no particular order, we used javascript, html, css, Twitter [bootstrap](http://getbootstrap.com/), [charts.js](http://www.chartjs.org/). 
On the computational side, we used a [Flask microframework](http://flask.pocoo.org/) with [Python 2.7](https://www.python.org/download/releases/2.7/).

Bootstrap was chosen to manipulate the html gridspace in an easy manner. The scrolling champion icon was displayed using bootstrap. 

## Challenges/Issues Encountered:
* Shen is the only champion with the tag “Melee”
* Aurelion Sol is tagged as “Figher”
* Chart.js was easy to initialize but is probably not the best idea for a chart with massives amount of data. Chart.js contributed to the longest load time on our webpage. We will be investigating other version of charts for future uses.
* Changing default fontsize and font color in chart.js proved to be difficult

