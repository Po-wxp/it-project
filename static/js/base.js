var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
var currentScrollPos = window.pageYOffset;
var heightOfMainNav = document.getElementById("navbar").getBoundingClientRect().bottom;
var accountNav =  document.getElementById('account-nav');

if (typeof(accountNav) != 'undefined' && accountNav != null)
{      
        console.log("s");
        var accountNavBottom = accountNav.getBoundingClientRect().bottom+50;
        if (prevScrollpos > currentScrollPos) {

            document.getElementById("navbar").style.top = "0";
            document.getElementById("navbar").style.borderBottom="0rem solid #bbb";
        
            console.log(heightOfMainNav);
            accountNav.style.top ="3.8rem";
            accountNav.style.position= "fixed";
            accountNav.style.borderBottom="0.02142857rem solid #bbb";
            accountNav.style.zIndex= "1031";
        }
        if(accountNavBottom > currentScrollPos){
            accountNav.style.position= "initial";
            accountNav.style.borderBottom="0rem solid #bbb";
        }
        else if (prevScrollpos < currentScrollPos) {
            accountNav.style.top = "-200px";
            accountNav.style.borderBottom="0rem solid #bbb";
            document.getElementById("navbar").style.top = "-100px";
        }
}

if (prevScrollpos > currentScrollPos) {

        document.getElementById("navbar").style.top = "0";

} else {
        document.getElementById("navbar").style.top = "-100px";
}

        prevScrollpos = currentScrollPos;
}


$("#categories_menu").on('click', 'a', function(){
        console.log("1");
        $("#dropdownMenuButton").html($(this).text() + ' <span class="caret"></span>');
        $("#dropdownMenuButton").val($(this).data('value'));
});    


var menuClicked = localStorage.getItem("menuClicked");
        //Create the input element
$(document).ready(function(){
        if (!$('#btn-Album').length){
                menuClicked=1;
                localStorage.setItem("menuClicked", menuClicked);
        }
});

$(document).ready(function(){
        console.log("21");    
        $("#id_Description").attr("placeholder","Description");
        $("#id_Title").attr("placeholder","Title");
});

$(document).ready(function() { 
        $('.btn-post-close').click(function() { 
        $("#id_Image").val('');
        $(".upload-img").hide();
        $('#tags_area').empty();
        $('#myInput').val('');
        $('.post-photo-panel').hide();
        $("#id_Description").val("");
        $("#id_Title").val("");
        $("#dropdownMenuButton").html("Select a category" + ' <span class="caret"></span>');
        });

});

$(document).ready(function() { 
        $('.btn-nav-post').click(function() { 
            $('.post-photo-panel').show();
        });
});


//clear search text when user add

$(document).ready(function(){$('#myDropdown').on('click', 'a', function() {

        var val = $(this).text();
        console.log(val);
        $('#myInput').val(val);
        $("#myDropdown").hide();
});});


function searchTag(){ //show dropdown
        $("#myDropdown").show();
};
$(document).on('click','#delete_tag',function(){//do something})

            var node =$(this).parent();
            var node2 =$(this).parent().parent();
            console.log(node);
            console.log(node2);
            $(node).remove();
        
});

$(document).mouseup(function(e)  //hide search dropdown
        {
        var container = $("#myDropdown");
        // if the target of the click isn't the container nor a descendant of the container
        if (!container.is(e.target) && container.has(e.target).length === 0) 
        {
            container.hide();
        }
});


function filterFunction() {
        var input, filter, ul, li, a, i;
        input = document.getElementById("myInput");
        filter = input.value.toUpperCase();
        div = document.getElementById("myDropdown");
        a = div.getElementsByTagName("a");
        for (i = 0; i < a.length; i++) {
            txtValue = a[i].textContent || a[i].innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    a[i].style.display = "";
            } else {
                    a[i].style.display = "none";
            }
        }
}

$('#add_tag').click(function(){
        var tag = $('#myInput').val()
        $("#myDropdown.a").filter(function() {
            return $(this).text() === tag;
        }).css("display", "none");
tag=tag.trim();
if(tag!=''&&tag!=null){
$('#tags_area').append( '<div class="tag" id="tag">'+
                    '<span class="fas fa-tag"></span>'+
            '<span> </span>'+'<span >'+tag+'</span>'+'<button type="button" id="delete_tag" ><span class="fas fa-times"></span></button></div>');
$('#tags_data_area').val($('#tags_data_area').val() + tag+' ');
$('#myInput').val("");}
console.log($('#tags_data_area').val());
});


$(document).ready(function(){
        $("#id_Image").change(function () {
            if (typeof (FileReader) != "undefined") {
                    var reader = new FileReader();
                    reader.onload = function (e) {
                            $(".upload-img").attr('src',e.target.result)
                            
                    }
                    $(".upload-img").show();
                    reader.readAsDataURL($(this)[0].files[0]);
            } else {
            alert("This browser does not support FileReader.");
            }
        });
});


        $(document).ready(function(){
                $(".collection-btn").click(function() {    
                var btn = $(this).children('span')
                $.get($(this).data('url'), function(response) {
                        console.log($(this).children());
                        if(response.message == "2"){              
                        btn.removeClass( ).addClass("favorite far fa-bookmark");
                        }else if (response.message == "1"){     
                        btn.removeClass( ).addClass("favorite fas fa-bookmark");
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
                    console.log("hey")
                    $(btn).children('span').removeClass().addClass('like fas fa-heart'); 
                })
        });
    });
    