$(document).ready(
    $('.multi-menu .title').on('click', function () {
        console.log('llll')
        $(this).next('.body').toggleClass('hide').parent().siblings('.item').find('.body').addClass('hide');
    })
);