MoodTracker.registerNamespace('MoodTracker.Background.Main')

MoodTracker.Background.MainClass = MoodTracker.BaseClass.extend({
    // namespaces
    config: null,
    messenger: null,
    moodInterface: null,
    _dataType: {
        userMood: 'usermood',
        userPortrait: 'userportrait',
    },

    init: function (options) {
        MoodTracker.rebindFunctionInstances(this);

        this._initNamespaces();
        this._runListeners();

        return {
            config: this.config,
            messenger: this.messenger,
            moodInterface: this.moodInterface
        };
    },

    // private memebers

    _initNamespaces: function () {
        this.config = MoodTracker.Background.Config;

        this.messenger = this.moodInterface = new MoodTracker.Background.Messenger({
            main: this
        });

        this.moodInterface = new MoodTracker.Background.MoodInterface({
            main: this
        });
    },

    _runListeners: function () {
        var that = this;

        this.moodInterface.on('userMoodRefresh', function (data) {
            that._userMoodRefreshEventHandler(data);
        });

        this.moodInterface.on('userPictureRefresh', function (data) {
            that._userPictureRefreshEventHandler(data);
        });
    },

    _userMoodRefreshEventHandler: function (data) {
        this.messenger.postMessage({
                dataType: this._dataType.userMood,
                data: data
            });
    },

    _userPictureRefreshEventHandler: function (data) {
        this.messenger.postMessage({
            dataType: this._dataType.userPortrait,
            data: data
        });
    }
});

MoodTracker.Background.Main = new MoodTracker.Background.MainClass({});