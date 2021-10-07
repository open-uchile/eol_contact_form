var correctCaptcha = function(response) {
    if(response.length != 0) {
        $('.form-submit').prop('disabled', false);;
    } else {
        $('.form-submit').prop('disabled', true);;
    }
};
$(function() {
    show_course_name();

    $('#form-type').on('change', function() {
        show_course_name();
    });

    function show_course_name() {
        if($('#form-type').val() == 'course') {
            $('.form-course-name').show();
            $("#form-course").prop('required',true);
        } else {
            $('.form-course-name').hide();
            $('#form-course').val('');
            $("#form-course").prop('required',false);
        }
    }
});