function refresh_function(){
	$.ajax({
		type: 'GET',
		url: 'refresh',
		success: function(data){
			//atualizar os dados dos displays
			$('#Temp1').text(data.Temp1);
			$('#Temp2').text(data.Temp2);
			$('#Temp3').text(data.Temp3);
			$('#Temp4').text(data.Temp4);
			$('#HotFlow').text(data.HotFlow);
			$('#ColdFlow').text(data.ColdFlow);

			//atualizar dados dos stauts on off
			if(data.PumpStatus){
				$('#ps').text = 'ON';
				if($('#ps').hasClass('label-off')){
					$('#ps').toggleClass('label-off label-on');
				}
			}
			else{
				$('#ps').text = 'OFF';
				if($('#ps').hasClass('label-on')){
					$('#ps').toggleClass('label-on label-off');
				}

			}

			if(data.HeaterStatus){
				$('#hs').text = 'ON';
				if($('#hs').hasClass('label-off')){
					$('#hs').toggleClass('label-off label-on');
				}
			}
			else{
				$('#hs').text = 'OFF';
				if($('#hs').hasClass('label-on')){
					$('#hs').toggleClass('label-on label-off');
				}

			}

			//dados analogicos (circle progess bar)
			$('#pb_speed_value').text = data.PumpSpeed;
			var pb_classes  = $('#pb_speed').attr('class').split(' ');
			$('#pb_speed').removeClass(pb_classes[2]);
			$('#pb_speed').addClass('p'+parseInt(data.PumpSpeed));
			if(data.PumpSpeed > 50){
				$('#pb_speed').addClass('over50');
			}
			else{
				//alert($('#pb_speed').hasClass('over50'));
				if($('#pb_speed').hasClass('over50')){	
					$('#pb_speed').removeClass('over50');
				}
				
			}

		}
	})
}

$(document).ready(function(){
	
	//setInterval(refresh_function,2000);
	refresh_function();

	//aqui embaixo setar as funções de comando
	

});