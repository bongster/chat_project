var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');

var sendMessage = function (msg) {
    // send message 버튼을 클릭했을 경우에 호출되는 함수.
    console.log(`call sendMessage function: ${msg}`);
    return jQuery.ajax({
      type: 'POST',
      url: '/api/messages',
      dataType: 'json',
      headers:{"X-CSRFToken": $crf_token},
      data: {
          msg: msg,
          room_id: $("#pk").val(),
      },
    }).then(function (data) {
      window.location.reload();
    })
};

var createRoom = function (data) {
  return jQuery.ajax({
      type: 'POST',
      url: '/api/rooms',
      dataType: 'json',
      headers:{"X-CSRFToken": $crf_token},
      data: data,
  }).then(function (data) {
      window.location.href = `/rooms/${data.id}`;
  })
};

var addUser = function (data) {
    return jQuery.ajax({
        type: 'POST',
        url: `/api/rooms/${data.room_id}/users`,
        dataType: 'json',
        headers:{"X-CSRFToken": $crf_token},
        data: data,
    }).then(function (data) {
        window.location.href = `/rooms/${data.room_id}`;
    })
  };

var removeUser = function (data) {
    return jQuery.ajax({
        type: 'DELETE',
        url: `/api/rooms/${data.room_id}/users`,
        dataType: 'json',
        headers:{"X-CSRFToken": $crf_token},
        data: data,
    }).then(function (data) {
        window.location.href = `/rooms/${data.room_id}`;
    })
};

$('#createRoomForm').on('submit', function (e) {
    console.log('click #createMessageForm');
    e.preventDefault();
    return createRoom({name: $("#recipient-name").val(), description: $("#recipient-name").val()});
})

$('#addUserForm').on('submit', function (e) {
    e.preventDefault();
    return addUser({
        room_id: $('#pk').val(),
        user_id: $('#user_id').val(),
    });
});


// Chat.init();
