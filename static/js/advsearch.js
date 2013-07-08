
var formFields = {};
var fieldNum = 1;

$(document).ready(function() {
    var formFields = $('#formFields');
    formFields.children('p').each(function(n, item) {
		var field = $(this).find(':input').attr( "name" );
		formFields[field] = $(this);
		$(this).addClass('form_item').hide().children().removeAttr('id').removeAttr('for');
		$(this).append(' <a href="#">Remove</a>');
		var name = $(this).find('label').text();
		$('#fieldList').append('<option value="' + field + '">' + name.substr(0, name.length - 1) + '</option>');
		$(this).detach();
	});

    formFields.remove();

	$('#addField').find('a').click(function( e ) {
		var field = $('#fieldList').val();
		if ( !formFields.hasOwnProperty( field ) )
			return false;
		field = formFields[field].clone();
		field.find('label').attr('for', 'field' + fieldNum);
		field.find(':input').attr('id', 'field' + fieldNum);
		fieldNum++;
		field.insertBefore( $('#addField') ).slideDown(200);
		return false;
	});

	$('form').on( 'click', 'p.form_item a', function(e) {
		$(this).closest('p.form_item').slideUp(150, function() { $(this).remove(); });
		return false;
	});
});