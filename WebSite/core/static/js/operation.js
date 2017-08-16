function refresh_function(){
	$.ajax({
		type: 'GET',
		url: 'refresh',
		success: function(data){
			//atualizar os dados da página
			$('#Temp1').text(data.Temp1);
			$('#Temp2').text(data.Temp2);
		}
	})
}

$(document).ready(function(){
	$('#sp_pumpspeed').slider({
		formatter: function(value){
			return 'Current value: ' + value;
	}}),

	setInterval(refresh_function,2000);
	//refresh_function();

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