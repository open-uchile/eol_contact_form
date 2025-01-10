var correctCaptcha = function(response) {
    if(response.length != 0) {
        $('.form-submit').prop('disabled', false);
    } else {
        $('.form-submit').prop('disabled', true);
    }
};
$(function() {
    const referrer = document.referrer;
    $('#form-referrer').val(referrer);
    show_course_name();
    show_identifier();
    show_eol_link();
    show_honor_link();

    $('#form-type').on('change', function() {
        show_course_name();
        show_identifier();
        show_eol_link();
        show_honor_link();
    });
    
    function show_course_name() {
        if($('#form-type :selected').parent().attr('label') == gettext("Specific course questions")) {
            $('.form-course-name').show();
            $("#form-course").prop('required',true);
        }else{
            $('.form-course-name').hide();
            $('#form-course').val('');
            $("#form-course").prop('required',false);
        }
    }
    function show_identifier() {
        if($('#form-type').val() == gettext("Login problems")) {
            $('.form-identifier-text').show();
        } else {
            $('.form-identifier-text').hide();
            $('#form-identifier').val('');
        }
    }
    function show_eol_link() {
        if($('#form-type').val() == gettext("Teacher training")) {
            $('#eol-link').show();
        } else {
            $('#eol-link').hide();
        }
    }
    function show_honor_link() {
        if($('#form-type').val() == gettext("Honor code")) {
            $('#honor-link').show();
        } else {
            $('#honor-link').hide();
        }
    }
});
