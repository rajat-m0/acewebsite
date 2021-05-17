const mainLogoBack = document.getElementById("MainLogoBack");
const btnFacebook = document.getElementById("btn-facebook");
const btnGoogle = document.getElementById("btn-google");
const t1 = new TimelineLite({ paused: true });

function animateFacebookButton() {
    t1.to(btnFacebook, 0.3, {
        transform: "translateY(0.1rem)",
        onComplete: function() {
            t1.to(btnFacebook, 0.3, {
                transform: "translateY(-0.2rem)",
                onComplete: function() {
                    btnFacebook.style.transform = "";
                }
            });
        }
    });
}

function animateGoogleButton() {
    t1.to(btnGoogle, 0.3, {
        transform: "translateY(0.1rem)",
        onComplete: function() {
            t1.to(btnGoogle, 0.3, {
                transform: "translateY(-0.2rem)",
                onComplete: function() {
                    btnGoogle.style.transform = "";
                }
            });
        }
    });
}

t1.to(".main-logo", 1, {
    height: "28rem",
    ease: Power2.easeOut,
    onComplete: function() {
        rotateLogo();
    }
});

function rotateLogo() {
    // return ;
    t1.to(".main-logo", 0.1, {
        rotation: "-=2",
        onComplete: function() {
            rotateLogo();
        }
    });
}

t1.play();
