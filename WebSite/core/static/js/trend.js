
var points = [];
var totalPoints = 300;
var cnt=0;

//time series para o smoothie
var Temp1 = new TimeSeries();
var Temp2 = new TimeSeries();
var Temp3 = new TimeSeries();
var Temp4 = new TimeSeries();
var HotFlow = new TimeSeries();
var ColdFlow = new TimeSeries();
var PumpSpeed = new TimeSeries();

function getRandomData() {

	if (points.length > 0)
		points = points.slice(1);

		// Do a random walk
		while (points.length < totalPoints) {
		    var prev = points.length > 0 ? points[points.length - 1] : 50,
			y = prev + Math.random() * 10 - 5;
			if (y < 0) {
			    y = 0;
            } 
            else if (y > 100) {
				y = 100;
			}

			points.push(y);
		}

		// Zip the generated y values with the x values

		var res = [];
		for (var i = 0; i < points.length; ++i) {
			res.push([i, points[i]])
		}

		return res;
}

function getTimeValue(){
    var dateBuffer = new Date();
    var Time = dateBuffer.getTime()/1000;
    return Time;
}

function rand() {
  return Math.random();
}

function getRandomValue(){
    var randomValue = Math.random()*100;
    return randomValue;
}

function refreshCharts(){
    $.ajax({
        type: 'GET',
        url: 'refresh',
        success: function(data){

            var time = data.TimeStamp;
            var timestr = data.StrTs;
            var y = data.Temp2;

            //epoch
            /*areaChartInstance.push([{time:time, y: y}]);

            //Plotly
            Plotly.extendTraces('chart', {
                x: [[ timestr ]],
                y: [[ y ]]
            }, [0], 60)

            cnt++;*/

            //smoothie
            Temp1.append(data.TimeStamp*1000 ,data.Temp1);
            Temp2.append(data.TimeStamp*1000,data.Temp2);
            Temp3.append(data.TimeStamp*1000 ,data.Temp3);
            Temp4.append(data.TimeStamp*1000,data.Temp4);
            HotFlow.append(data.TimeStamp*1000 ,data.HotFlow);
            ColdFlow.append(data.TimeStamp*1000,data.ColdFlow);
            PumpSpeed.append(data.TimeStamp*1000 ,data.PumpSpeed);

        }
    });
}

function setoptions(minVal,maxVal){
    var options = {
        millisPerPixel:51,
        //maxValueScale:1.40,
        //minValueScale:1.37,
        interpolation:'linear',
        scaleSmoothing:0.035,
        grid:{
            fillStyle:'#ffffff',
            strokeStyle:'rgba(119,119,119,0.90)',
            sharpLines:true,
            millisPerLine:4000,
            verticalSections:13
        },
        labels:{fillStyle:'#000000'},
        tooltip:true,
        timestampFormatter:SmoothieChart.timeFormatter,
        maxValue: maxVal,
        minValue: minVal
        //responsive: true
    };
    return options;
}

$(document).ready(function(){

    /*
    $(window).resize(function() {
        var y = $(window).width();
        $('#schart').attr('width', y-100);
    });*/

    /*
    var chartData = [
        {
            label: 'A',
            values: []
        }
    ];
    var areaChartInstance = $('#area').epoch({
        type: 'time.line',
        data: chartData,
        axes: ['left','bottom'],
        range: {left: [-10,30]}
    });

    var layout = {
        //xaxis: {range: [2, 5]},
        yaxis: {range: [-10, 30]}
    };

    Plotly.plot('chart', 
    [{
        x: [-3, -2,-1],
        y: [1,2,3].map(rand)
    }],layout);
    */

    var smoothie1 = new SmoothieChart(setoptions(-10,40));
    var smoothie2 = new SmoothieChart(setoptions(0,30));
    var smoothie3 = new SmoothieChart(setoptions(0,30));
    var smoothie4 = new SmoothieChart(setoptions(0,100));

    //temperaturas quentes
    smoothie1.addTimeSeries(Temp1,{lineWidth:2,strokeStyle:'#900c3f'});
    smoothie1.addTimeSeries(Temp2,{lineWidth:2,strokeStyle:'#ffc300'});
    smoothie1.streamTo(document.getElementById('charttemp1'));

    //temperaturas frias
    smoothie2.addTimeSeries(Temp3,{lineWidth:2,strokeStyle:'#010c5b'});
    smoothie2.addTimeSeries(Temp4,{lineWidth:2,strokeStyle:'#0fe5c2'});
    smoothie2.streamTo(document.getElementById('charttemp2'));

    //vazões
    smoothie3.addTimeSeries(HotFlow,{lineWidth:2,strokeStyle:'#2f4727'});
    smoothie3.addTimeSeries(ColdFlow,{lineWidth:2,strokeStyle:'#42df10'});
    smoothie3.streamTo(document.getElementById('chartflows'));

    //velocidade da bomba
    smoothie4.addTimeSeries(PumpSpeed,{lineWidth:2,strokeStyle:'#142463'});
    smoothie4.streamTo(document.getElementById('chartspeed'));
    

    setInterval(refreshCharts,400);
			
});
    
    



