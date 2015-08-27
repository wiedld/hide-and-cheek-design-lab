// Javascript for step2.html


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
		});
	});
	console.log("ready!");
	$('#styles-tab').removeClass('selected');
	$('#fabrics-tab').addClass('selected');

});
///////////////EVENT HANDLERS///////////////

// shows the fabric description when selected
$('.fabric-button').on('change', function (evt){
	$('#description').remove();
	$('.fabrics').removeClass('nope');
	$('.form-error').remove();

	var descriptionText = $(this).data('extra-text');
	var descriptionImg = $(this).data('image');
	$('#fabric-details').append('<img id="fabric-image"/><span id="description" > ' + descriptionText + '</span>');
	$('#fabric-image').attr('src', '/static/images/' + descriptionImg);
}); 

//validates the form 
$('#fabric-form').on('submit', function(evt){
	var fabricSelected = $("input[name='fabric']:checked").length;
	if(fabricSelected == 0) {
	   //Is not Valid
	   evt.preventDefault();
	   $('.fabrics').addClass('nope');
	   $('.fabric-error').append("<p class='form-error'>please select a fabric!</p>");
	}
});
