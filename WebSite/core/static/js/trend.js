

//time series para o smoothie
var Temp1 = new TimeSeries();
var Temp2 = new TimeSeries();
var Temp3 = new TimeSeries();
var Temp4 = new TimeSeries();
var HotFlow = new TimeSeries();
var ColdFlow = new TimeSeries();
var PumpSpeed = new TimeSeries();

function refreshCharts(){
    $.ajax({
        type: 'GET',
        url: 'refresh',
        success: function(data){

            if(!data){
                //retornou vazio
                return;
            }
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
        millisPerPixel:200,
        //maxValueScale:1.40,
        //minValueScale:1.37,
        interpolation:'linear',
        scaleSmoothing:0.165,
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

    var smoothie1 = new SmoothieChart(setoptions(0,60));
    var smoothie2 = new SmoothieChart(setoptions(0,50));
    var smoothie3 = new SmoothieChart(setoptions(0,30));
    var smoothie4 = new SmoothieChart(setoptions(0,110));

    //temperaturas quentes
    smoothie1.addTimeSeries(Temp1,{lineWidth:2,strokeStyle:'#900c3f'});
    smoothie1.addTimeSeries(Temp2,{lineWidth:2,strokeStyle:'#213DEA'});
    smoothie1.streamTo(document.getElementById('charttemp1'));

    //temperaturas frias
    smoothie2.addTimeSeries(Temp3,{lineWidth:2,strokeStyle:'#c88b51'});
    smoothie2.addTimeSeries(Temp4,{lineWidth:2,strokeStyle:'#6F6185'});
    smoothie2.streamTo(document.getElementById('charttemp2'));

    //vazões
    smoothie3.addTimeSeries(HotFlow,{lineWidth:2,strokeStyle:'#2f4727'});
    smoothie3.addTimeSeries(ColdFlow,{lineWidth:2,strokeStyle:'#C4C211'});
    smoothie3.streamTo(document.getElementById('chartflows'));

    //velocidade da bomba
    smoothie4.addTimeSeries(PumpSpeed,{lineWidth:2,strokeStyle:'#142463'});
    smoothie4.streamTo(document.getElementById('chartspeed'));
    

    setInterval(refreshCharts,400);
			
});
    
    



