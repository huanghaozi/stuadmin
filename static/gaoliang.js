(function ($) {
    $.fn.GL = function (options) {
        var dataop = {
            ocolor: '',
            oshuru: '',
        };
        var chuancan = $.extend(dataop, options);
        $(this).each(function () {
            var _this = $(this)
            _this.find($(".glnow")).each(function () {
                $(this).css({color: ""});
            });
        });
        if (chuancan.oshuru == '') {
            return false;
        } else {
            var regExp = new RegExp("(" + chuancan.oshuru.replace(/[(){}.+*?^$|\\\[\]]/g, "\\$&") + ")", "ig");
            $(this).each(function () {
                var _this1 = $(this)
                var html = _this1.html();
                var newHtml = html.replace(regExp, '<span class="glnow" style="color:' + chuancan.ocolor + '">' + chuancan.oshuru + '</span>');
                _this1.html(newHtml);
            });
        }
    }
})(jQuery);


