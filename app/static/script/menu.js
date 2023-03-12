var main = function() {
	
	$('.del-repo').click(function() {
        $('#dialog').dialog("open")
    })

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
$(document).ready(main_2);