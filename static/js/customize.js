        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        csrftoken = getCookie('csrftoken');

        function csrfSafeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $(document).ready(function () {
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
        });

        $(".two-answer").click(function () {

           $(this).remove();
           form.append('q_id', $('.tab-pane.active:last').attr('data-id'));
           $.ajax({
                  url: window.two_answer_url,
                  type: "POST",
                  data: form,
                  processData: false,
                  contentType: false,
                  success: function(data) {
                        if(data.error) {
                            alert(data.error);
                        }
                        else {
                            window.two_answer = true;
                        }

                  }
            });
        });

        // Change the questions Joker
        $('.change_question').click(function () {
            var form = new FormData();
            $(this).remove();
            form.append('q_id', $('.tab-pane.active:last').attr('data-id'));
            form.append('count', $('.tab-pane.active:last').attr('data-count'));
            $.ajax({
                  url: window.change_question,
                  type: "POST",
                  data: form,
                  processData: false,
                  contentType: false,
                  success: function(data) {
                        if(data.error) {
                            alert(data.error);
                        }
                        else {
                            $('.tab-pane.active:last').html(data);
                        }

                  }
            });
        });
        $('.half-question').click(function () {
            var form = new FormData();
            $(this).remove();
            form.append('q_id', $('.tab-pane.active:last').attr('data-id'));
            $.ajax({
                  url: window.half_question,
                  type: "POST",
                  data: form,
                  processData: false,
                  contentType: false,
                  success: function(data) {
                        console.log(data.object);
                        $('.tab-pane.active:last > .answer-list li').map(function (t, e) {
                           if ($(e).attr('data-answer-id') !== String(data.object[0]) && $(e).attr('data-answer-id') !== String(data.object[1])) {
                               $(e).hide();
                           }
                        });
                  }
            });
        })

    });
        function  check_answer(e) {
            var form = new FormData();
            form.append('question_id', $(e).attr('data-question-id'));
            form.append('answer_id', $(e).attr('data-answer-id'));
            $.ajax({
                  url: window.current_url,
                  type: "POST",
                  data: form,
                  processData: false,
                  contentType: false,
                  success: function(data) {
                        if (data === "False") {
                            $(e).addClass('false-answer');
                            $('.helper-text').text("Cavab yanlışdır");
                            if (window.two_answer) {
                                window.two_answer = false;
                            }
                            else {
                                window.can_pass = true;
                                window.location.href = window.done_url;
                            }
                        }
                        else {
                            $(e).addClass('right-answer');
                            $('.helper-text').text("Cavab doğrudur");
                            setTimeout(function(){
                                window.count_times.push(1);
                                if(window.count_times.length === 10) {
                                    window.can_pass = true;
                                    window.location = window.done_url;
                                }
                                else {
                                    $('.nav-tabs li > .active').parent().next('li').find('a').trigger('click');
                                    $('.helper-text').text("");

                                }
                            }, 100);


                        }
                  }
            });

        }