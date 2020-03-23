$(document).ready(function(){
    $('#follow-button').click(function() {
       
        $.get($(this).data('url'), function(response) {
            $('.message-section').text(response.message);
            if($('.message-section').text() == "2"){
                $('#follow-button').attr("value","Follow")
            }else if ($('.message-section').text() == "1"){
                $('#follow-button').attr("value","Cancel Follow")
            }
            
        });
    });
})

$(document).ready(function(){
    $(".collection-btn").click(function() {    
    if ($(this).hasClass("fas")){
        $(this).removeClass( ).addClass("collection-btn favorite far fa-bookmark");
    }else{
       $(this).removeClass( ).addClass("collection-btn favorite fas fa-bookmark");
    }            
     });

});

  $(document).ready(function(){
    $("#follow").click(function() {    
        console.log("123");
    if ($(this).hasClass("cancel-follow")){
        $(this).removeClass( ).addClass("btn btn-outline-light  follow can-follow ");
        $(this).val("Follow");
        $(this).text("Follow");
    }else{
       $(this).removeClass( ).addClass("btn btn-outline-light  follow cancel-follow ");
       $(this).val("Cancel Follow");
        $(this).text("Cancel Follow");
    }            
     });

    });


    $(document).ready(function(){
    $('#follow').click(function() {
        $.get($(this).data('url'), function(response) {
            $('.message-section').text(response.message);
             console.log($('.message-section').text(response.message));
            if($('.message-section').text() == "2"){
             
            }else if ($('.message-section').text() == "1"){
                           console.log("1");
            }
            
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

$(document).ready(function(){
    $('#btn-Favorite').click(function(){
        $('.photo_area').show();
        clear();
        $('#favorite_area').show();            
    })
});

$(document).ready(function(){
    $('#btn-Album').click(function(){
        $('.photo_area').show();
        clear();
        $('#album_area').show();
        

    })
});

$(document).ready(function(){
    $('#btn-Review').click(function(){
        $('.photo_area').show();
        clear();
        $('#review_area').show();

    })
});

$(document).ready(function(){
    $('#btn-Following').click(function(){
        $('.photo_area').show();
        clear();
        $('#following_area').show();

    })
});

function clear(){
        $('.profile-area').hide();
        $('#favorite_area').hide();
        $('#album_area').hide();
        $('#review_area').hide();
        $('#following_area').hide();
        $('.account-nav').css("position","initial");
        $('.account-nav').css("borderBottom","0rem solid #bbb");
};


$(document).ready(function(){
    $('#btn-Profile').click(function() {
        $('.profile-area').show();
        $('.account-nav').css("top","3.8rem");   
        $('.account-nav').css("position","fixed");
        $('.account-nav').css("z-index","1031");
        $('.account-nav').css("borderBottom","0.02142857rem solid #bbb");
        $('.photo_area').hide();
    });
});