MoodTracker.registerNamespace('MoodTracker.Background.MoodInterface')

MoodTracker.Background.MoodInterface = MoodTracker.BaseClass.extend({
    _config: null,
    _options: {
        main: null
    },
    _eventNames: {
        userMoodRefresh: 'userMoodRefresh',
        userPictureRefresh: 'userPictureRefresh'
    },
    _eventSubcribtions: [],

    init: function (options) {
        MoodTracker.rebindFunctionInstances(this);
		
        this._config = options.main.config;
        this._options = options;

        this._refresh(this._refreshMoodState, this._config.performance.moodUpdateFrequency);
        this._refresh(this._refreshUserPicture, this._config.performance.userPictureUpdateFrequency);

        return {
            on: this.on
        }
    },

    // public members

    on: function (eventName, handler) {
        this._eventSubcribtions.push({ name: eventName, handler: handler });
    },

    // private members

    _refreshMoodState: function () {
        var that = this,
            exMessage = 'An error occured while refreshing user state.';

        $.ajax({
            url: that._options.main.config.urls.moodDataSource,
            data: {},
            dataType: 'json',
            type: 'get',
            timeout: 10000,
            crossDomain: true,
            success: function (response) {
                if (response.data) {
                    that._fire(that._eventNames.userMoodRefresh, response);
                } else {
                    console.log(exMessage)
                    that._fire(that._eventNames.userMoodRefresh, null);
                }
            },
            error: function () {
                console.log(exMessage)
                that._fire(that._eventNames.userMoodRefresh, null);
            }
        })
    },

    // permanently checks for a user's picture
    // and stores the results as a local variable (url)
    _refreshUserPicture: function () {
        var url = this._options.main.config.urls.userPicture + "?date=" + new Date().getTime();
        this._fire(this._eventNames.userPictureRefresh, url);
    },

    _refresh: function (funcToRefresh, timeout) {
        var that = this;

        setTimeout(function () {
            funcToRefresh();
            that._refresh(funcToRefresh, timeout);
        }, timeout);
    },

    _fire: function (eventName, data) {
        // call function if exists
        if ($.isFunction(this[eventName])) {
            this[eventName]();
        }

        // then call external subscribers (if exists)
        var subcribtions = [];
        $.each(this._eventSubcribtions, function (i, subscriber) {
            if (subscriber.name == eventName) {
                if (subscriber.handler != null && $.isFunction(subscriber.handler)) {
                    subscriber.handler(data);
                }
            }
        });
    },
});