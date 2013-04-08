$(document).ready(function() {
	var parts = $('#id_date').val().match(/(\d+)/g);
	var d = new Date(parts[0], parts[1]-1, parts[2]); // months are 0-based
	for ( var y = 2013; y <= new Date().getFullYear() + 1; y++ ) {
		$('#goToDate_year').append('<option value="' + y + '">' + y + '</option>');
	}

	$('#goToDate_month').change(function() {
		switch( $(this).val() ) {
			case '1':
			case '3':
			case '5':
			case '7':
			case '8':
			case '10':
			case '12':
				$('#goToDate_day option').show();
				break;
			case '4':
			case '6':
			case '9':
			case '11':
				if ( $('#goToDate_day').val() > 30 )
					$('#goToDate_day').val( 30 );
				$('#goToDate_day option').show();
				$('#goToDate_day option[value=31]').hide();
				break;
			case '2':
				var y = $('#goToDate_year').val();
				var maxDay = ( y % 400 == 0 || ( y % 4 == 0 && y % 100 != 0 ) ) ? 29 : 28;
				if ( $('#goToDate_day').val() > maxDay )
					$('#goToDate_day').val( maxDay );
				for ( var x = maxDay + 1; x <= 31; x++ )
					$('#goToDate_day option[value=' + x + ']').hide();
			}
	});

	$('#goToDate_year').change(function() {
		if ( $('#goToDate_month').val() != 2 )
			return;
		var y = $('#goToDate_year').val();
		var maxDay = ( y % 400 == 0 || ( y % 4 == 0 && y % 100 != 0 ) ) ? 29 : 28;
		if ( $('#goToDate_day').val() > maxDay )
			$('#goToDate_day').val( maxDay );
		for ( var x = maxDay + 1; x <= 31; x++ )
			$('#goToDate_day option[value=' + x + ']').hide();
	});


	$('#goToDate_month').val( d.getMonth() + 1 );
	$('#goToDate_day').val( d.getDate() );
	$('#goToDate_year').val( d.getFullYear() );
	$('#goToDate_month').change();

	$('#goToDate').click(function() {
		var loc = $('#reportForm').attr('action');
		loc += "/" + $('#goToDate_year').val() + "/" + $('#goToDate_month').val() + "/" + $('#goToDate_day').val();
		document.location = loc;
	});
});
