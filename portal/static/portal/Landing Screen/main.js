let t1;

window.onload = function() {
    t1 = new TimelineLite({ paused: true });

    rotateLogo();

    function rotateLogo() {
        t1.to(".back", 0.1, {
            rotation: "-=2",
            onComplete: function() {
                rotateLogo();
            }
        });
    }

    t1.play();
};
