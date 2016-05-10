//var ctx = document.getElementById("data_chart");
//var python_data = {{ su_score|tojson }};
//var keys = [];
//var su_values = [];
//var se_data = {{ se_data|tojson }};
//var se_values = [];
//var summ_types = { "Marksman":0, "Assassin":0, "Support":0, "Mage":0, "Fighter":0, "Tank":0 };
//var senpai_types = { "Marksman":0, "Assassin":0, "Support":0, "Mage":0, "Fighter":0, "Tank":0 };
//var d = {{ riot_champ_file|tojson }};
//var summ_types_values = [];
//var senpai_types_values = [];

function initGraphs(){
    for (var key in python_data) {
        if (python_data.hasOwnProperty(key)) {
            keys.push( d['data'][key]['name']);
            su_values.push(python_data[key]);
            se_values.push(se_data[key]);

        var a = d['data'][key]['tags']
            a.forEach(function( tag ) {
                summ_types[tag] = summ_types[tag] + python_data[key];
                senpai_types[tag] = senpai_types[tag] + se_data[key];
            });
        }
    }



    for( category in summ_types){
        if (summ_types.hasOwnProperty(category)) {
            summ_types_values.push( summ_types[category] );
            senpai_types_values.push( senpai_types[category] );
        }
    }
}

function drawBarGraph(){
    Chart.defaults.global.responsive = true;
    var data = {
        labels: keys,
        datasets: [
            {
                label: "Summoner",
                backgroundColor: "rgba(255,99,132,0.2)",
                borderColor: "rgba(255,99,132,1)",
                borderWidth: 1,
                hoverBackgroundColor: "rgba(255,99,132,0.4)",
                hoverBorderColor: "rgba(255,99,132,1)",
                data: su_values,
            },
            {
                label: "Senpai",
                backgroundColor: "rgba(255,255,132,0.2)",
                borderColor: "rgba(255,255,132,1)",
                borderWidth: 1,
                hoverBackgroundColor: "rgba(255,255,132,0.4)",
                hoverBorderColor: "rgba(255,255,132,1)",
                data: se_values,
            }
        ]
    };
    var myChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: data,
        responsive: false,
        fullWidth: false,
        stacked: true,
        options: {
            maintainAspectRatio: true,
            defaultFontSize: 20,
            defaultColor: "rgba(255,255,255,0.2)",

            scales: {
                pointLabels: {
                    fontSize: 20
                },

                yAxes: [{
                    ticks: {
                        beginAtZero:true,
                        fontSize: 20
                    },
                    gridLines: {
                        color: "rgba(255,255,255,0.2)"
                    }
                }],
                xAxes: [{
                    display: false,

                }]
            }
        }
    });
}

function drawRadarGraph(){
    Chart.defaults.global.responsive = true;
    ctx = document.getElementById("radar_chart");

    data = {
        labels: Object.keys(summ_types),
        datasets: [
            {
                label: "Summoner",
                backgroundColor: "rgba(100,100,255,0.2)",
                borderColor: "rgba(100,100,255,1)",
                pointBackgroundColor: "rgba(100,100,255,1)",
                pointBorderColor: "#fff",
                pointHoverBackgroundColor: "#fff",
                pointHoverBorderColor: "rgba(100,100,255,1)",
                data: summ_types_values
            },
            {
                label: "Senpai",
                backgroundColor: "rgba(255,99,132,0.2)",
                borderColor: "rgba(255,99,132,1)",
                pointBackgroundColor: "rgba(255,99,132,1)",
                pointBorderColor: "#fff",
                pointHoverBackgroundColor: "#fff",
                pointHoverBorderColor: "rgba(255,99,132,1)",
                data: senpai_types_values
            }
        ]
    };

    var radChart = new Chart(ctx, {
        type: 'radar',
        data: data,
        maintainAspectRatio: false,
        responsive: false,
        scaleLineColor : "rgba(255, 255, 255, 0.9)",
        fullWidth: false,
        stacked: true,
        pointDot: false,
        pointLabelFontSize: 20,
        options: {
            defaultColor: "rgba(255, 255, 255, 0.9)",
            defaultFontColor: "rgba(255, 255, 255, 0.9)",
            scaleLineColor: "rgba(255, 255, 255, 0.9)",
            defaultFontSize: 20,
            scale: {
                angleLines: {
                    display: true,
                    color: "rgba(255, 255, 255, 0.3)",
                    lineWidth: 1
                },
                scaleLabel: {
                    display: false,
                    fontSize:10,
                    fontColor: "rgba(255, 255, 255, 0.9)"
                },
                ticks: {
                    display: false,
                    beginAtZero: true
                },
                gridLines: {
                    color: "rgba(255, 255, 255, 0.5)",
                    zeroLineColor: "rgba(255, 255, 255, 0.3)"
                },
                pointLabels: {
                    fontSize: 20,
                    fontColor: "rgba(255, 255, 255, 0.5)"
                }
            }
        }
    });
}