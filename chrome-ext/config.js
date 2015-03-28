MoodTracker.registerNamespace('MoodTracker.Background.Config')

MoodTracker.Background.Config = {
    urls: {
        moodDataSource: 'http://127.0.0.1:8080/',
        userPicture: 'http://127.0.0.1:8080/image'
    },
    performance: {
        moodUpdateFrequency: 3000,
        userPictureUpdateFrequency: 1000,
        popupChartUpdateFrequency: 200
    }
}