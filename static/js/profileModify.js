$(document).ready(function(){
    $("#id_image").change(function () {
           console.log("2");
           if (typeof (FileReader) != "undefined") {
                  var reader = new FileReader();
                  reader.onload = function (e) {
                         $(".edit-avatar").attr('src',e.target.result)
                         
                  }
                   $(".edit-avatar").show();
                  reader.readAsDataURL($(this)[0].files[0]);
           } else {
           alert("This browser does not support FileReader.");
           }
    });
});