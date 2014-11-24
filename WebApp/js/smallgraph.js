var example1 = {
    chart: {
        type: 'line'
    },
    title: {
        text: 'Fruit Consumption'
    },
    xAxis: {
        tickInterval: 1
    },
    series: [{
            data: [1, 2, 4, 8, 16, 32, 64, 128, 256, 512],
            pointStart: 1
                        }, {
            data: [-0.2, 0.8, 5.7, 11.3, 17.0, 22.0, 24.8, 24.1, 20.1, 14.1, 8.6, 2.5]
                        }
                        ]
};

sine = [];
for (var i = 0; i <= 6.4; i += 0.3) {
    sine.push([i, Math.sin(i)]);
};
sine2 = [];
for (var i = 0; i <= 6.4; i += 0.3) {
    sine2.push([i, 2*Math.sin(i)]);
};

var example2 = {
    chart: {
        type: 'line',
        renderTo: 'container2',
    },
    title: {
        text: ''
    },
    xAxis: {
        tickInterval: 1,
        lineColor: 'transparent',
        labels: {
            enabled: false
        },
        minorTickLength: 0,
        tickLength: 0
    },
    yAxis: {
        title: {
            text: ''
        },
        labels: {
            enabled: false
        },
        minorGridLineWidth: 0,
        gridLineWidth: 0,
    },

    series: [
        {
            showInLegend: false,
            name: 'sensor 1',
            data: sine,
            pointStart: 1
                    },
                ],

    credits: {
        enabled: false
    },
}

example3 = {
            chart: {
                type: 'spline',
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
                events: {
                    load: function () {

                        // set up the updating of the chart each second
                        var series = this.series[0];
                        setInterval(function () {
                            var x = (new Date()).getTime(), // current time
                                y = Math.random();
                            series.addPoint([x, y], true, true);
                        }, 1000);
                    }
                }
            },
            title: {
                text: 'Live random data'
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150
            },
            yAxis: {
                title: {
                    text: 'Value'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function () {
                    return '<b>' + this.series.name + '</b><br/>' +
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                        Highcharts.numberFormat(this.y, 2);
                }
            },
            legend: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: 'Random data',
                data: (function () {
                    // generate an array of random data
                    var data = [],
                        time = (new Date()).getTime(),
                        i;

                    for (i = -19; i <= 0; i += 1) {
                        data.push({
                            x: time + i * 1000,
                            y: Math.random()
                        });
                    }
                    return data;
                }())
            }]
        };