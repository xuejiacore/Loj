/**
 * 右侧快速操作
 * kongge@office.weiphone.com
 * 2012.06.07
 */
jQuery(function ($) {
    //创建DOM
    var
        quickHTML = '<div class="quick_links_panel">' +
            '<div id="quick_links" class="quick_links">' +
            '<a href="#top" class="return_top"><i class="top"></i><span>返回顶部</span></a>' +
            '<a href="#" class="my_qlinks"><i class="setting"></i><span>个人中心</span></a>' +
            '</div></div>',
        quickShell = $(document.createElement('div')).html(quickHTML).addClass('quick_links_wrap'),
        quickLinks = quickShell.find('.quick_links');
    quickPanel = quickLinks.parent();
    quickShell.appendTo('body');


    //showQuickPop
    var
        prevPopType,
        prevTrigger,
        doc = $(document),
        popDisplayed = false,
        hideQuickPop = function () {
            if (prevTrigger) {
                prevTrigger.removeClass('current');
            }
            popDisplayed = false;
            prevPopType = '';
            quickPop.hide();
        },
        showQuickPop = function (type) {
            if (quickPopXHR && quickPopXHR.abort) {
                quickPopXHR.abort();
            }
            if (type !== prevPopType) {
                var fn = quickDataFns[type];
                quickPop.html(ds.tmpl(popTmpl, fn));
                fn.init.call(this, fn);
            }
            doc.unbind('click.quick_links').one('click.quick_links', hideQuickPop);

            quickPop[0].className = 'quick_links_pop quick_' + type;
            popDisplayed = true;
            prevPopType = type;
            quickPop.show();
        };
    quickShell.bind('click.quick_links', function (e) {
        e.stopPropagation();
    });

    //通用事件处理
    var
        view = $(window),
        quickLinkCollapsed = !!ds.getCookie('ql_collapse'),
        getHandlerType = function (className) {
            return className.replace(/current/g, '').replace(/\s+/, '');
        },
        showPopFn = function () {
            var type = getHandlerType(this.className);
            if (popDisplayed && type === prevPopType) {
                return hideQuickPop();
            }
            showQuickPop(this.className);
            if (prevTrigger) {
                prevTrigger.removeClass('current');
            }
            prevTrigger = $(this).addClass('current');
        },
        quickHandlers = {
            //购物车，最近浏览，商品咨询
            my_qlinks: showPopFn,
            message_list: showPopFn,
            history_list: showPopFn,
            leave_message: showPopFn,
            //返回顶部
            return_top: function () {
                ds.scrollTo(0, 0);
                hideReturnTop();
            },
            toggle: function () {
                quickLinkCollapsed = !quickLinkCollapsed;

                quickShell[quickLinkCollapsed ? 'addClass' : 'removeClass']('quick_links_min');
                ds.setCookie('ql_collapse', quickLinkCollapsed ? '1' : '', 30);
            }
        };
    quickShell.delegate('a', 'click', function (e) {
        var type = getHandlerType(this.className);
        if (type && quickHandlers[type]) {
            quickHandlers[type].call(this);
            e.preventDefault();
        }
    });

    //Return top
    var scrollTimer, resizeTimer, minWidth = 1350;

    function resizeHandler() {
        clearTimeout(scrollTimer);
        scrollTimer = setTimeout(checkScroll, 160);
    }

    function checkResize() {
        quickShell[view.width() > 1340 ? 'removeClass' : 'addClass']('quick_links_dockright');
    }

    function scrollHandler() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(checkResize, 160);
    }

    function checkScroll() {
        view.scrollTop() > 100 ? showReturnTop() : hideReturnTop();
    }

    function showReturnTop() {
        quickPanel.addClass('quick_links_allow_gotop');
    }

    function hideReturnTop() {
        quickPanel.removeClass('quick_links_allow_gotop');
    }

    view.bind('scroll.go_top', resizeHandler).bind('resize.quick_links', scrollHandler);
    quickLinkCollapsed && quickShell.addClass('quick_links_min');
    resizeHandler();
    scrollHandler();
});
