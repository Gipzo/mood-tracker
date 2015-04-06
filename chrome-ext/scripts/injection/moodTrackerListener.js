

//var port = chrome.runtime.connect();
var mood_data;
var portait;
window.addEventListener("message",
  function(e) {
	  if (e.data =='get_mood'){
	  window.postMessage(mood_data,'*');
  }
  });

chrome.runtime.onConnect.addListener(function (port) {
    console.assert(port.name == "moodTrackerPort");


	
    port.onMessage.addListener(function (msg) {

        if (msg.dataType == 'userportrait') {
            portait=msg.data;
			//$('.b-teasers-2__teaser-i').attr('style','background-image:url(\''+msg.data+'\'); background-position:contain;');
        }
		
		if (msg.dataType == 'usermood') {
			 mood_data = msg.data;
			//var injectedCode = 'window.userMoodRefresh('+JSON.stringify(msg.data)+');';
			//console.log(chrome);
		    //chrome.tabs.executeScript({
		    //   code: injectedCode
		    // });
			 
			//var script = document.createElement('script');
			//script.appendChild(document.createTextNode('('+ injectedCode +')();'));
			//(document.body || document.head || document.documentElement).appendChild(script);
			
			
		}
        
        


        //

        //$('.top-search-input').val(input + msg.data.data.current_mood);
    });
});