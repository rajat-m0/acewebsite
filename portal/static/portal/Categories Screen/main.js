/* let container, ruleContainer;

window.onload = function() {
    container = document.getElementsByClassName("container")[0];
    ruleContainer = document.getElementsByClassName("rule-container")[0];
};

function showRules() {
    TweenMax.to(".rules", 0.6, {
        display: "flex",
        left: 0,
        top: 0,
        ease: Power2.easeIn,
        width: "100vw",
        height: "100vh",
        onComplete: function() {
            ruleContainer.style.visibility = "visible";
            container.style.display = "none";
        }
    });
}

function hideRules() {
    container.style.display = "inline-block";
    ruleContainer.style.visibility = "hidden";
    TweenMax.to(".rules", 0.7, {
        display: "none",
        left: "87vw",
        ease: Power2.easeOut,
        top: "9vh",
        width: "0",
        height: "0"
    });
} */


$(document).ready(function(){
	$("#ruleTrigger").click(function(){
		$(".rules").slideDown();
	})
	
	$(".back-button").click(function(){
		$(".rules").slideUp();
	})
})
