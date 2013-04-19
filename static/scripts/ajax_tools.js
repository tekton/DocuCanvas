
$.fn.asAjax = function( ) {
    var successFunc = null;
    var failFunc = null;
    var urlFunc = null;
    if ( arguments.length > 0 && typeof arguments[0] == "function" )
        successFunc = arguments[0];
    if ( arguments.length > 1 && typeof arguments[1] == "function" )
        failFunc = arguments[1];
    if ( arguments.length > 2 && typeof arguments[2] == "function" )
        urlFunc = arguments[2];
    else
        urlFunc = function() { return $(this).attr('href'); };

    $(this).each( function(i, item) {
        $(item).on( 'click.asAjax', function(e) {
            e.preventDefault();
            var url = urlFunc.apply(this, [i]);
            if ( typeof url == "string" )
                $.get(url, function() { if ( successFunc ) successFunc.apply(item, arguments); } )
                    .fail( function() { if ( failFunc ) failFunc.apply(item, arguments); } );
            return false;
        });
    });
};

