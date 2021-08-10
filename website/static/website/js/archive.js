const data = fetch('https://raw.githubusercontent.com/ACE-VSIT/acewebsite/master/website/static/website/json/archive.json');
    data.then(
      res => res.json()
    ).then(
      data => {console.log(data)
      data.forEach(element => {
        const archive = document.querySelector('#archive');
        const archiveData = 
        `<div class="items-grid">
          <div class="flex-div">
            <div class="frame-inside">
              <img class="frame-child-image"
                  src="${ element.image }"
                  alt="${ element.eventname }">
            </div>
            </div class="frame-text-area">
            <div class="frame-child-text-area">${ element.eventname }</div>
            <div class="frame-child-date-area">${ element.eventdate }</div>
          </div>
        </div>`
      archive.innerHTML += archiveData;
      });
      })