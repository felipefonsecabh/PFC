function refresh_function(gaugeChart){
	$.ajax({
		type: 'GET',
		url: 'refresh',
		success: function(data){

			//atualizar os dados dos displays
			$('#TempA').text(data.Temp1.toFixed(2).replace('.',','));
			$('#TempB').text(data.Temp2.toFixed(2).replace('.',','));
			$('#TempC').text(data.Temp3.toFixed(2).replace('.',','));
			$('#TempD').text(data.Temp4.toFixed(2).replace('.',','));
			$('#Vazao_Quente').text(data.HotFlow.toFixed(2).replace('.',','));
			$('#Vazao_Fria').text(data.ColdFlow.toFixed(2).replace('.',','));

			$('#TimeStamp').text(data.TimeStamp)

			//atualizar os dados dos labels de modo de operação

			//modo arduino local/remoto
			
			var status = 2*data.EmergencyMode + !data.ArduinoMode;

			switch(status){
				case 0: //operação decide
					$('#arduino-mode').text('Remoto');
					if($('#arduino-mode').hasClass('label-danger')){
						$('#arduino-mode').toggleClass('label-danger label-info');
					}
					if($('#operation-mode').hasClass('label-default')){
						$('#operation-mode').toggleClass('label-default label-info');
					}
					operation_process(data); //operacao decide o modo; os demais sempre a operação é bloqueada
					break;
				case 1:
					//alert(1);
					$('#arduino-mode').text('Local');
					if($('#arduino-mode').hasClass('label-danger')){
						$('#arduino-mode').toggleClass('label-danger label-info');
					}
					if($('#operation-mode').hasClass('label-info')){
						$('#operation-mode').toggleClass('label-info label-default');
					}
					disable_commands();
					$('.modeactions').addClass('disabled');
					break;
				case 2:
					//alert(2);
					$('#arduino-mode').text('Emergência');
					if($('#arduino-mode').hasClass('label-info')){
						$('#arduino-mode').toggleClass('label-info label-danger');
					}
					if($('#operation-mode').hasClass('label-info')){
						$('#operation-mode').toggleClass('label-info label-default');
					}
					disable_commands();
					$('.modeactions').addClass('disabled');
					break;
				case 3:
					//alert(3);
					$('#arduino-mode').text('Emergência');
					if($('#arduino-mode').hasClass('label-info')){
						$('#arduino-mode').toggleClass('label-info label-danger');
					}
					if($('#operation-mode').hasClass('label-info')){
						$('#operation-mode').toggleClass('label-info label-default');
					}
					disable_commands();
					$('.modeactions').addClass('disabled');
					break;
			}

			//atualizar apenas o nome do modo de operação
			if(data.OpMode){
				$('#operation-mode').text('Manual');
			}
			else{
				$('#operation-mode').text('Automático');
			}
					
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
			//atualizar o status dos botões de gerenciamento de dados do trend
			if(data.TrendStarted){
				//alert('iniciado');
				if(!$('#start-trend').hasClass('disabled')){
					$('#start-trend').addClass('disabled');
				}
				if($('#stop-trend').hasClass('disabled')){
					$('#stop-trend').removeClass('disabled');
				}
				//alert($('#stop-trend').hasClass('disabled'));
			}
			else{
				//alert('parado');
				if($('#start-trend').hasClass('disabled')){
					$('#start-trend').removeClass('disabled');
				}
				if(!$('#stop-trend').hasClass('disabled')){
					$('#stop-trend').addClass('disabled');
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

			//atualizar dados do gauge
			//gaugeChart.update(data.PumpSpeed);
			gaugeChart.refresh(data.PumpSpeed);
		}
	})
}

function disable_commands(){
	//habilitar os itens
	//alert('desabilitar no automatico');

	$('.slidercmd').slider("disable");
	if(!$('.commandbutton').hasClass("disabled")){
		$('.commandbutton').addClass('disabled');
	}		
}

function enable_commands(){
	//desabilitar os itens
	//alert('habilitar no manual');

	$('.slidercmd').slider("enable");
	if($('.commandbutton').hasClass("disabled")){
		$('.commandbutton').removeClass('disabled');
	}
}

function operation_process(data){

	if(data.OpMode){
		//trocar o texto do modo de operação
		$('#operation-mode').text("Manual")
		enable_commands();
		if(!$('#set-manual').hasClass("disabled")){
			$('#set-manual').addClass("disabled");
		}
		if($('#set-auto').hasClass("disabled")){
			$('#set-auto').removeClass("disabled");
		}
	}
	else{
		//trocar o texto do modo de operação
		$('#operation-mode').text("Automático")
		disable_commands();	
	
		if($('#set-manual').hasClass("disabled")){
			$('#set-manual').removeClass("disabled");
		}
		if(!$('#set-auto').hasClass("disabled")){
			$('#set-auto').addClass("disabled");
		}			
	}
}

$(document).ready(function(){
	
	//aqui embaixo setar as funções de comando
	$('.commandbutton').on('click',function(){
		if(!$(this).hasClass('disabled')){
			var data = {'command':$(this).data('target')};
			$.ajax({
				type: 'POST',
				url: 'command/',
				data: data
			});
		}
	});

	$('#sp_pumpspeed').on('slideStop',function(slideEvt){
		//ajax code here
		data = {'speed': slideEvt.value}
		$.ajax({
			type: 'POST',
			url: 'analogcommand/',
			data: data
		});
	});

	//habilita o uso de confirmações para ações importantes
	$('[data-toggle=confirmation]').confirmation({
		rootSelector: '[data-toggle=confirmation]',
	});


	//retorno das confirmações para fazer as ações
	$('.actions').on('confirmed.bs.confirmation',function(){
		var data = {'command': $(this).data('action')};
		$.ajax({
			type:'POST',
			url: 'command/',
			data: data
		});		
	});

	var dflt = {
      min: 0,
      max: 100,
      donut: true,
      gaugeWidthScale: 0.6,
      counter: true,
	  levelColors:['#167EB9'],
	  decimals:1,
      hideInnerShadow: true,
	  symbol: "%",
	  valueFontSize: "8px",
    }

	var gaugeChart = new JustGage({
		id: "g1",
		value: 0.0,
		defaults:dflt
	});

	setInterval(refresh_function,600,gaugeChart);
});

