
var formFields = {};
var formFieldNames = {};

$(document).ready(function() {
	$('#formFields > p').each(function(n, item) {
		var field = $(this).find(':input').attr( "name" );
		formFields[field] = $(this);
		formFieldNames[field] = $(this).find('label').text();
		$(this).detach();
	});

	for ( field in formFieldNames ) {
		if ( !formFieldNames.hasOwnProperty( field ) )
			continue;
		$('#fieldList').append('<option value="' + field + '">' + formFieldNames[field] + '</option>');
	}

	$('#addField a').click(function( e ) {
		var field = $('#fieldList').val();
		if ( !formFields.hasOwnProperty( field ) )
			return false;
		console.log( field );
		field = formFields[field].clone().hide().insertBefore( $('#addField') ).slideDown(200);
		return false;
	});

	$('form').on( 'click', 'p.form_item a', function(e) {
		$(this).closest('p.form_item').remove();
		return false;
	});
});