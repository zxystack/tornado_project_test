function logout() {
    $.get("/api/logout", function(data){
        if ('1' == data.errno) {
            location.href = "/";
        }
    })
}

$(document).ready(function(){
	$.post('',function(data){

		if('1'==data.errno){
			$('.menu-text h3').html(data.data.username)
			$('.menu-text h5').html(data.data.mobile)
		}
	})
})