var main = function() {
  $('.ch-issues').click(
    function(){
      $('.issues').attr('style', 'display: block');
      $('.pull-requests').attr('style', 'display: none');
      $('.commits').attr('style', 'display: none');
    });

    $('.ch-pr').click(
      function(){
        $('.issues').attr('style', 'display: none');
        $('.pull-requests').attr('style', 'display: block');
        $('.commits').attr('style', 'display: none');
      });
      
      $('.ch-commits').click(
        function(){
          $('.issues').attr('style', 'display: none');
          $('.pull-requests').attr('style', 'display: none');
          $('.commits').attr('style', 'display: block');
        });

  $('.open-menu').click(
    function() {
      $('.menu').animate({left: '0px'}, 200);
      $('body').animate({left: '285px'}, 200);
    });
 
  $('.close-menu').click(
    function() {
      $('.menu').animate({left: '-285px'}, 200);
      $('body').animate({left: '0px'}, 200);
    });
};

$(document).ready(main);