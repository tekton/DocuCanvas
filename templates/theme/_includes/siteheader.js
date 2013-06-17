/** theme/_includes/siteheader.js **/
var SiteNav = {
	contextSelector: '#siteheader',
    triggerSelector: '.navitem',
    submenuSelector: '.navitem-sub',
    submenuTriggerCls: '',

    triggers: [],
    submenus: [],

    _timeout: null,
    _submenuTriggerCls: '',
    _submenuActiveCls: '',
    _submenuHiddenCls: '',

    ClearDisplayTimeout: function(){
        // Clears display timeout
        if (SiteNav._timeout) {
            clearTimeout(SiteNav._timeout);
        }
    },

    SetDisplayTimeout: function(){
        // Hide any open menu after 5 seconds if: 
        //  Desktop User - mouses out from menu
        //  Mobile User - does not click a menu item
        SiteNav.ClearDisplayTimeout();
        SiteNav._timeout = setTimeout(function(){
            SiteNav.HideAll();
        },5000);
    },

    HideAll: function(){
        // Removes any pending timeout since we won't need it
        SiteNav.ClearDisplayTimeout();
        // Hide all visible menu items
        SiteNav.submenus.removeClass(SiteNav._submenuActiveCls).addClass(SiteNav._submenuHiddenCls);
        SiteNav.triggers.removeClass(SiteNav._submenuTriggerCls);
    },

    ShowMenu: function(trigger,subMenu) {
        // Hides any active menus5
        SiteNav.HideAll();

        trigger.addClass(SiteNav._submenuTriggerCls);
		subMenu.addClass(SiteNav._submenuActiveCls).removeClass(SiteNav._submenuHiddenCls);
        
        // Re-add timeout
        SiteNav.SetDisplayTimeout();
    },

    Init: function(){

    	// Set class names for the visible/hidden state for the triggers
    	if (!SiteNav.submenuTriggerCls) {
    		SiteNav.submenuTriggerCls = SiteNav.submenuSelector;
    	}
    	SiteNav.submenuTriggerCls = SiteNav.submenuTriggerCls.replace(/\./,'');
    	SiteNav._submenuTriggerCls = SiteNav.submenuTriggerCls + '-active';
    	SiteNav._submenuActiveCls = SiteNav.submenuTriggerCls + '-visible';
    	SiteNav._submenuHiddenCls = SiteNav.submenuTriggerCls + '-hidden';

    	// Put triggers and submenus into array
        SiteNav.triggers = $(SiteNav.contextSelector + ' ' + SiteNav.triggerSelector);
        SiteNav.submenus = $(SiteNav.contextSelector + ' ' + SiteNav.submenuSelector);

        // Bind click event to triggers to show their submenu
        SiteNav.triggers.on('click', function(evt){
            var trigger = $(this),
            	subMenu = trigger.siblings(SiteNav.submenuSelector),
            	activeItem = $(SiteNav.contextSelector + ' .' + SiteNav._submenuTriggerCls);
            	
            if (activeItem[0] == trigger[0]) {
            	SiteNav.HideAll();
            }
            else {
	            SiteNav.ShowMenu(trigger,subMenu);
	        }
        });

        SiteNav.submenus.on({
            // Removes display timeout if the user is currently within the menu (desktop users)
            mouseover: SiteNav.ClearDisplayTimeout,

            // Re-add timeout after they mouse over menu
            mouseout: SiteNav.SetDisplayTimeout
        });

        // If user clicks anything other than a menu item or trigger, hide the menus
        $(document).click(function(evt){
            var el = evt.target,
                $el = $(el);

            if ( $.inArray(el, SiteNav.triggers) > -1 || $.inArray(el, SiteNav.submenus) > -1 ) {
                // Nav menu item was clicked
                return;
            }
           
            // Clicked on an item within a SiteNav menu
            if ( $el.parents(SiteNav.triggerSelector).length == 0 && $el.parents(SiteNav.submenuSelector).length == 0 ) {
                SiteNav.HideAll();
            }
        });

        $('#search').on('click', SiteNav.HideAll);
    }
};

SiteNav.Init();