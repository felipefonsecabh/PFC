function refresh_function(){
	$.ajax({
		type: 'GET',
		url: 'refresh',
		success: function(data){
			//atualizar os dados da página
			alert(data.Temp1);
		}
	})
}

$(document).ready(function(){
	$('#sp_pumpspeed').slider({
		formatter: function(value){
			return 'Current value: ' + value;
	}}),

	//setInterval(refresh_function,1000);
	refresh_function();

});

/*$.ajax({
	type: 'GET',
	url: '/refresh/',
	success: function(data){
		//atualizar os dados da página
		alert(data);
	}

})*/

/*.done(function(response){
	alert(response);
})*/