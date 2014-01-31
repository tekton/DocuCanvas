function toggleHeader(){
	$('#sitenav').toggle();
};

$(function(){
	// Set layout on page load
	$('#container').height($(window).height());
	
	// Adjust layout when window is resized
	$(window).resize(function(){
		$('#container').height($(window).height());
	});
});