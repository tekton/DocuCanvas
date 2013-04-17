/** include/NavMenu.js **/
var NavMenu = {
    items: [],
    triggers: [],
    mapping: {
        'account' : 'account_nav',
        'projects_list' : 'projects_nav',
        'context' : 'context_nav',
        'search_icon' : 'search_nav'
    },
    _timeout: null,

    ClearDisplayTimeout: function(){
        // Clears display timeout
        if (NavMenu._timeout) {
            clearTimeout(NavMenu._timeout);
        }
    },

    SetDisplayTimeout: function(){
        // Hide any open menu after 5 seconds if: 
        //  Desktop User - mouses out from menu
        //  Mobile User - does not click a menu item
        NavMenu.ClearDisplayTimeout();
        NavMenu._timeout = setTimeout(function(){
            NavMenu.items.slideUp();
        },5000);
    },

    HideAll: function(){
        // Removes any pending timeout since we won't need it
        NavMenu.ClearDisplayTimeout();
        // Hide all visible menu items
        NavMenu.items.slideUp();
    },

    ShowMenu: function(navId,trigger) {
        // Remove 5 second timeout (refer to .SetDisplayTimeout)
        NavMenu.ClearDisplayTimeout();

        // Itterate through all menu items and hide or show them
        NavMenu.items.each(function(i,el){
            el = $(el);

            // Toggle (slide) requested menu
            if (el.attr('id') == navId) {
                // Resets position of NavMenu to be aligned to the bottom left of the triggr
                // Top, Left, and Right attributes removed from CSS
                var offsetHeight = trigger.outerHeight(true),
                    offsetPosition = trigger.offset();

                el.css({
                    top: offsetPosition.top + offsetHeight,
                    left: offsetPosition.left
                });

                el.slideToggle();
            }
            // Hide any other menu
            else {
                el.slideUp();
            }
        });

        // Re-add timeout
        NavMenu.SetDisplayTimeout();
    },

    Init: function(){
        // Get mapped IDs for triggers and menus and put them into a DOM query array
        $.each(NavMenu.mapping, function(k,v){
            NavMenu.triggers.push('#'+k);
            NavMenu.items.push('#'+v);
        });
        NavMenu.items = $(NavMenu.items.join(','));
        NavMenu.triggers = $(NavMenu.triggers.join(','));

        // Bind click event to triggers to show their corresponding menu, based on mapping
        NavMenu.triggers.on("click", function(evt){
            var trigger = $(this),
                navId = NavMenu.mapping[trigger.attr('id')];
            NavMenu.ShowMenu(navId,trigger);
        });


        NavMenu.items.on({
            // Removes display timeout if the user is currently within the menu (desktop users)
            mouseover: NavMenu.ClearDisplayTimeout,

            // Re-add timeout after they mouse over menu
            mouseout: NavMenu.SetDisplayTimeout
        });

        // If user clicks anything other than a menu item or trigger, hide the menus
        $(document).click(function(evt){
            var el = evt.target;

            if ( $.inArray(el, NavMenu.triggers) > -1 || $.inArray(el, NavMenu.items) > -1 ) {
                // Nav menu item was clicked
                return;
            }
           
            if ( $(el).parents('.navitem').length == 0 ) {
                NavMenu.HideAll();
            }
        });

        $('#search').on('click', NavMenu.HideAll);
    }
};