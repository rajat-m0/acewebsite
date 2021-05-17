let previousState = [],
  buttons,
  tasks,
  btnSize,
  uploadDivs = [],
  taskDivSize = "25vw",
  attempted;

window.onload = function() {
  const bgImg = document.getElementById("bgImg");
  attempted = {
    taskeasy: true,
    taskmedium: false,
    taskhard: true
  };
  bgImg.src = "background image path";
  if (bgImg.src.includes("AudioVisual")) {
    bgImg.style.transform = "rotate(-9deg)";
  } else if (bgImg.src.includes("Misc")) {
    bgImg.style.transform = "rotate(-15deg)";
  }
  bgImg.parentElement.style.backgroundColor = "background color";
  setAnimatedButtonSize();
  window.onresize = setAnimatedButtonSize;
  buttons = [...document.getElementsByClassName("checked-btn")];
  tasks = [
    document.getElementById("taskeasy"),
    document.getElementById("taskmedium"),
    document.getElementById("taskhard")
  ];
  buttons.forEach(button => {
    for (let task of tasks) {
      if (task.contains(button)) {
        if (attempted[task.id]) {
          button.firstElementChild.style.display = "none";
          button.firstElementChild.style.visibility = "hidden";
          button.children[1].innerText = "Attempted";
          move(button.id);
        } else {
          button.addEventListener("mouseenter", animateChecked);
          button.addEventListener("mouseleave", reanimateChecked);
        }
      }
    }
  });
};

function setAnimatedButtonSize() {
  if (window.innerWidth <= 2560 && window.innerWidth > 1440) {
    btnSize = "5rem";
  } else if (window.innerWidth <= 1440 && window.innerWidth > 768) {
    btnSize = "2.5rem";
    taskDivSize = "27vw";
  } else if (window.innerWidth <= 768 && window.innerWidth > 425) {
    btnSize = "2.1rem";
    taskDivSize = "40vw";
  } else if (window.innerWidth <= 425 && window.innerWidth > 375) {
    btnSize = "1.5rem";
  }
}

function getParentNode(element) {
  for (let task of tasks) {
    if (task.contains(element)) {
      return task;
    }
  }
}

function isReadyState(srcElement) {
  for (let prevState of previousState) {
    if (prevState.state && prevState.state.includes(srcElement.id)) {
      return true;
    }
  }
  return false;
}

function uploadFiles() {
  const parentNode = getParentNode(event.srcElement);
  previousState.push({
    id: parentNode.id,
    html: parentNode.innerHTML
  });
  if (!isReadyState(parentNode)) {
    parentNode.innerHTML = `<div class="title title-container-upload">
                                <div class="angle-btn" onclick="goBack()">
                                    <i class="fas fa-angle-left"></i> 
                                </div>
                                <div>Upload Files</div>
                            </div>
                            <hr />
                            <div class="body upload-body-container">
                                You can submit one file in on submission,
                                so if you have multiple files, submit a 
                                zip file.
                            </div>
                            <div class="body upload-container" id="${parentNode.id}upload" onclick="openFileUploadDialog()">
                                <input type="file" name="${parentNode.id}uploadfile" id="${parentNode.id}uploadfile" style="display: none; width: 0; height: 0;" onchange="showFile(this)">
                                <div class="largebody"}>
                                    Drag File here or <span style="color: #ff669f">Browse</span>
                                </div>
                            </div>
                            <div class="upload-submission">
                                <button class="upload-btn" onclick="sendFile()" disabled>
                                    <span>
                                        Submit
                                    </span>
                                </button>
                            </div>`;
    let uploadDiv = document.getElementById(`${parentNode.id}upload`);
    uploadDiv.addEventListener("dragenter", dragHandler, false);
    uploadDiv.addEventListener("dragover", dragHandler, false);
    uploadDiv.addEventListener("dragleave", dragLeaveHandler, false);
    uploadDiv.addEventListener("drop", fileDropHandler, false);
    uploadDiv.addEventListener("drop", dragLeaveHandler, false);
    uploadDivs.push(uploadDiv);
  } else {
    for (let prevState of previousState) {
      if (prevState.state && prevState.state.includes(parentNode.id)) {
        parentNode.innerHTML = prevState.state;
      }
    }
  }
}

function sendFile() {
  let input = event.srcElement.parentElement.previousElementSibling;
  input = [...input.children][0];
  const file = input.files[0];
  const fileReader = new FileReader();
  fileReader.readAsDataURL(file);
  fileReader.onload = function() {
    fetch(url, {
      method: "POST",
      body: fileReader.result
    });
  };
}

function dragHandler() {
  uploadDivs.forEach(uploadDiv => {
    if (uploadDiv == event.srcElement) {
      uploadDiv.style.backgroundColor = "grey";
    }
  });
}

