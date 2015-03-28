MoodTracker.registerNamespace('MoodTracker.Popup.Index')

MoodTracker.Popup.Index = MoodTracker.BaseClass.extend({
    _$chart: null,
    _background: null,
    _main: null, // background entry point
    _moodData: {},
    _elements: {
        
    },

    init: function (options) {
        MoodTracker.rebindFunctionInstances(this);

        this._background = chrome.extension.getBackgroundPage();
        this._main = this._background.MoodTracker.Background.Main;
        this._$chart = this._createChart();

        this._refresh(this._updateChart, this._main.config.performance.popupChartUpdateFrequency);
        this._onUserMoodChange();
        this._onUserPortraitChange();

        return {};
    },

    // public members

    // private members

    _createChart: function () {
        var time = new Date().getTime();
        return $('#areaChart').epoch({
            type: 'time.line',
            axes: ['bottom', 'left'],
            pixelRatio: 3,
            range: [-100, 100],
            tickFormats: { time: function(d) { return new Date(time*1000).toString(); } },
            data: [{
                label: "Layer 1",
                values: [{ time: time, y: 0 }]
            }]
        });
    },

    _onUserMoodChange: function () {
        var that = this;

        this._main.moodInterface.on('userMoodRefresh', function (moodData) {
            if (moodData) {
                console.log(moodData.data.main_mood);
                that._moodData = moodData;
            }
        });
    },

    // listen to user portrait refresh event
    _onUserPortraitChange: function () {
        this._main.moodInterface.on('userPictureRefresh', function (data) {
            $('#UserPicture').attr('src', data)
        });
    },

    _updateChart: function () {
        var chartData = this._$chart.data,
            time = new Date().getTime(),
            lastDataItemIndex = chartData.length - 1,
            lastChartDataItem = length[lastDataItemIndex],
            lastChartDataItemValues = chartData[lastDataItemIndex].values,
            newDataItemValue = { time: time, y: 0 };

        if (this._moodData.data) {
            console.log(this._moodData.data.main_mood * 100000);
            newDataItemValue = { time: time, y: (this._moodData.data.main_mood * 100000)};
        }

        console.log(newDataItemValue);
        lastChartDataItemValues.push(newDataItemValue);

        //this._chartData[lastDataItemIndex].values.push(lastChartDataItemValue);
        this._$chart.update(chartData);
    },

    _refresh: function (funcToRefresh, timeout) {
        var that = this;

        setTimeout(function () {
            funcToRefresh();
            that._refresh(funcToRefresh, timeout);
        }, timeout);
    },

});

MoodTracker.Popup.Index.Instance = new MoodTracker.Popup.Index({});