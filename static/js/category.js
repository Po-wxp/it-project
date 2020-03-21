$(document).ready(function(){
    $(".collection-btn").click(function() {    
        $.get($(this).data('url'), function(response) {
            if ($(".collection-btn").hasClass("fas")){
                $(".collection-btn").removeClass( ).addClass("collection-btn favorite far fa-bookmark");
            }else{
                $(".collection-btn").removeClass( ).addClass("collection-btn favorite fas fa-bookmark");
            }   
        });    
    });
})

$(document).ready(function(){
    $(".collection-btn favorite fas fa-bookmark-btn").click(function() {    
        $.get($(this).data('url'), function(response) {
            $(this).removeClass( ).addClass("collection-btn favorite far fa-bookmark");
             
        });    
    });
})


$(document).ready(function() { 
    $('.like-btn').click(function() { 
        var IdVar; 
        
        IdVar = $(this).attr('data-photoid');
        var btn = this;
        $.get('/capturer/like_photo/', 
            {'photo_id': IdVar}, 
            function(data) { 
                $('#like_count').html("Likes "+data); 
                $(btn).replaceWith('<span class="like fas fa-heart"></span>');

            })
    });
});

