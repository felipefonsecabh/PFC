$(document).ready(function(){
	$('#sp_pumpspeed').slider({
		formatter: function(value){
			return 'Current value: ' + value;
		}
	})
})