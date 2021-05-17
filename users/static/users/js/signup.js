let state = [],
    toolTipText,
    fi1,
    fi2,
    fi3,
    fi4,
    fi5,
    com,
    container,
    main;

window.onload = function() {
    toolTipText = document.getElementsByClassName("tooltiptext")[0];
};

function higlight(value) {
    const icon = event.srcElement.parentElement.nextElementSibling;
    if (value != "") {
        icon.style.color = "white";
        event.srcElement.style.color = "white";
    } else {
        icon.style.color = "#9f9fa5";
        event.srcElement.style.color = "#9f9fa5";
        if (event.srcElement.type != "date") {
            removeTopPlaceholder(value);
        }
    }
}

function addTopPlaceholder(placeholder, value) {
    if (value == "") {
        const placeholderContainer = event.srcElement.nextElementSibling;
        event.srcElement.placeholder = "";
        placeholderContainer.innerText = placeholder;
        state.push({ element: event.srcElement, placeholder: placeholder });
        placeholderContainer.className = "top-placeholder";
    }
}

function removeTopPlaceholder(value) {
    if (value == "") {
        const placeholderContainer = event.srcElement.nextElementSibling;
        placeholderContainer.innerText = "";
        placeholderContainer.className = "";
        if (event.srcElement.placeholder == "") {
            event.srcElement.placeholder = getPlaceholder(event.srcElement);
        }
    }
}

function higlightSelect(value) {
    const icon = event.srcElement.parentElement.nextElementSibling;
    if (value == "0") {
        icon.style.color = "#9f9fa5";
    } else {
        icon.style.color = "white";
    }
}

function addTopPlaceholderDate(placeholder, value) {
    if (value == "" && placeholder != "") {
        const placeholderContainer = event.srcElement.nextElementSibling;
        event.srcElement.placeholder = "";
        placeholderContainer.innerText = placeholder;
        placeholderContainer.className = "top-placeholder";
    }
}

function removeTopPlaceholderDate(value) {
    if (value == "") {
        const placeholderContainer = event.srcElement.nextElementSibling;
        placeholderContainer.innerText = "";
        placeholderContainer.className = "";
        event.srcElement.placeholder = "DOB";
    }
}

function addPlaceHolderSelect() {
    if (
        event.srcElement.options[event.srcElement.options.length - 1].value !=
        "empty"
    ) {
        const option = document.createElement("option");
        option.text = "";
        option.value = "empty";
        option.style.display = "none";
        event.srcElement.add(option);
        if (event.type == "mousedown") {
            event.srcElement.value = "empty";
        }
        const placeholderContainer = event.srcElement.nextElementSibling;
        const placeholder = event.srcElement.options[0].text;
        placeholderContainer.innerText = placeholder;
        state.push({ element: event.srcElement, placeholder: placeholder });
        placeholderContainer.className = "top-placeholder";
    }
}

function getPlaceholder(element) {
    for (let s of state) {
        if (s.element == element) {
            let placeholder = s.placeholder;
            state.splice(state.indexOf(s), 1);
            return placeholder;
        }
    }
}

function selectChanged() {
    higlight("this");
    if (event.srcElement.selectedIndex != 0) {
        event.srcElement.style.color = "white";
        addPlaceHolderSelect();
    } else {
        event.srcElement.style.color = "#9f9fa5";
        removePlaceHolderSelect();
    }
}

function removePlaceHolderSelect(outside) {
    let length = event.srcElement.options.length - 1;
    if (outside == "outside") {
        if (
            event.srcElement.options[length].value == "empty" &&
            event.srcElement.selectedIndex == length
        ) {
            event.srcElement.selectedIndex = 0;
            removePlaceHolderSelect();
        }
    } else if (
        event.srcElement.selectedIndex == 0 &&
        event.srcElement.options[length].value == "empty"
    ) {
        event.srcElement.remove(length);
        const placeholderContainer = event.srcElement.nextElementSibling;
        placeholderContainer.innerText = "";
        placeholderContainer.className = "";
        event.srcElement.placeholder = getPlaceholder(event.srcElement);
    }
}

function showToolTipText() {
    toolTipText.style.visibility = "visible";
    toolTipText.style.marginLeft = "1.3rem";
}

function hideToolTipText() {
    toolTipText.style.visibility = "hidden";
    toolTipText.style.marginLeft = "0";
}

function showToolTipTextemail() {
    tooltiptext1.style.visibility = "visible";
    tooltiptext1.style.marginLeft = "1.3rem";
}

function hideToolTipTextemail() {
    tooltiptext.style.visibility = "hidden";
    tooltiptext.style.marginLeft = "0";
}
