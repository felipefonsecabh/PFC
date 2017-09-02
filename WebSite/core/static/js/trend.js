function getTimeValue(){
    var dateBuffer = new Date();
    var Time = dateBuffer.getTime()/1000;
    return Time;
}

function getRandomValue(){
    var randomValue = Math.random()*100;
    return randomValue;
}

function refreshCharts(areaChartInstance){
    //atualizar os gráficos aqui
    $.ajax({
        type: 'GET',
        url: 'refresh',
        success: function(data){
            epochtime = int(time.mktime(data.TimeStamp.timetuple())*1000)
            y = data.Temp1
            areaChartInstance.push([{time:epochtime, y: y}]);
        }
    })
}

$(document).ready(function(){
    var chartData = [
        {
            label: 'A',
            values: []
        }
    ];
    var areaChartInstance = $('#area').epoch({
        type: 'time.line',
        data: chartData,
        axes: ['left','bottom']
    });

    
    /*$('#rf').click(function(){
        var time = getTimeValue();
        var y = getRandomValue();
        ret = areaChartInstance.push([{time: time, y: y}]);
        alert(ret);
    });*/

    setInterval(refreshCharts,400,areaChartInstance);
    
});


