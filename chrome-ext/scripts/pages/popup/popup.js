MoodTracker.registerNamespace('MoodTracker.Popup.Index')

MoodTracker.Popup.Index = MoodTracker.BaseClass.extend({
    _background: null,
    _main: null, // background entry point
    _elements: {
        $chartBox: null,
        $statusValue: null,
        $statusText: null,
        $title: null,
    },
    _colors: {
        surprise: '#FFBF4D',
        happy: '#F29441',
        normal: '#D0D98F',
        sadness: '#76A67D',
        disgust: '#255959'
    },
    _chart: null,
    _pieCharts: {
        surprise: null,
        happy: null,
        normal: null,
        sadness: null,
        disgust: null
    }, // list of 5 pie charts
    _chartDataMaxLength: 16, // number of dataPoints visible at any point
    _moodCoefMultiplier: 100,
    _chartData: null,
    _moodData: {},
    

    init: function (options) {
        MoodTracker.rebindFunctionInstances(this);

        this._background = chrome.extension.getBackgroundPage();
        this._main = this._background.MoodTracker.Background.Main;
        this._chartData = [];

        this._initElements();
        this._chart = this._createChart();
        this._createPieCharts();

        this._refresh(this._updateChart, this._main.config.performance.popupChartUpdateFrequency);
        this._refresh(this._updatePieCharts, this._main.config.performance.popupChartUpdateFrequency);
        this._refresh(this._updateWidgetAppearing, this._main.config.performance.popupChartUpdateFrequency);
        

        // todo <dp> find out how to set body styles for popup
        $('body').css('margin', 0).css('padding', 0);

        this._onUserMoodChange();
        this._onUserPortraitChange();

        return {};
    },

    // public members

    // private members

    _initElements: function(){
        this._elements.$chartBox = $('.popup-chart-box');
        this._elements.$statusValue = $('.popup-valueStatus');
        this._elements.$statusText = $('.popup-textStatus');
        this._elements.$title = $('.popup-title');
    },

    _createChart: function () {
        var that = this,
            initialData = [];

        for (var i = 0; i < this._chartDataMaxLength; i++) {
            that._chartData.push({ x: new Date().getTime(), y: 0 });
        }

        var options = {
            animationEnabled: true,
            //colorSet: "custom1",
            //theme: "theme2",
            backgroundColor: "transparent",
            toolTip: {
                enabled: false
            },
            axisX: {
                gridThickness: 0,
                tickThickness: 0,
                lineThickness: 0,
                labelFontColor: 'transparent'
            },
            axisY: {
                minimum: 0,
                maximum: 100,
                gridThickness: 0,
                tickThickness: 0,
                lineThickness: 0,
                labelFontColor: 'transparent'
            },
            data: [{
                markerSize: 0,
                color: "black",
                fillOpacity: 1,
                lineThickness: 2,
                type: "spline",
                dataPoints: that._chartData
            }]
        };

        //CanvasJS.addColorSet('custom1', ['black']);

        return new CanvasJS.Chart('chartContainer', options);
    },

    _createPieCharts: function(){
        var that = this;

        this._pieCharts.surprise = $('#PieChartSurprise').easyPieChart({
            barColor: that._colors.surprise,
            lineWidth: 4,
            size: 80
        });

        this._pieCharts.happy = $('#PieChartHappy').easyPieChart({
            barColor: that._colors.happy,
            size: 80
        });

        this._pieCharts.normal = $('#PieChartNormal').easyPieChart({
            barColor: that._colors.normal,
            size: 80
        });

        this._pieCharts.sadness = $('#PieChartSadness').easyPieChart({
            barColor: that._colors.sadness,
            size: 80
        });

        this._pieCharts.disgust = $('#PieChartDisgust').easyPieChart({
            barColor: that._colors.disgust,
            size: 80
        });
    },

    _onUserMoodChange: function () {
        var that = this;

        this._main.moodInterface.on('userMoodRefresh', function (moodData) {
            if (moodData) {
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
        var that = this,
            dateTime = new Date().getTime(),
            chartData = this._chartData;

        if (this._moodData.data) {
            console.log(that._moodData.data.main_mood);
            var mainMood = that._moodData.data.main_mood;
            chartData.push({ x: dateTime, y: mainMood * that._moodCoefMultiplier });
        } else {
            chartData.push({ x: dateTime, y: 0});
        }

        chartData.shift();

        this._chart.render();
    },

    _updatePieCharts: function(){
        var that = this,
            chartData = that._chart.options.data[0].dataPoints;

        if (this._moodData.data) {
            var moodCoef = this._moodData.data.mood_coef;

            // name of chart objects are equal to mood object values
            // so use single name
            var updatePieChart = function (name) {
                var value = (moodCoef[name] * that._moodCoefMultiplier).toFixed(0),
                    canvasElement = that._pieCharts[name].children(0).clone();

                that._pieCharts[name][0].childNodes[0].nodeValue = value + '%';
                that._pieCharts[name].data('easyPieChart').update(value);
            }

            updatePieChart('surprise');
            updatePieChart('happy');
            updatePieChart('normal');
            updatePieChart('sadness');
            updatePieChart('disgust');
        }
    },

    _updateWidgetAppearing: function () {
        var that = this;

        if (this._moodData.data) {
            var detectedMood = that._moodData.data.detected_mood,
                mainMood = that._moodData.data.main_mood,
                color = that._colors[detectedMood],
                updateSpeed = this._main.config.performance.moodUpdateFrequency;

            that._elements.$chartBox
                .css('transition-duration', updateSpeed + 'ms')
                .css('transition', color + ' 1000ms linear')
                .css('background-color', color);

            that._elements.$title
                .css('transition-duration', updateSpeed + 'ms')
                .css('transition', color + ' 1000ms linear')
                .css('color', color);

            //that._elements.$statusValue.html((mainMood * that._moodCoefMultiplier).toFixed(0));
            that._elements.$statusText.html(detectedMood);
        }
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