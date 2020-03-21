$(document).ready(function(){
    $("#id_image").change(function () {
        if (typeof (FileReader) != "undefined") {
            var reader = new FileReader();
            reader.onload = function (e) {
                    $(".sign-up-avatar").attr('src',e.target.result)
                    
            }
            $(".sign-up-avatar").show();
            reader.readAsDataURL($(this)[0].files[0]);
        } else {
        alert("This browser does not support FileReader.");
        }
    });
});