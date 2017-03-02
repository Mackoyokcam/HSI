var content = JSON.parse(json_content);
var addStatus = content['status'];


function loadJson() {
    var status = document.getElementById('addStatus');
    if (addStatus == 'True')
        status.innerHTML = "Thank you for registering!";
    else
        status.innerHTML = "Error in adding property. Please make sure data is correct."

}

window.onload = loadJson;