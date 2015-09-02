// Javascript for step3.html


///////DEFINE VARIABLES/////
var hex;
var obj;
var objData;


///////DEFINE FUNCTIONS////////
function fillSvg(hex){
	obj = document.getElementById("design-object");
	objData = obj.contentDocument;
	console.log(objData);	
	var highWaist = objData.getElementById("highWaist");
	console.log(highWaist);
	var lowWaist = objData.getElementById("lowWaist");
	highWaist.setAttribute('fill', hex);
	lowWaist.setAttribute('fill', hex);
	$('#color-hex').attr('value', hex);
};


$(document).ready( function(){
    ////////GET DATA FROM SERVER////////
	// loads the previous selections via JSON
    $.get('/current-design.json', function (current_design) {
		console.log(current_design);
		$(window).load(function (){
			var obj = document.getElementById("design-object");
			var objData = obj.contentDocument;
			var highWaist = objData.getElementById("highWaist");
			console.log(highWaist);
			var lowWaist = objData.getElementById("lowWaist");
			console.log(current_design.waist_id);

			if(current_design.waist_id == 1){
				highWaist.setAttribute('visibility', 'hidden');
				lowWaist.setAttribute('visibility', 'visible');
			} else {
				highWaist.setAttribute('visibility', 'visible');
				lowWaist.setAttribute('visibility', 'hidden');
			};

			console.log(current_design.color_hex);
			if (current_design.color_id != null && current_design.color_hex != null){
				fillSvg(current_design.color_hex);
			};

		});
	});
	
	$('#fabrics-tab').removeClass('selected');
	$('#colors-tab').addClass('selected');

});

///////////////EVENT HANDLERS///////////////

var colorButtons = $('.color-button');

// changes the color of the pants on click 
$(colorButtons).each( function(){
	$(this).on('click', function(evt) {
		$('.colors').removeClass('nope');
		$('#color-error').remove();
		console.log(evt);
		hex = $(this).attr('hex');
		console.log(hex);
		fillSvg(hex);
	});
});

$('.threads').click( function(evt){
	$('#thread-error').remove();
});

$('.font').click( function(evt){
	$('#font-error').remove();
});

$('.place').click( function(evt){
	$('#place-error').remove();
});

// checks limit on characters allowed in embroidery textarea
$('#embroidery-text').on('blur', function(evt) {
	var textCount = $('#embroidery-text').val().length;
	if(textCount > 50){
		$('#embroidery-text').addClass('nope');
	} else{
		$('#embroidery-text').removeClass('nope');
	};

});

// form validation
$('#color-form').on('submit', function(evt){

	var textCount = $('#embroidery-text').val().length;
	if(textCount > 50){
		evt.preventDefault();
		$('#embroidery-text').addClass('nope');
		$('.text-error').append("<p id='text-error' class='form-error'>custom tag must be 50 characters or less!</p>");
	};
	// color selection is required!
	var colorSelected = $("input[name='color']:checked").length;
	if(colorSelected == 0) {
	   evt.preventDefault();
	   $('.colors').addClass('nope');
	   $('.color-error').append("<p id='color-error' class='form-error'>please select a color!</p>");
	   $("#collapseOne").collapse('show');
	};
	//personalization is not required, but all fields must be selected 
	var customTag = $("input[name='emb-place']:checked").length;
	var fontSelected = $("input[name='stitch']:checked").length;
	var threadSelected = $("input[name='thread']:checked").length;
	// text validation
	if(textCount > 0 && customTag == 0){
		evt.preventDefault();
		$('.place').addClass('nope');
		$('.place-error').append("<p id='place-error' class='form-error'>please select a location for your custom embriodery!</p>");
	};
	if(textCount > 0 && fontSelected == 0){
		evt.preventDefault();
		$('.fonts').addClass('nope');
		$('.font-error').append("<p id='font-error' class='form-error'>please select a font for your custom tag!</p>");
	};
	if(textCount > 0 && threadSelected == 0){
		evt.preventDefault();
		$('.threads').addClass('nope');
		$('.thread-error').append("<p id='thread-error' class='form-error'>please select a thread color for your custom tag!</p>");
	};
	// tag placement validation
	if (customTag != 0 && textCount == 0){
		evt.preventDefault();
		$('#embroidery-text').addClass('nope');
		$('.text-error').append("<p id='text-error' class='form-error'>please add text for your custom tag!</p>");
	};

	if (customTag != 0 && fontSelected == 0){
		evt.preventDefault();
		$('.fonts').addClass('nope');
		$('.font-error').append("<p id='font-error' class='form-error'>please select a font for your custom tag!</p>");
	};

	if (customTag != 0 && threadSelected == 0) {
		   evt.preventDefault();
		   $('.threads').addClass('nope'); 
		   $('.thread-error').append("<p id='thread-error' class='form-error'>please select a thread color for your custom tag!</p>");
		};

	// stitching font validation
	if (fontSelected != 0 && threadSelected == 0) {
		   evt.preventDefault();
		   $('.threads').addClass('nope'); 
		   $('.thread-error').append("<p id='thread-error'class='form-error'>please select a thread color for your custom tag!</p>");
		};

	// threadSelected validation
	if (threadSelected != 0 && fontSelected == 0){
		evt.preventDefault();
		$('.fonts').addClass('nope');
		$('.font-error').append("<p id='font-error' class='form-error'>please select a font for your custom tag!</p>");
	};

	if (threadSelected != 0 && customTag == 0){
		evt.preventDefault();
		$('.place').addClass('nope');
		$('.place-error').append("<p id='place-error' class='form-error'>please select a location for your custom embriodery!</p>");
	};
});	
