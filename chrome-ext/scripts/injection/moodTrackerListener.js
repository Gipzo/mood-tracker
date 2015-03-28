


chrome.runtime.onConnect.addListener(function (port) {
    console.assert(port.name == "moodTrackerPort");
    port.onMessage.addListener(function (msg) {
        console.log(msg)

        if (msg.dataType == 'userportrait') {
            $('.b-section-main__col-fig').attr('src', msg.data);
        }
        
        


        //

        //$('.top-search-input').val(input + msg.data.data.current_mood);
    });
});