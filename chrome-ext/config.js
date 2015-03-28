MoodTracker.registerNamespace('MoodTracker.Background.Config')

MoodTracker.Background.Config = {
    urls: {
        moodDataSource: 'http://10.168.1.50:8080/',
        userPicture: 'http://10.168.1.50:8080/image'
    },
    performance: {
        moodUpdateFrequency: 3000,
        userPictureUpdateFrequency: 3000,
        popupChartUpdateFrequency: 200
    }
}