// $(function(){
// 	$('button').click(function(){
// 		var user = $('#inputUsername').val();
// 		var pass = $('#inputPassword').val();
// 		$.ajax({
// 			url: '/signUpUser',
// 			data: $('form').serialize(),
// 			type: 'POST',
// 			success: function(response){
// 				console.log(response);
// 			},
// 			error: function(error){
// 				console.log(error);
// 			}
// 		});
// 	});
// });


$(function(){
	$('checkbox').click(function(e){
		var $form = $(this);
		var $error = $form.find(".error");
		var dataform = $form.serialize();

		$.ajax({
			url: '/toggleUpdate',
			data: dataform , //$('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
		e.preventDefault();
	});
});
