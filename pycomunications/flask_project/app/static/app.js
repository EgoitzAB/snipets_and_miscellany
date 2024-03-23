var privateKey = null;

function register() {
  const username = $('#register-username').val();
  const password = $('#register-password').val();
  $.post('/register', { username, password }, function(data) {
    privateKey = data.private_key;
    console.log('Registered:', data);
  }).fail(function() {
    console.log('Error: Could not register.');
  });
}

function login() {
  const username = $('#login-username').val();
  const password = $('#login-password').val();
  $.post('/login', { username, password }, function(data) {
    console.log('Logged in:', data);
  }).fail(function() {
    console.log('Error: Could not log in.');
  });
}

function sendMessage() {
  const recipient = $('#message-recipient').val();
  const message = $('#message-content').val();
  $.get('/public_key', { username: recipient }, function(data) {
    var encrypt = new JSEncrypt();
    encrypt.setPublicKey(data.public_key);
    var encryptedMessage = encrypt.encrypt(message);
    $.post('/send_message', { recipient, message: encryptedMessage }, function(data) {
      console.log('Message sent:', data);
    }).fail(function() {
      console.log('Error: Could not send message.');
    });
  }).fail(function() {
    console.log('Error: Could not get public key.');
  });
}

function getMessages() {
  $.get('/receive_messages', function(data) {
    $('#message-list').empty();
    var decrypt = new JSEncrypt();
    decrypt.setPrivateKey(privateKey);
    data.forEach(function(message) {
      var decryptedMessage = decrypt.decrypt(message.message);
      $('#message-list').append('<li>' + message.sender + ': ' + decryptedMessage + '</li>');
    });
  }).fail(function() {
    console.log('Error: Could not get messages.');
  });
}