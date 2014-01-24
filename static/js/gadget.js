

var AlertMessage = (function(){
    var msgContainer = $('#pagemessage');
    if (msgContainer.length == 0) {
        msgContainer = $('<div/>');
    }
    return {
        msgContainer: msgContainer,
        tmpl: function(cls,msg,block,closable) {
            closable = typeof(closable) == 'boolean' ? closable : true;
            block = typeof(block) == 'boolean' ? block : false;

            cls = cls ? ' alert-' + cls : '';
            blockCls = block ? ' alert-block' : '';

            var html = '' +
            '<div class="alert' + cls + blockCls + '">' +
              (closable ? '<button type="button" class="close" data-dismiss="alert">&times;</button>' : '') +
              msg +
            '</div>';

            return $(html);
        },
        _showMsg: function(alertEl,targetEl) {
            console.log(arguments);
            targetEl = targetEl || AlertMessage.msgContainer;
            targetEl.prepend(alertEl);
            alertEl.delay(3000).fadeOut('normal',function(){
                $(this).remove();
            });
        },
        warn: function(msg,targetEl,block,closable) {
            var alertEl = AlertMessage.tmpl(null,msg,block,closable);
            AlertMessage._showMsg(alertEl,targetEl);
        },
        info: function(msg,targetEl,block,closable) {
            var alertEl = AlertMessage.tmpl('info',msg,block,closable);
            AlertMessage._showMsg(alertEl,targetEl);
        },
        error: function(msg,targetEl,block,closable) {
            var alertEl = AlertMessage.tmpl('error',msg,block,closable);
            AlertMessage._showMsg(alertEl,targetEl);
        },
        success: function(msg,targetEl,block,closable) {
            var alertEl = AlertMessage.tmpl('success',msg,block,closable);
            AlertMessage._showMsg(alertEl,targetEl);
        },
        genericUnknownError: function(){
            AlertMessage.error('<strong>Unknown Error!</strong> An unknown error has occured. Try again later.');
        }
    };
})();

// Hides sidebar
$("#metainfo-toggle").click(function(){
    var btn = $(this),
        icon = btn.children('i').first(),
        parent = btn.parents('aside.metainfo'),
        sideColumn = parent.parents('.metainfo-asidecolumn'),
        mainColumn = sideColumn.siblings('.metainfo-maincolumn');

    if (parent.hasClass('metainfo-show')) {
        icon.removeClass('icon-resize-small').addClass('icon-resize-full');
        parent.removeClass('metainfo-show').addClass('metainfo-hide');
        mainColumn.removeClass('span9').addClass('span11');
        sideColumn.removeClass('span3').addClass('span1');
    }
    else {
        icon.removeClass('icon-resize-full').addClass('icon-resize-small');
        parent.removeClass('metainfo-hide').addClass('metainfo-show');
        mainColumn.removeClass('span11').addClass('span9');
        sideColumn.removeClass('span1').addClass('span3');
    }
});

$(".table-sortable").tablesorter();

 $('.control-group-datefield a.add-on:has("i.icon-calendar")').click(function(evt){
    evt.preventDefault();
    $(this).siblings('input.hasDatepicker').focus();
 });