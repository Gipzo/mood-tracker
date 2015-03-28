var MoodTracker = function () { };

MoodTracker.registerNamespace = function () {
    var a = arguments, o = null, i, j, d;
    for (i = 0; i < a.length; i = i + 1) {
        d = ("" + a[i]).split(".");
        o = MoodTracker;

        for (j = (d[0] == "MoodTracker") ? 1 : 0; j < d.length; j = j + 1) {
            o[d[j]] = o[d[j]] || {};
            o = o[d[j]];
        }
    }

    return o;
};

MoodTracker.rebindFunctionInstances = function (obj) {
    for (var member in obj) {
        if ($.isFunction(obj[member])) {
            obj[member] = $.proxy(obj[member], obj);
        }
    }
};

MoodTracker.inherit = function (child, parent) {
    $.extend(true, child.prototype, parent.prototype, {
        _callBaseMethod: function (methodName, arg, arg1, arg2, arg3) {
            parent.prototype[methodName].call(this, arg, arg1, arg2, arg3);
        }
    });
};