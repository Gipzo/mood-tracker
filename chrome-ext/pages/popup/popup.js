function checkOrder() {
    $.ajax({
        url: 'http://ip.jsontest.com/?callback=showMyIP',
        data: { },
        dataType: 'json',
        type: 'post',
        success: function (response) {
            alert(response);
        },
        beforeSend: function () { },
        complete: function () { },
    })



    //$(button).html(i)
    setTimeout(checkOrder, 1000);
}
setTimeout(checkOrder, 1000);