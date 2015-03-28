MoodTracker.BaseClass = function (dataObject) {
    this.init(dataObject);
};

$.extend(MoodTracker.BaseClass.prototype, {
    init: function (dataObject) { }
});

MoodTracker.BaseClass.extend = function (proto) {
    var base = function () { },
        member,
        that = this,
        subclass = proto && proto.init ? proto.init : function () {
            that.apply(this, arguments);
        },
        fn;

    base.prototype = that.prototype;
    fn = subclass.fn = subclass.prototype = new base();

    for (member in proto) {
        if (proto[member] != null && proto[member].constructor === Object) {
            // Merge object members TODO:TEST IT, merge needs to be implemented.
            fn[member] = $.extend(true, {}, base.prototype[member], proto[member]);
        } else {
            fn[member] = proto[member];
        }
    }

    fn.constructor = subclass;
    subclass.extend = that.extend;

    return subclass;
};