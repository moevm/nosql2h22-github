var main = function(){
$('.message a').click(function(){
    $('.register-form').animate({height: "toggle", opacity: "toggle"}, "slow");
    $('.login-form').animate({height: "toggle", opacity: "toggle"}, "slow");
 });
}
$(document).ready(main);
$(document).ready(main_2);
