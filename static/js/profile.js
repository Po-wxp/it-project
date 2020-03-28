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



var menuClicked = localStorage.getItem("menuClicked");

$(document).ready(function(){
    console.log(menuClicked);
    if (menuClicked==1) {
        showAlbum();       
        $('#btn-Album a').addClass('account-nav-click');
    }
    else if (menuClicked==2) {
        console.log( "showFavorite");
        showFavorite();
        $('#btn-Favorite a').addClass('account-nav-click');
    }
    else if (menuClicked==3) {
        showReview();
        $('#btn-Review a').addClass('account-nav-click');
    }
    else if (menuClicked==4) {
        showFollowing();
        $('#btn-Following a').addClass('account-nav-click');
    }
    else if (menuClicked==5) {
        showProfile();
        $('#btn-Profile a').addClass('account-nav-click');
    }
});

$(document).ready(function(){$('#btn-Album').click(function() {
    menuClicked = 1;      
    localStorage.setItem("menuClicked", menuClicked);
    location.reload();

});});

$(document).ready(function(){$('#btn-Favorite').click(function() {

    menuClicked = 2;      
    localStorage.setItem("menuClicked", menuClicked);
    location.reload();

});});

$(document).ready(function(){$('#btn-Review').click(function() {
    menuClicked = 3;      
    localStorage.setItem("menuClicked", menuClicked);
    location.reload();
});});

$(document).ready(function(){$('#btn-Following').click(function() {
    menuClicked = 4;      
    localStorage.setItem("menuClicked", menuClicked);
    location.reload();
});});

$(document).ready(function(){$('#btn-Profile').click(function() {
    menuClicked = 5;      
    localStorage.setItem("menuClicked", menuClicked);
    location.reload();
});});


function showAlbum(){
    $('.photo_area').show();
    clear();
    $('#album_area').show();            
}


function showFavorite(){
    console.log(menuClicked);
    $('.photo_area').show();
    clear();
    $('#favorite_area').show();            
}

function showReview(){
    $('.photo_area').show();
    clear();
    $('#review_area').show();            
}

function showFollowing(){
    $('.photo_area').show();
    clear();
    $('#following_area').show();            
}

function showProfile(){
        $('.profile-area').show();
        $('.account-nav').css("top","3.8rem");   
        $('.account-nav').css("position","fixed");
        $('.account-nav').css("z-index","1031");
        $('.account-nav').css("borderBottom","0.02142857rem solid #bbb");
        $('.photo_area').hide();       
}
