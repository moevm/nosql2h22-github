
var main = function() { //главная функция
  
  $('.open-menu').hover(
    function(){
      $('.logo').attr('src', '../static/images/252311.png');
    },
    function(){
      $('.logo').attr('src', '../static/images/25231.png');
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