function refresh_function(){
	$.ajax({
		type: 'GET',
		url: 'refresh',
		success: function(data){
			//atualizar os dados dos displays
			$('#Temp1').text(data.Temp1.toFixed(2).replace('.',','));
			$('#Temp2').text(data.Temp2.toFixed(2).replace('.',','));
			$('#Temp3').text(data.Temp3.toFixed(2).replace('.',','));
			$('#Temp4').text(data.Temp4.toFixed(2).replace('.',','));
			$('#HotFlow').text(data.HotFlow.toFixed(2).replace('.',','));
			$('#ColdFlow').text(data.ColdFlow.toFixed(2).replace('.',','));

			//atualizar dados dos stauts on off
			if(data.PumpStatus){
				$('#ps').text('ON');
				if($('#ps').hasClass('label-off')){
					$('#ps').toggleClass('label-off label-on');
				}
			}
			else{
				$('#ps').text('OFF');
				if($('#ps').hasClass('label-on')){
					$('#ps').toggleClass('label-on label-off');
				}

			}

			if(data.HeaterStatus){
				$('#hs').text('ON');
				if($('#hs').hasClass('label-off')){
					$('#hs').toggleClass('label-off label-on');
				}
			}
			else{
				$('#hs').text('OFF');
				if($('#hs').hasClass('label-on')){
					$('#hs').toggleClass('label-on label-off');
				}

			}

			//dados analogicos (circle progess bar)
			$('#pb_speed_value').text(data.PumpSpeed.toFixed(1).replace('.',',') +'%');
			
			var pb_classes  = $('#pb_speed').attr('class').split(' ');

			if($('#pb_speed').hasClass('over50')){
				//alert(pb_classes[4]);
				$('#pb_speed').removeClass(pb_classes[4]) 
				if(data.PumpSpeed <= 50){
					$('#pb_speed').removeClass('over50');
				}
				$('#pb_speed').addClass('p'+ parseInt(data.PumpSpeed));
				//alert('p'+parseInt(data.PumpSpeed));
			}
			else{
				//alert(pb_classes[2]);
				$('#pb_speed').removeClass(pb_classes[2]);
				if(data.PumpSpeed > 50){
					$('#pb_speed').addClass('over50');
				}
				$('#pb_speed').addClass('p'+parseInt(data.PumpSpeed));
			}	
		}
	})
}

$(document).ready(function(){
	
	setInterval(refresh_function,1000);
	//refresh_function();

	//aqui embaixo setar as funções de comando
	$('.commandbutton').click(function(){
		data = {'command':$(this).data('target')};
		$.ajax({
			type: 'POST',
			url: 'command/',
			data: data
		})
	});

	$('#sp_pumpspeed').on('slideStop',function(slideEvt){
		//ajax code here

	});

	//habilita o uso de confirmações para ações importantes
	$('[data-toggle=confirmation]').confirmation({
		rootSelector: '[data-toggle=confirmation]',
	});

	//retorno das confirmações para fazer as ações
	$('.actions').on('confirmed.bs.confirmation',function(){
		data = {'command': $(this).data('action')};
		$.ajax({
			type:'POST',
			url: 'command/',
			data: data
		});		
	});
});