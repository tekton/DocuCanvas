
var sYear;
var sMonth;
var sDay;

$(document).ready(function() {
    sYear = $('#goToDate_year');
    sMonth = $('#goToDate_month');
    sDay = $('#goToDate_day');

	var parts = $('#id_date').val().match(/(\d+)/g);
	var d = new Date(parts[0], parts[1]-1, parts[2]); // months are 0-based
    for ( var y = 2013; y <= new Date().getFullYear() + 1; y++ ) {
		sYear.append('<option value="' + y + '">' + y + '</option>');
	}

	sMonth.change(function() {
        switch( $(this).val() ) {
			case '1':
			case '3':
			case '5':
			case '7':
			case '8':
			case '10':
			case '12':
                sDay.find('option').show();
				break;
			case '4':
			case '6':
			case '9':
			case '11':
				if ( sDay.val() > 30 )
					sDay.val( 30 );
				sDay.find('option').show();
				sDay.find('option[value=31]').hide();
				break;
			case '2':
				var y = $('#goToDate_year').val();
				var maxDay = ( y % 400 == 0 || ( y % 4 == 0 && y % 100 != 0 ) ) ? 29 : 28;
				if ( sDay.val() > maxDay )
					sDay.val( maxDay );
				for ( var x = maxDay + 1; x <= 31; x++ )
					sDay.find('option[value=' + x + ']').hide();
			}
	});

	sYear.change(function() {
		if ( $('#goToDate_month').val() != 2 )
			return;
		var y = $('#goToDate_year').val();
		var maxDay = ( y % 400 == 0 || ( y % 4 == 0 && y % 100 != 0 ) ) ? 29 : 28;
		if ( sDay.val() > maxDay )
            sDay.val( maxDay );
		for ( var x = maxDay + 1; x <= 31; x++ )
            sDay.find('option[value=' + x + ']').hide();
	});


	sMonth.val( d.getMonth() + 1 );
    sDay.val( d.getDate() );
	sYear.val( d.getFullYear() );
	sMonth.change();

	$('#goToDate').click(function() {
		var loc = $('#reportForm').attr('action');
		loc += "/" + sYear.val() + "/" + sMonth.val() + "/" + sDay.val();
		document.location = loc;
	});
});
