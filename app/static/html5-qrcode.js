!function($){jQuery.fn.extend({html5_qrcode:function(qrcodeSuccess,qrcodeError,videoError){return this.each(function(){var currentElem=$(this),height=currentElem.height(),width=currentElem.width();null==height&&(height=250),null==width&&(width=300);var localMediaStream,vidElem=$('<video width="'+width+'px" height="'+height+'px"></video>').appendTo(currentElem),canvasElem=$('<canvas id="qr-canvas" width="'+(width-2)+'px" height="'+(height-2)+'px" style="display:none;"></canvas>').appendTo(currentElem),video=vidElem[0],canvas=canvasElem[0],context=canvas.getContext("2d"),scan=function(){if(localMediaStream){context.drawImage(video,0,0,307,250);try{qrcode.decode()}catch(e){qrcodeError(e,localMediaStream)}$.data(currentElem[0],"timeout",setTimeout(scan,500))}else $.data(currentElem[0],"timeout",setTimeout(scan,500))};window.URL=window.URL||window.webkitURL||window.mozURL||window.msURL,navigator.getUserMedia=navigator.getUserMedia||navigator.webkitGetUserMedia||navigator.mozGetUserMedia||navigator.msGetUserMedia;var successCallback=function(stream){video.src=window.URL&&window.URL.createObjectURL(stream)||stream,localMediaStream=stream,$.data(currentElem[0],"stream",stream),video.play(),$.data(currentElem[0],"timeout",setTimeout(scan,1e3))};navigator.getUserMedia?navigator.getUserMedia({video:!0},successCallback,function(error){videoError(error,localMediaStream)}):console.log("Native web camera streaming (getUserMedia) not supported in this browser."),qrcode.callback=function(result){qrcodeSuccess(result,localMediaStream)}})},html5_qrcode_stop:function(){return this.each(function(){$(this).data("stream").stop(),clearTimeout($(this).data("timeout"))})}})}(jQuery);
