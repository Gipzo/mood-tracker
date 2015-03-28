MoodTracker.registerNamespace('MoodTracker.Background.Messenger')

MoodTracker.Background.Messenger = MoodTracker.BaseClass.extend({
    _portName: 'moodTrackerPort',
    _config: null,
    _options: {
        main: null
    },

    init: function (options) {
        MoodTracker.rebindFunctionInstances(this);

        this._config = options.main.config;
        this._options = options;

        //this._openConnection();

        return {
            postMessage: this.postMessage
        }
    },

    // public members

    // todo <dp> open connection once and then post multiple messages with this connection
    postMessage: function (data) {
        var that = this;

        chrome.tabs.query({ currentWindow: true, active: true },
           function (tabArray) {
               $.each(tabArray, function (i, tab) {
                   var port = chrome.tabs.connect(tab.id, { name: that._portName });
                   port.postMessage(data);
                   that._port = port;
               });
           }
       )
    },

    // private members

    // open connection between ext. and injected script
    // for currently opened tab
    //_openConnection: function () {
    //    var that = this;
    //}

});