function dragLeaveHandler() {
  event.srcElement.style.backgroundColor = "";
}

function fileDropHandler() {
  const dt = event.dataTransfer;
  const files = dt.files;
  event.srcElement.children[0].files = files;
  showFile(event.srcElement.children[0]);
}

function showFile(srcElement) {
  const files = srcElement.files;
  const file = files[0];
  srcElement.parentElement.nextElementSibling.children[0].style.backgroundColor =
    "#ff669f";
  srcElement.parentElement.nextElementSibling.children[0].disabled = false;
  let uploadDivContent = srcElement.nextElementSibling;
  uploadDivContent.innerText = "";
  uploadDivContent.className = " upload-container-ready";
  uploadDivContent.innerHTML = `
        <div class="udiv-ficon"><i class="fas fa-file"></i></div>
        <div class="udiv-txt">${file.name}</div>
        <div class="udiv-crossicon"><i class="fas fa-times-circle" onclick="removeFile()"></i></div>
    `;
  srcElement.disabled = true;
  const readyState = {
    state: getParentNode(srcElement).innerHTML
  };
  previousState.push(readyState);
}

function removeFile() {
  const parentElement = getParentNode(event.srcElement);
  for (let i = 0; i < previousState.length; i++) {
    if (
      previousState[i].state &&
      previousState[i].state.includes(parentElement.id)
    ) {
      previousState.splice(i, 1);
    }
  }
  const largeBodyDiv = event.srcElement.parentElement.parentElement;
  largeBodyDiv.parentElement.nextElementSibling.children[0].style.backgroundColor =
    "rgba(255, 255, 255, 0.2)";
  largeBodyDiv.parentElement.nextElementSibling.children[0].disabled = true;
  largeBodyDiv.innerHTML = `Drag File here or <span style="color: #ff669f">Browse</span>`;
  largeBodyDiv.className = "largebody";
  largeBodyDiv.previousElementSibling.value = "";
  largeBodyDiv.previousElementSibling.disabled = false;
}

window.addEventListener(
  "dragover",
  function(e) {
    e = e || event;
    e.preventDefault();
  },
  false
);
window.addEventListener(
  "drop",
  function(e) {
    e = e || event;
    e.preventDefault();
  },
  false
);

function reanimateChecked() {
  if (event.srcElement.style.width == "100%") {
    remove(event.srcElement);
    event.srcElement.children[1].innerText = "";
  }
}

function animateChecked() {
  if (event.srcElement.tagName == "DIV") {
    event.srcElement.firstElementChild.style.display = "none";
    event.srcElement.firstElementChild.style.visibility = "hidden";
    event.srcElement.children[1].innerText = "Attempted";
    move(event.srcElement.id);
  }
}

function move(obj) {
  TweenMax.to(`#${obj}`, 0.4, {
    ease: Power0.easeIn,
    width: "100%"
  });
}

function remove(obj) {
  let p = document.getElementById(obj.id);
  p.children[0].style.visibility = "visible";
  TweenMax.to(`#${obj.id}`, 0.1, {
    ease: Power0.easeOut,
    width: btnSize,
    onComplete: function() {
      obj.firstElementChild.style.display = "block";
    }
  });
}

function openFileUploadDialog() {
  const parentNode = getParentNode(event.srcElement);
  if (parentNode) {
    const uploadButton = document.getElementById(
      `${parentNode.id}uploadfile`
    );
    uploadButton.dispatchEvent(new MouseEvent("click"));
  }
}

function goBack() {
  const parentNode = getParentNode(event.srcElement);
  for (let i = 0; i < uploadDivs.length; i++) {
    if (uploadDivs[i].id.includes(parentNode.id)) {
      uploadDivs.splice(i, 1);
    }
  }
  parentNode.innerHTML = removeState(parentNode);
  buttons = [...document.getElementsByClassName("checked-btn")];
  buttons.forEach(button => {
    for (let task of tasks) {
      if (task.contains(button)) {
        if (attempted[task.id]) {
          button.firstElementChild.style.display = "none";
          button.firstElementChild.style.visibility = "hidden";
          button.children[1].innerText = "Attempted";
          move(button.id);
        } else {
          button.addEventListener("mouseenter", animateChecked);
          button.addEventListener("mouseleave", reanimateChecked);
        }
      }
    }
  });
}

function removeState(node) {
  let html;
  for (let state of previousState) {
    if (state.id == node.id) {
      html = state.html;
      previousState.splice(previousState.indexOf(state), 1);
      return html;
    }
  }
}

