/*============== Ajax helper csrf_token generate ajax methods =============*/

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

/*=================youtube video=================*/
//$(document).ready(function () {
//  
//  $('#video').YTPlayer({
//    fitToBackground: true,
//    videoId: 'yRll4kJp6Ow',
//    mute:true,
//    playerVars: {
//      modestbranding: 0,
//      autoplay: 1,
//      controls: 0,
//      showinfo: 0,
//      branding: 0,
//      rel: 0,
//      autohide: 0
//    }
//});

//var player = $('#video').data('ytPlayer').player;


$(document).ready(function () {


	/*============== Ajax Setup csrf_token generate ajax headers =============*/
	$.ajaxSetup({
		beforeSend: function (xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});
	/*==============Audio Player==============*/


	function initAudio() {
		audio.play();
		$('.pause-button').show();
		$('.play-button').hide();
	}


	function change_track() {
		if (count == 7) {
			count = 0;
		} else {
			$("#song").attr('src', '../../static/olimpiad/mp3/' + songs[count]);
			audio.play();
			count++;
			console.log(count);
		}
	}

	if ($('section').is('.music-start')) {
		var audio = document.querySelector('#song');
		var songs = ['1.mp3', '2.mp3', '3.mp3', '4.mp3', '5.mp3', '6.mp3', '7.mp3'];
		var progressWidth;
		var count = 1;

		initAudio();

		//playbutton
		$('.play-button').click(function () {
			audio.play();
			$(this).hide();
			$('.pause-button').show();
		});

		audio.onended = function () {
			change_track();
		};

		//pause button
		$('.pause-button').click(function () {
			audio.pause();
			$(this).hide();
			$('.play-button').show();
		});

		//volume control
		$('.volume').mousedown(function (e) {
			progressWidth = Math.floor(e.pageX - $(this).offset().left);
			$('.volume-progress-bar').css('width', progressWidth + 'px');
			audio.volume = progressWidth / 100;
			if (audio.muted == true && audio.volume > 0) {
				audio.muted = false;
				$('.mute-drop').hide();
			}
		});

		//  mute button
		$('.mute').click(function (e) {
			e.preventDefault();
			if (audio.muted == false) {
				audio.muted = true;
				$('.mute-drop').show();
				progressWidth = 0;
				$('.volume-progress-bar').css('width', progressWidth + 'px');
			} else {
				audio.muted = false;
				$('.mute-drop').hide();
				progressWidth = 100 * audio.volume;
				$('.volume-progress-bar').css('width', progressWidth + 'px');
			}
		});
	}

	/*===================right section - result tables===================*/
	$('.week').click(function () {
		$('.month-table').hide();
		$('.result-table').hide();
		$('.week-table').show();
		$(this).addClass('hist-active');
		$('.month').removeClass('hist-active');
		$('.result').removeClass('hist-active');
	});

	/*=================== facebook open share model pop up window ===================*/

        $('.fb').click(function(e) {
            e.preventDefault();
            window.open($(this).attr('href'), 'fbShareWindow', 'height=450, width=550, top=' + ($(window).height() / 2 - 275) + ', left=' + ($(window).width() / 2 - 225) + ', toolbar=0, location=0, menubar=0, directories=0, scrollbars=0');
            return false;
            });

        $('.share').click(function(e) {
            e.preventDefault();
			if(!$('section').is('.music-start')){
				   window.onbeforeunload = null;
				   window.location = '/share/';
			   }
			   else if (confirm('Oyundan çıxmağınıza əminsiniz?')) {
					window.onbeforeunload = null;
					window.location = '/share/';
				}
            //window.open('http://mok25.az/share/', 'fbShareWindow', 'height=450, width=550, top=' + ($(window).height() / 2 - 275) + ', left=' + ($(window).width() / 2 - 225) + ', toolbar=0, location=0, menubar=0, directories=0, scrollbars=0');
            // return false;
            });


	$('.month').click(function () {
		$('.week-table').hide();
		$('.result-table').hide();
		$('.month-table').show();
		$(this).addClass('hist-active');
		$('.week').removeClass('hist-active');
		$('.result').removeClass('hist-active');
	});

	$('.result').click(function () {
		$('.month-table').hide();
		$('.week-table').hide();
		$('.result-table').show();
		$(this).addClass('hist-active');
		$('.week').removeClass('hist-active');
		$('.month').removeClass('hist-active');
	});

	/*=======================mobile slide menu=======================*/

	$('#game-hamburger-btn').click(function () {
		$('.mobile-slide').animate({
			right: "0"
		}, 500);
	});

	$('#game-hamburger-close').click(function () {
		$('.mobile-slide').animate({
			right: "-100%"
		}, 500);
	});

	/*==========================joker color==========================*/

	$('.help-1').click(function () {
		if ($(this).hasClass('joker-color')) {
			return false;
		} else {
			$(this).addClass('joker-color');
			var form = new FormData();
			form.append('q_id', $('.tab-pane.active:last').attr('data-id'));
			$.ajax({
				url: "/question/half/",
				type: "POST",
				data: form,
				processData: false,
				contentType: false,
				success: function (data) {
					console.log(data.object);
					$('.tab-pane.active:last > .answers .answer').map(function (t, e) {
						if ($(e).attr('data-answer-id') !== String(data.object[0]) && $(e).attr('data-answer-id') !== String(data.object[1])) {
							$(e).hide();
						}
					});
				}
			});
		}
	});

	$('.help-2').click(function () {

		if ($(this).hasClass('joker-color')) {
			return false;
		} else {
			$(this).addClass('joker-color');
			var form = new FormData();
			form.append('q_id', $('.tab-pane.active:last').attr('data-id'));
			form.append('count', $('.tab-pane.active:last').attr('data-count'));
			form.append('q_list', $('#game-id-list').val());
			$.ajax({
				url: "/question/change/",
				type: "POST",
				data: form,
				processData: false,
				contentType: false,
				success: function (data) {
					if (data.error) {
						console.log(data.error);
					} else {
						$('.tab-pane.active:last').html(data);
					}

				}
			});
		}
	});

	$('.help-3').click(function () {
		if ($(this).hasClass('joker-color')) {
			return false;
		} else {
			$(this).addClass('joker-color');
			var form = new FormData();
			form.append('q_id', $('.tab-pane.active:last').attr('data-id'));
			$.ajax({
				url: "/question/two/",
				type: "POST",
				data: form,
				processData: false,
				contentType: false,
				success: function (data) {
					if (data.error) {
						alert(data.error);
					} else {
						window.two_answer = true;
					}

				}
			});
		}
	});

	/*===========history section change color date===========*/
	$('.history-date').click(function () {
		$('.history-date').addClass('hist-color');
		$(this).removeClass('hist-color');
		$(this).addClass('hist-active');
	});
	// history click
	$('.history').click(function () {
		if ($('section').is('.in-game')) {
			if (confirm('Oyundan çıxmağınıza əminsiniz?')) {
				window.onbeforeunload = null;
				window.location = '/history/';
			} else {
				return false;
			}

		} else {
			window.onbeforeunload = null;
			window.location = '/history/';
		}
	});
	//  change color days btn
	$('.days-btn').click(function () {
		$('.days-btn').addClass('hist-color');
		$(this).removeClass('hist-color');
		$(this).addClass('days-active');
	});

	// exit button
	$('.exit').click(function () {
		if(!$('section').is('.music-start')){
           window.onbeforeunload = null;
           window.location = '/game/exit/';
       }
       else if (confirm('Oyundan çıxmağınıza əminsiniz?')) {
			window.onbeforeunload = null;
			window.location = '/game/exit/';
		}
		else {
			return false;
		}
	});
	// Exit modal button
	$('.exit-modal').click(function (e) {
		e.preventDefault();
		$('.overlay').remove();
	});

	// result exit
	$('.res-exit').click(function () {
		if (confirm('Oyundan çıxmağınıza əminsiniz?')) {
			window.onbeforeunload = null;
			window.location = '/';
		} else {
			return false;
		}
	});

	// game exit
	if ($('section').is('#game')) {
		console.log("Read code");
		window.onbeforeunload = function (event) {
			var message = "Important: Please click on 'Save' button to leave this page.";
			if (typeof event == 'undefined') {
				event = window.event;
			}
			if (event) {
				event.returnValue = message;
			}
			return message;

		};
	}

	// go back
	if ($('section').is('.go-back')) {
		window.onhashchange = function () {
			window.location = '/';
		};
	}

	// play button click
	$('.play-btn').click(function () {
		window.onbeforeunload = null;
	});

	//safety exit button
	$('.safe-exit').click(function () {
		window.onbeforeunload = null;
	});
});
/*=========== Game section time ===========*/
var minutes = 0;
var seconds = 0;
var end_counter = 3;
// helper digit function
function digit(num) {
	if (String(num).length === 1) {
		return "0" + String(num);
	} else {
		return String(num);
	}
}
// time function auto start
$(document).ready(function () {
	var y = setInterval(function () {
		// Get todays date and time
		var now = new Date().getTime();

		// Find the distance between now an the count down date
		var counter = $(".start_count");

		end_counter -= 1;
		if (end_counter == 0) {
			$(".must_be_hide").remove();
			var x = setInterval(function () {
				// Get todays date and time
				var now = new Date().getTime();

				// Find the distance between now an the count down date


				seconds += 1;
				if (seconds === 60) {
					seconds -= 60;
					minutes += 1;
				}

				// Display the result in the element with id="demo"
				if (!document.getElementById("time")) {
					return false;
				} else {
					document.getElementById("time").innerHTML = digit(minutes) + ":" + digit(seconds);
				}


			}, 1000);
		}

		// Display the result in the element with id="demo"

		if (!counter) {
			return false;
		} else {
			counter.map(function (index, el) {
				el.innerHTML = Number(end_counter);
			});
		}


	}, 1000);
});


// game
var falseAnswer = false;
// Next element function
function next() {
	setTimeout(function () {
		var query = $('.nav-tabs li > .active');
		var star = $('.stars > i.star-yellow:last');
		// console.log(query);
		star.next().addClass('star-yellow');
		query.parent().next('li').find('a').trigger('click');
		// console.log(query.next('li').find('a'));
		query.removeClass('active');

		// console.log(query);
		query.parent().next('li').find('a').addClass('active');
		// console.log(query.next('li').find('a'));
	}, 100);
}
// check answer game sections
function check_answer(e) {
	var form = new FormData();
	form.append('question_id', $(e).attr('data-question-id'));
	form.append('answer_id', $(e).attr('data-answer-id'));
	form.append('count', $('.tab-content > .active').attr('data-count'));
	$.ajax({
		url: "/online/test/",
		type: "POST",
		data: form,
		processData: false,
		contentType: false,
		success: function (data) {
			if (data === "False") {
				$(e).addClass('false-answer');
				if (window.two_answer) {
					window.two_answer = false;
				} else {
					window.onbeforeunload = null;
					window.location.href = "/results/";
				}
			} else if (data === "True") {
				$(e).addClass('right-answer');
				next();
			} else if (data.token) {
				$(e).addClass('false-answer');
				window.onbeforeunload = null;
				window.location.href = "/";
			} else {
				$(e).addClass('right-answer');
				window.onbeforeunload = null;
				window.location.href = "/results/";
			}
		}
	});

}
