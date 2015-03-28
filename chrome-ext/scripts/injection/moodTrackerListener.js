


chrome.runtime.onConnect.addListener(function (port) {
    console.assert(port.name == "moodTrackerPort");
    port.onMessage.addListener(function (msg) {


        if (msg.dataType == 'userportrait') {
            $('img').attr('src', msg.data);
			//$('.b-teasers-2__teaser-i').attr('style','background-image:url(\''+msg.data+'\'); background-position:contain;');
        }
        
        


        //

        //$('.top-search-input').val(input + msg.data.data.current_mood);
    });
});