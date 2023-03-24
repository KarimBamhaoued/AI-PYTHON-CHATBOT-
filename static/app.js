$(function() {
  const $chatSupport = $('.chatbox__support');
  const $chatSupportHeader = $('.chatbox__header');
  const $chatSupportMinimize = $('.chatbox__content--header button.minimize');
  const $chatSupportMessages = $('.chatbox__messages');
  const $chatSupportInput = $('.chatbox__footer input');
  const $chatSupportSend = $('.chatbox__footer button');
  const $chatButton = $('.chatbox__button button');
  const $chatButtonWrapper = $('.chatbox__button-wrapper');

  function setResponse(val) {
    $chatSupportMessages.append('<div><span>' + val + '</span></div>');
  }

  function getBotResponse(userText) {
    $.get('/get', { msg: userText }).done(function(data) {
      setResponse(data);
    });
  }

  $chatButtonWrapper.click(function() {
    $chatSupport.toggleClass('chatbox__support--active');
  });

  $chatButton.click(function() {
    $chatSupport.toggleClass('chatbox__support--active');
  });

  $chatSupportMinimize.click(function() {
    $chatSupport.toggleClass('chatbox__support--active');
  });

  $chatSupportHeader.click(function() {
    $chatSupport.toggleClass('chatbox__support--active');
  });

  $chatSupportSend.click(function(e) {
    e.preventDefault();
    const userText = $chatSupportInput.val();
    if (userText === '') return;
    $chatSupportMessages.append('<div><span>You: </span>' + userText + '</div>');
    $chatSupportInput.val('');
    getBotResponse(userText);
  });

  $chatSupportInput.keypress(function(e) {
    if (e.which === 13) {
      const userText = $chatSupportInput.val();
      if (userText === '') return;
      $chatSupportMessages.append('<div><span>You: </span>' + userText + '</div>');
      $chatSupportInput.val('');
      getBotResponse(userText);
    }
  });
});
