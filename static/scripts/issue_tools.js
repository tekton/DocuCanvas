
$(document).ready(function() {

    $('a.pin_issue').click(function(e) {
        e.preventDefault();
        $.get($(this).attr('href'), function(data, status) {
            // Hides nav menu only after successful submission
            NavMenu.HideAll();
            if ( data.success ) {
                if ( data.is_pinned ) {
                    $('a.pin_issue').text("Unpin");
                    alert( "Issue pinned" );
                }
                else {
                    $('a.pin_issue').text("Pin");
                    alert( "Issue unpinned" );
                }
            }
            else {
                alert( "Pinning error: " + data.error )
            }
        }).fail(function(xhr, status, e) {
                alert( "Server error: " + e );
            });
        return false;
    });

    $('a.assign_issue').click(function(e) {
        e.preventDefault();
        assignUser($(this).attr('href'), null);
        return false;
    });

    $('#assign_issue_to').click(function(e) {
        e.preventDefault();
        console.log( $('#assigned_user').val() );
        assignUser($(this).attr('data-url'), $('#assigned_user').val());
        return false;
    });

});

function assignUser( url, user_id ) {
    var success = function(data) {
        // Hides nav menu only after successful submission
        NavMenu.HideAll();
        if ( data.success ) {
            if ( data.assigned_to == "self" ) {
                $('a.assign_issue').text( "Unassign" );
                alert( "Issue now assigned to you." );
            }
            else if ( data.assigned_to == "none" ) {
                $('a.assign_issue').text( "Assign to me" );
                alert( "Issue unassigned." );
            }
            else if ( data.assigned_to == "user" ) {
                $('a.assign_issue').text( "Assign to me" );
                alert( "Issue successfully assigned." );
            }
        }
        else {
            alert( "Assigning error: " + data.error );
        }
    };

    var failure = function(xhr, status, e) {
        alert( "Server error: " + e );
    };
    console.log( url + user_id );
    if ( user_id )
        $.get(url + user_id, success).fail( failure );
    else
        $.get(url, success).fail( failure );
}
