jQuery(document).ready(function($){
    //uprava zobrazovania tooltipov - presun do samostatneho elementu z description
    $('form .form-control').each(function(){
       if($(this).attr('data-toggle') == 'tooltip'){
           var description = $(this).attr('title');
           $(this).parent().find('label').append('<span rel="tooltip" class="glyphicon glyphicon-question-sign tooltip-mark" data-toggle="tooltip" title="'+description+'"></span>');
           $(this).parent().find('[data-toggle="tooltip"]').tooltip();
       }
    });

    //panel sipky
    $('.panel-collapse').on('show.bs.collapse', function () {
        $(this).siblings('.panel-heading').addClass('active');
    });

    $('.panel-collapse').on('hide.bs.collapse', function () {
        $(this).siblings('.panel-heading').removeClass('active');
    });
});

