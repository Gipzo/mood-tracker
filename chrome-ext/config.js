MoodTracker.registerNamespace('MoodTracker.Background.Config')

MoodTracker.Background.Config = {
    urls: {
        moodDataSource: 'http://127.0.0.1:8080/',
        userPicture: 'http://127.0.0.1:8080/image'
    },
	
    performance: {
        moodUpdateFrequency: 200,
        userPictureUpdateFrequency: 2000,
        popupChartUpdateFrequency: 50
    }
}