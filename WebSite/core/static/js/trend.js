$(document).ready(function(){
    var chartData = [
        {
            label: 'Layer 1',
            values: [{time: 1370044800, y:100}, {time: 1370044801, y:1000}]
        },
        {
            label: 'Layer 2',
            values: [{time: 1370044800, y:78}, {time: 1370044801, y:98}]
        },
    ];
    var areaChartInstance = $('#area').epoch({
        type: 'time.line',
        data: chartData
        //axes: ['left','right','bottom']
    });
    
});