$(document).ready(function(){
    // Connection
    const socket = io({autoConnect:true});
    socket.on('connect', function () {
        socket.emit('event', {data: 'Transmission Test Passed'});
    });
    socket.on('disconnect', function () {
        $('#log').append('<br>Disconnected');
    });
    socket.on('response', function (msg) {
        $('#log').append('<br>' + msg.data);
    });
    // HN Page
    $('#hntext-submit').click(function() {
        let hnArr = $('textarea#hnbox').val().split(" ", 10);
        console.log(hnArr);
        socket.emit('patient', hnArr);
        // {#$('#hn-log').append(hnArr);#}
    });
        //{#let add_hn = function () {#}

    $('#add-hn-button').click(function() {
        let count = $('#hn-set').children().length;
        const templateMarkup = $('#hn-template').html();
        let compiledTemplate = templateMarkup.replace(/__prefix__/g, count);
        if (count < $('#hn-MAX_NUM_FORMS').val()){
            $('#hn-set').append(compiledTemplate);
            $('#hn-TOTAL_FORMS').attr('value', count+1);
        }
    });
    $('#remove-hn-button').click(function (){
        let count = $('#hn-set').children().length;
        $('#num').text($('#hn-set:checked').length);
/*{% comment %}                if ($('input:has(DELETE):check').prop('checked')){
                    $(this).parent().remove();
                    $('#hn-TOTAL_FORMS').attr('value', count-1);
                }{% endcomment %}
                {% comment %}if ($('#hn-MAX_NUM_FORMS').val() === 0){

                }{% endcomment %}*/
    });
    $('form#patient').submit(function(event) {
        socket.emit('patient', {
            hn: $('#hn').val(),
            birthdate: $('#birthdate').val(),
            gender: $('#gender').val(),
            name: $('#name').val(),
            register: $('#register').prop('checked')
        });
        return false;
    });
    socket.on('hn_response', function(msg) {
        $('#hn_log').text(msg.data)
        //        {#$('#hn_log').html(msg.data + '<br>' + msg.register)#}
    });

    $('form#visit').submit(function(event) {
        socket.emit('visit', {txn: $('#txn').val(), hn: $('#hn').val()});
        return false;
    });
    socket.on('txn_response', function(msg) {
        $('#txn_log').text(msg.data);
    });

    $('form#item').submit(function(event) {
        socket.emit('item', {ser: $('#ser').val(), txn: $('#txn').val(), hn: $('#hn').val()});
        return false;
    });
    socket.on('ser_response', function(msg) {
        $('#ser_log').text(msg.data);
    });
});