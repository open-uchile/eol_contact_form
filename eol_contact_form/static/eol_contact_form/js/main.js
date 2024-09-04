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
    async function is_logged(){
        let course_list = []
        try {
            const response = await $.ajax("/api/enrollment/v1/enrollment");
            response.forEach(element => {
                course_list.push([
                    element.course_details.course_id,
                    element.course_details.course_name
                ]);
            });
        } catch (error) {
            console.error('Error', error);
        }
        return course_list;  
    }
    async function show_course_name() {
        const list_course = [
            'issuance_of_certificates',
            'where_to_find_the_course_programs',
            'problems_in_progress',
            'content_of_a_course',
            'administrative',
            'evaluations'
        ]
        if( list_course.includes($('#form-type').val())) {
            let list_user_courses=  await is_logged();
            if(list_user_courses.length>0){
                const selectCourses= document.getElementById("select-course");
                list_user_courses.forEach(course => {
                    const option = document.createElement("option");
                    option.value = course[0];
                    option.textContent = course[1];
                    selectCourses.appendChild(option);
                });
                const option = document.createElement("option");
                option.value = "-"; 

                option.textContent = gettext("Other");
                selectCourses.appendChild(option);
                $('#select-course').show();
                $('.form-select-course-name').show();
                $("#form-select-course").prop('required',true);
                $('.form-course-name').hide();
                $("#form-course").prop('required',false);
            }else{
                $('.form-course-name').show();
                $("#form-course").prop('required',true);
                $('.form-select-course-name').hide();
                $('#select-course').hide();
                $("#form-select-course").prop('required',false);
            }
        } else {
            $('#select-course').hide();
            $('.form-select-course-name').hide();
            $("#form-select-course").prop('required',false);
            $('.form-course-name').hide();
            $('#form-course').val('');
            $("#form-course").prop('required',false);

        }
    }
    function show_identifier() {
        if($('#form-type').val() == 'login') {
            $('.form-identifier-text').show();
        } else {
            $('.form-identifier-text').hide();
            $('#form-identifier').val('');
        }
    }
    function show_eol_link() {
        if($('#form-type').val() == 'teacher_training') {
            $('#eol-link').show();
        } else {
            $('#eol-link').hide();
        }
    }
    function show_honor_link() {
        if($('#form-type').val() == 'honor_code') {
            $('#honor-link').show();
        } else {
            $('#honor-link').hide();
        }
    }
});
