var reviews = 0;

$(document).ready(function(){
    reviews= $('#review_num').text();
    reviews=parseInt(reviews);
    $('#review-btn').text(reviews+' reviews')
})





$(document).ready(function(){
    $('#show_pic_collection_btn').click(function() {
        $.get($(this).data('url'), function(response) {
            console.log(response.message);
            console.log("one");
            if(response.message == "2"){
                $('#show_pic_collection_btn').removeClass( ).addClass("show_pic_collection-btn far fa-bookmark");
            }else if (response.message == "1"){     
                $('#show_pic_collection_btn').removeClass( ).addClass("show_pic_collection-btn fas fa-bookmark");
            }
            
        });
    });
})

// in base.js
// $(document).ready(function(){
//     $(".collection-btn").click(function() {    
//         $.get($(this).data('url'), function(response) {
//             if(response.message == "2"){
//                 $(".collection-btn span").removeClass( ).addClass("collection-btn favorite far fa-bookmark");
//             }else if (response.message == "1"){     
//                 $(".collection-btn span").removeClass( ).addClass("collection-btn favorite fas fa-bookmark");
//             }
//         });    
//     });
// })



// //for related picts
// $(document).ready(function() { 
//     $('.like-btn').click(function() { 
//         var IdVar; 
//         IdVar = $(this).attr('data-photoid');
//         var btn = this;
//         $.get('/capturer/like_photo/', 
//             {'photo_id': IdVar}, 
//             function(data) { 
//                 $('#like_count').html("Likes "+data); 
//                 console.log("hey")
//                 $(btn).children('span').removeClass().addClass('like fas fa-heart'); 
//             })
//     });
// });




$(document).ready(function() { 
    $('#show_pic_like_btn').click(function() { 
        var IdVar; 
        IdVar = $(this).attr('data-photoid');
        var btn = this;
        $.get('/capturer/like_photo/', 
            {'photo_id': IdVar}, 
            function(data) { 
                $('#like_count').html("Likes "+data); 
                $(btn).replaceWith('<span class="like-btn fas fa-heart mr-3"></span>'); 
            })
    });
});

$(document).ready(function(){
    $('#delete_btn').click(function() {
        if(confirm("Are you sure to delete your post?")){
            $.get($(this).data('url'), function(response) {
                window.location.href=document.referrer;
            })
        }
    });
})

$(document).ready(function(){
    $('#review_form').submit(function(event) {
        event.preventDefault();
        $('.error-message').text('');
        CKEDITOR.instances['id_content'].updateElement();
        
        $.ajax({
            url: "{% url 'capturer:upload_comment' photo.id %}",
            type: 'POST',
            data: $(this).serialize(),
            // async: false,
            success: function(data){
                console.log(data);
                if(data['status']=="success"){ 
                    review_html =  '<div class=\"rol mx-0 mb-4\">'+
                                    '<div class=\"col mx-0 px-0 d-flex\">'+
                            '<a href=\"{% url \'capturer:profile\' '+ data['profile_name'] +'\">'+
                            '<img class=\"review-avatar\"src=\"' + data['profile_avatar'] +'\" alt=\"Avatar\" />'+'</a>'+
                            '<div class=\"col mx-0\" style=\"\">'+
                                '<div class=\"row mx-0\">'+
                                '<a class=\"review-author\" href=\"{% url \'capturer:profile\''+ data['profile_name'] +'\">' + data['profile_name'] +'&nbsp;</a>'+
                                '<div class=\"review-content\">'+
                                    data['content']+
                                '</div>'+
                                '</div>'+
                                '<div class=\"row mx-0\">'+
                                    '<span class=\"review-time\">' +' ' +data['date'] + ':'+'</span>'+
                                '</div>'+
                            '</div>'+                               
                        '</div>'+                          
                        '</div>';
                    $('#show_reviews').prepend(review_html)

                    CKEDITOR.instances['id_content'].setData('');
                    reviews=reviews+1;
                        $('#review-btn').text(reviews+' reviews');
                }else{
                    $('.error-message').text(data['message']).show();
                }
            },
            error: function(xhr){
                console.log(data);
            }
        });
        return false;
    });
})

jQuery.fn.center = function () {
this.css("position","absolute");
this.css("top", Math.max(0, (($(window).height() - $(this).outerHeight()) / 2) + 
                                            $(window).scrollTop()) + "px");
this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) + 
                                            $(window).scrollLeft()) + "px");
return this;
}

$(document).ready(function(){
    $('#com_btn').click(function(){
        $('#pic').hide();
        $('#main_panel').css("width","50%");
        $('#main_panel').css("margin","auto");
        $('#main_panel').css("float","none");
        $('#main_panel').css("min-height","500px");
        $('#reviews_panel').show();
        $('.django-ckeditor-widget').find('textarea').text("");
        $('.django-ckeditor-widget').find('textarea').css("placeholder","Write a review!");
        $('#review-back-btn').css("display","block");
        $('#back-btn').css("display","none");
    }); 
})


$(document).ready(function(){
    $('#review-btn').click(function(){
        $('#pic').hide();
        $('#main_panel').css("width","50%");
        $('#main_panel').css("margin","auto");
        $('#main_panel').css("float","none");
        $('#main_panel').css("min-height","500px");
        $('#reviews_panel').show();
        $('#review-back-btn').css("display","block");
        $('#back-btn').css("display","none");           
    });
})






$(document).ready(function(){
    $('#review-back-btn').click(function(){
        $('#pic').show();
        $('#main_panel').css("width","30%");
        $('#main_panel').css("margin","0px");
        $('#main_panel').css("float","left");
        $('#main_panel').css("min-height","auto");
        $('#reviews_panel').hide();
        $('#review-back-btn').css("display","none");
        $('#back-btn').css("display","block");
    });
})

$(document).ready(function(){
    $('#follow-button').click(function() {

        $.get($(this).data('url'), function(response) {
            if(response.message == "2"){
                $('#follow-button').attr("value","Follow")
            }else if (response.message == "1"){
                $('#follow-button').attr("value","Cancel Follow")
            }
        });
    });
})