function showTaskExtended(id) {
  const taskDivs = [...document.getElementsByClassName(id)];
  const taskDiv = findTaskCategory(taskDivs);
  taskDivs.splice(taskDivs.indexOf(taskDiv), 1);
  const taskContainer = document.getElementById("taskcontainer");
  if (window.innerWidth <= 768) {
    [...document.getElementsByClassName("title-container")].forEach(tc => {
      tc.className += " title-container-tabandlower";
    });
    taskContainer.className += "-tabandlower";
    taskDiv.className += " task-tabandlower";
    document.getElementsByClassName("background")[0].className +=
      " bg-tabandlower";
  } else {
    taskContainer.style.justifyContent = "flex-end";
  }
  taskDivs.forEach(div => {
    div.style.display = "none";
  });
  const cardContainer = taskDiv.children[0];
  previousState.push({
    id: cardContainer.id,
    html: cardContainer.innerHTML
  });
  let type = "";
  if (taskDiv.className.includes("middle")) {
    taskDiv.style.backdropFilter = "none";
    type = "med";
  }
  cardContainer.children[4].style.height = "0";
  cardContainer.children[4].style.display = "none";
  cardContainer.children[2].innerText = "Generic Question Title";
  cardContainer.children[0].children[1].className += " spl-ch";
  cardContainer.children[3].className += " spl-lg-bd-cont";
  cardContainer.children[2].className += " spl-lg-tt-cont";
  cardContainer.children[3].innerText =
    "Generic Question Description, which might give the user knowledge of what kind of problem it is. Detailed Description, input, output, complexity(maybe)";
  cardContainer.children[0].style.justifyContent = "flex-start";
  const prevHTML = cardContainer.children[0].innerHTML;
  const startHTML = `<div class="angle-btn" onclick="showTaskNormal('${id}')">
                            <i class="fas fa-angle-left"></i>
                        </div>`;
  const endHTML = `<div class="spl-sub-sub${type}">999 Total Submission</div><button class="btn spl${type}" onclick="LargeDivuploadFiles('${id}', '${cardContainer.id}')">
                        <span>
                            Submit
                            <i class="fas fa-arrow-right"></i>
                        </span>
                    </button>`;
  cardContainer.children[0].innerHTML = startHTML + prevHTML + endHTML;
  buttons = [...document.getElementsByClassName("checked-btn")];
  buttons.forEach(button => {
    for (let task of tasks) {
      if (task.contains(button)) {
        if (attempted[task.id]) {
          button.firstElementChild.style.display = "none";
          button.firstElementChild.style.visibility = "hidden";
          button.children[1].innerText = "Attempted";
          move(button.id);
        } else {
          button.addEventListener("mouseenter", animateChecked);
          button.addEventListener("mouseleave", reanimateChecked);
        }
      }
    }
  });
  TweenMax.to(taskDiv, 0.5, {
    width: "100%",
    ease: Power0.easeIn
  });
}

function findTaskCategory(nodes) {
  for (let node of nodes) {
    if (node.contains(event.srcElement)) {
      return node;
    }
  }
}

function showTaskNormal(id) {
  const parentNode = getParentNode(event.srcElement);
  const container = parentNode.parentElement;
  if (container.className.includes("middle")) {
    container.style.backdropFilter = "blur(10px)";
  }
  parentNode.innerHTML = removeState(parentNode);
  buttons = [...document.getElementsByClassName("checked-btn")];
  buttons.forEach(button => {
    for (let task of tasks) {
      if (task.contains(button)) {
        if (attempted[task.id]) {
          button.firstElementChild.style.display = "none";
          button.firstElementChild.style.visibility = "hidden";
          button.children[1].innerText = "Attempted";
          move(button.id);
        } else {
          button.addEventListener("mouseenter", animateChecked);
          button.addEventListener("mouseleave", reanimateChecked);
        }
      }
    }
  });
  const taskDivs = [...document.getElementsByClassName(id)];
  taskDivs.splice(taskDivs.indexOf(container), 1);
  const taskContainer = document.getElementById("taskcontainer");
  if (window.innerWidth <= 768) {
    [...document.getElementsByClassName("title-container")].forEach(tc => {
      tc.className += "title-container";
    });
    taskContainer.className = "task-container";
    container.className = "task";
    document.getElementsByClassName("background")[0].className =
      "background img-container";
  } else {
    taskContainer.style.justifyContent = "flex-end";
  }
  TweenMax.to(container, 0.5, {
    width: taskDivSize,
    ease: Power0.easeOut
  });
  taskDivs.forEach(div => {
    div.style.display = "flex";
  });
  if (id == "misc") {
    taskContainer.style.justifyContent = "center";
  } else {
    taskContainer.style.justifyContent = "space-between";
  }
}

function LargeDivuploadFiles(id, child) {
  showTaskNormal(id);
  const element = document.getElementById(child).children[4].children[1]
    .children[0];
  element.dispatchEvent(new MouseEvent("click"));
}