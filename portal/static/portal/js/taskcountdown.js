

window.onload = function() {
    let clock,
    angle = 0,
    timer,
    startDate = (new Date( document.getElementById("script-data").getAttribute("data-start_date") )).getTime()

    clock = document.getElementsByClassName("clock")[0];
    // Parse date object from backend, set it as onload timer value
    clock.style.transform = `rotate(${angle}deg)`;
    timer = [...document.getElementsByClassName("timer")];

    window.setInterval(() => {
        clock.style.transform = `rotate(${angle}deg)`;
        angle += 6;
        if (angle >= 360) angle = 0;
    }, 1000);

    // window.setInterval(() => {
    //     let min = parseInt(timer[2].innerText);
    //     min -= 1;
    //     if (min == 0) {
    //         timer[2].innerText = 60;
    //         let hours = parseInt(timer[1].innerText);
    //         hours -= 1;
    //         if (hours == 0) {
    //             timer[1].innerText = 24;
    //             let days = parseInt(timer[0].innerText);
    //             days -= 1;
    //             if (days.toString().length < 2) {
    //                 timer[0].innerText = `0${days}`;
    //             } else {
    //                 timer[0].innerText = `${days}`;
    //             }
    //         } else {
    //             if (hours.toString().length < 2) {
    //                 timer[1].innerText = `0${hours}`;
    //             } else {
    //                 timer[1].innerText = `${hours}`;
    //             }
    //         }
    //     } else {
    //         if (min.toString().length < 2) {
    //             timer[2].innerText = `0${min}`;
    //         } else {
    //             timer[2].innerText = `${min}`;
    //         }
    //     }
    // }, 60000);

    function setClock() {
        let diff = Math.floor((startDate - Date.now())/1000)

        const days = Math.floor(diff/ 3600 / 24)
        diff -= days * 60 * 60 * 24

        const hours = Math.floor(diff / 3600)
        diff -= hours * 3600

        const mins = Math.floor(diff/60)
        diff -= mins * 60

        timer[2].innerText = (mins.toString().length < 2 ? "0" : "") + mins
        timer[1].innerText = (hours.toString().length < 2 ? "0" : "") + hours
        timer[0].innerText = (days.toString().length < 2 ? "0" : "") + days
        
        if(!angle) {
            angle = (60 - diff) * 6
            clock.style.transform = `rotate(${angle}deg)`;
        }
    }

    setClock();
    window.setInterval(setClock, 60000);
};

const mainLogoBack = document.getElementById("MainLogoBack");
const t1 = new TimelineLite({ paused: true });

t1.to(".main-logo", 1, {
    height: "28rem",
    ease: Power2.easeOut,
    onComplete: function() {
        rotateLogo();
    }
});

function rotateLogo() {
    t1.to(".main-logo", 0.1, {
        rotation: "-=2",
        onComplete: function() {
            rotateLogo();
        }
    });
}

t1.play();
