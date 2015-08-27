
////////DEFINE VARIABLES/////
var index;
var style_data;
var svg_path;


///////DEFINE FUNCTIONS////////

function submitSuggestions(evt) {
	evt.preventDefault();
	var suggestions = $("#size-suggestions").val();
	if (suggestions == "") { 
		$("label#suggestions_error").show();
    	$("input#size-suggestions").focus();
    } else {
    	var suggestionInputs = {'suggestions': suggestions};
    	$.post('/suggestions', suggestionInputs, function() {
			$('#suggestions-form').html("<div id='message'></div>");
	        $('#message').html("<p>Suggestions submitted</p>").hide().fadeIn(1500, function() {
	        	$('#suggestion-div').html('<p class="label"> My Suggestions: </p> <p id="submitted-suggestions"></p>');
	        	$('#submitted-suggestions').html(suggestions); 
    		});
    	});
	};
};

function clickStyleHandler(evt){
	index++;
	if (index === style_data.length) {
		index = 0;
	}
	change_svg(style_data, index);
	change_radio(style_data, index);
	$('input[name=waist').val('2');
}

function loadStyleHandler(evt){

	var obj = document.getElementById("design-object");
	var objData = obj.contentDocument;
	var el = objData.getElementById("doll");
	el.addEventListener("click", clickStyleHandler);
}

function change_svg (style_data, index) {
	svg_path = style_data[index].style_svg;
	$('#style-svg').attr('value', svg_path);
	$('.styles').removeClass('nope');
	$('.form-error').remove();
	$('#design-object').remove();
	var newObject = document.createElement('object');
	newObject.setAttribute('data', '/static/svg/'+svg_path);
	newObject.id = 'design-object';
	newObject.className = 'doll';
	newObject.addEventListener('load', loadStyleHandler);
	$('#design-div').append(newObject);
};

function change_radio (style_data, index){
	id = style_data[index].style_id;
	selector_str = '.style-button[value="'+id+'"]';
	$(selector_str).prop("checked", true);
};


function change_waist (){

		var waist = $('#waist').val();
		debugger;
		var obj = document.getElementById("design-object");
		var objData = obj.contentDocument;
		var highWaist = objData.getElementById("highWaist");
		console.log(highWaist);
		var lowWaist = objData.getElementById("lowWaist");
		console.log(lowWaist);

		if (waist == 1) {
			highWaist.setAttribute('visibility', 'hidden');
			lowWaist.setAttribute('visibility', 'visible');
		} else {
			highWaist.setAttribute('visibility', 'visible');
			lowWaist.setAttribute('visibility', 'hidden');
		};

};
		
///////EVENT HANDLERS////////


///// submit custom sizing suggestions
$("#submit-suggestions").click( submitSuggestions);		

// // initial load of event handler: click the image to change the style 
var obj = document.getElementById("design-object");
obj.addEventListener('load', loadStyleHandler);

function setUpPage (){
	console.log("Page is set up now!");

	var styleButtons = $('.style-button'); 

	// click the button to change the style
	$(styleButtons).each( function(idx) {
		$(this).on('click', function(evt) {
			index = $(this).val() - 1;
			$("input[name='waist']").val('2');
			change_svg(style_data, index);
		});	
	});
			 
	// change the slider bar to select waist style
	$('#waist').click( function(evt){
		console.log(evt);
		change_waist();
	});

	// Form validation 
	$('#step1-form').on('submit', function(evt){
		var styleSelected = $("input[name='style']:checked").length;
		if(styleSelected == 0) {
		   //Is not Valid
		   evt.preventDefault();
		   $('.styles').addClass('nope');
		   $('.style-error').append("<p class='form-error'>please select a style!</p>");

		}
	});
		
};



///////////////LOADS THE PAGE///////////////
$(document).ready(function(){
    ////////GET DATA FROM SERVER////////
	$.get('/styles.json', function(data){
				style_data = data.styles;
				index = -1;
				setUpPage();
	});
	 $.get('/current-design.json', function (current_design) {
		console.log(current_design);
		$(window).load(function (){
			
			/////this makes sure that the current design from the session renders when the user hits the back button
			if (current_design.style_id != null && current_design.style_svg != "naked.svg"){
				$('#design-object').attr('data', '/static/svg/'+ current_design.style_svg);

				var waist = $('#waist').val();
				if (waist != 2){
					change_waist();
				};
			};
		});
		// selects step 1:styles in the top process bar
		$('#styles-tab').addClass('selected');
		$('.error').hide();
	
	});
});
