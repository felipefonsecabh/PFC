function getTimeValue(){
    var dateBuffer = new Date();
    var Time = dateBuffer.getTime()/1000;
    return Time;
}

function getRandomValue(){
    var randomValue = Math.random()*100;
    return randomValue;
}

$(document).ready(function(){
    var chartData = [
        {
            label: 'A',
            values: [{time: 1370044800, y:100}, {time: 1370044801, y:80}]
        }
    ];
    var areaChartInstance = $('#area').epoch({
        type: 'time.line',
        data: chartData,
        axes: ['left','bottom']
    });

    $('#rf').click(function(){
        var time = getTimeValue();
        var y = getRandomValue();
        ret = areaChartInstance.push([{time: time, y: y}]);
        alert(ret);
    });
    
});


