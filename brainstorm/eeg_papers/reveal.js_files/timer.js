/*
	Timers for each slide
	Define timers by slide number
*/


// Next button code
// First, make an array of whether or not the next button is enabled
var is_enabled = new Array();
/*for (var i = 0; i < Reveal.getTotalSlides(); i++) {
	is_enabled.push(false);
}*/

function next_slide() {
	if (is_enabled[Reveal.indexf]) {
		Reveal.next;
	}
}

// enable next button on page
function enable_next(slide_num) {
	is_enabled[slide_num] = true;
	console.log("enable next!");
}



// Part D = Slides 3-6

// Event listeners and specific functions

// Slide 3: Human Trafficking
var human_trafficking_timer = function() {timer(3);}
Reveal.addEventListener('human_trafficking', human_trafficking_timer, false );
// Slide 4: Sex Trafficking
var sex_trafficking_timer = function() {timer(3);}
Reveal.addEventListener('sex_trafficking', sex_trafficking_timer, false );
// Slide 5: In Maryland
var in_maryland_timer = function() {timer(3);}
Reveal.addEventListener('in_maryland', in_maryland_timer, false );
// Slide 6: Child Trafficking
var child_trafficking_timer = function() {timer(2);}
Reveal.addEventListener('child_trafficking', child_trafficking_timer, false );

// Slides 3-6 function
// generalized function that is specified in handlers above
// frag_num = number of fragments
function timer(frag_num){
	// timer var to track time for event
	// start at 1000 to offer some recognition time
	var timer = 1000;
	// set a constant to be used as duration between fragments
	var FRAG_DUR = 7000;
	for (var i = frag_num; i >= 0; i--) {
		setTimeout(Reveal.nextFragment, timer);
		timer = timer + FRAG_DUR;
	}
	console.log("Reveal Index: " + Reveal.getIndices().f);
	enable_next(Reveal.getIndices().f);
}



// Youtube Videos: Slide 7 and 16 event watchers

// Youtube API Code
// var player is the iFrame interacting object
var player;
function video_controller(playerId) {
	// debug write
	console.log("Started controller");
	// set player based on input variable of ID and set the onStateChange function
	player = new YT.Player(playerId, {
		events: {
			'onStateChange': onPlayerStateChange
		}
	});
}

// function watching for state changes in youtube video to enable next button after video finishes
function onPlayerStateChange(event) {
  	console.log("Caught state change");
    if (event.data == YT.PlayerState.ENDED) {
    	enable_next();
    }
}

// Slide 7: Connection between human trafficking and porn
var connection_controller = function() {video_controller("connection_player");}
Reveal.addEventListener('connection_video', connection_controller, false );
// Slide 16: Why I stopped watching porn
var stop_controller = function() {video_controller("stop_player");}
Reveal.addEventListener('stop_video', stop_controller, false );




// Slides 8, 9, 14
// Timers that prompt for each cue in the voiceover

// First, define general function of code used accross slides
var audio;
var cue_counter;
// audioId = id of audio object, cueTimes= array of different fragment cues
function prompted_voiceover(audioId, cueTimes) {
	// initialize cue_counter
	cue_counter = 0;
	// get audio object
	audio = document.getElementById(audioId);
	audio.load();
	// add the cue times to the audio object
	audio.timesArray = cueTimes;
	console.log("Playing: " + audioId);
	console.log("Cue Times: " + cueTimes);
	audio.play();
	// listen for if time has changed
	audio.addEventListener('timeupdate', timeCheck);
	// listen for if audio ends, then enable next button
	audio.addEventListener('ended', enable_next);
}

// timeCheck function checks if the current time passes one of the cues
function timeCheck(event) {
	if (audio.currentTime >= event.target.timesArray[cue_counter]) {
			Reveal.nextFragment();
			cue_counter++;
	}
}

// Then, use specific event listeners to make sure monitoring correct audio
// Slide 8: Magnitude
var magnitude_audio = function() {prompted_voiceover("magnitude_audio", [3.5,12.5,16,34]);}
Reveal.addEventListener('magnitude', magnitude_audio, false );
// Slide 9: Keyboard
var demand_audio = function() {prompted_voiceover("demand_audio", [3.5,29.1]);}
Reveal.addEventListener('demand', demand_audio, false );
// Slide 14: Coercion
var coercion_audio = function() {prompted_voiceover("coercion_audio", [4,8]);}
Reveal.addEventListener('coercion', coercion_audio, false );




// Slides 11,12,13: Static Centered Text
// Timers that enable the page after the time of their voiceovers

// First, define general function of code used accross slides
// audioId is the id of the audio object
function static_voiceover(audioId) {
	// get audio object
	audio = document.getElementById(audioId);
	audio.load();
	console.log("Playing: " + audioId);
	audio.play();
	// listen for if audio ends
	audio.addEventListener('ended', enable_next);
}

// Then, use specific event listeners to make sure monitoring correct audio
// Slide 11: Jessica Richardson
var jessica_audio = function() {static_voiceover("jessica_audio");}
Reveal.addEventListener('jessica', jessica_audio, false );
// Slide 12: Advertising for Trafficking
var advertising_trafficking_audio = function() {static_voiceover("advertising_trafficking_audio");}
Reveal.addEventListener('advertising_trafficking', advertising_trafficking_audio, false );
// Slide 13: Keyboard
var keyboard_audio = function() {static_voiceover("keyboard_audio");}
Reveal.addEventListener('keyboard', keyboard_audio, false );



// Slide 15: Clickable prompts
// Enable the next button after all prompts clicked,
// Only enable the next prompt after the previous one is clicked
var ethic_fn = function() {
	// grab the elements from the page to watch
	prompt1 = document.getElementById("ethics1");
	prompt2 = document.getElementById("ethics2");
	prompt3 = document.getElementById("ethics3");
	// initialize that the prompt hasn't occurred yet
	prompt1.prompt_occur = false;
	prompt2.prompt_occur = false;
	prompt3.prompt_occur = false;
	// all prompts are run
	prompt1.addEventListener("click", prompt_response);
	prompt2.addEventListener("click", prompt_response);
	prompt3.addEventListener("click", prompt_response);
}

var prompt_response = function(event) {
	if (!event.target.prompt_occur) {
		Reveal.nextFragment();
		event.target.prompt_occur = true;
	}
	event.target.removeEventListener("click", prompt_response);
}

Reveal.addEventListener('ethical', ethic_fn, false );

// Slide 10: Clickable prompts