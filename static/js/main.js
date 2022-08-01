$(document).ready(function(){
    $('#image_upload').on('change',function(){
        var fileName = $(this).val().split('\\').pop();
        $(this).next('.custom-file-label').html(fileName);
    })

    // Scroll Animation
    $('.section-link').click(function(){
        var id = $(this).text();
        $("html, body").animate({  scrollTop: $("#"+id).offset().top});
    });
    

});