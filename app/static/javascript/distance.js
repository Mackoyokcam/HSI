var data = {};
var origins_array = [];
var destinations_array = [];
var reference_array = [];
var count = -1;
var restore_height;
var restore_width;

function addFunction() {
    var origin = document.getElementById('origin_address');
    var destination = document.getElementById('destination_address');
    var addresses = document.getElementById('addresses');
    var originValue = origin.value;
    var destinationValue = destination.value;

    origins_array.push(originValue);
    destinations_array.push(destinationValue);

    count++;

    //restore_height = addresses.clientHeight;
    //restore_width = addresses.clientWidth;

    addresses.innerHTML = "<div>" + originValue + " to " + destinationValue +
        "  <button class='removeButton' onclick='removeButtonFunction(event)'>X</button> </div><br>"
        + addresses.innerHTML;

}

function removeButtonFunction(event) {
    var x = event.target;

   // x.parentElement.parentElement.style.height = restore_height;
    x.parentNode.remove();


}

function submitFunction() {
    data['Origins'] = origins_array;
    data['Destinations'] = destinations_array;
    data['Key'] = '';


    xhr = new XMLHttpRequest();
    var url = "/test2";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var content = JSON.parse(xhr.responseText);
            var google = content['google'];
            var googleStatus = google['status'];

            if (googleStatus == 'OK') {
                orig = google['origin_addresses'];
                dest = google['destination_addresses'];
                elements = google['rows'][0]['elements'][0];
                elementStatus = elements['status'];
                if (elementStatus == 'OK') {
                    distance = elements['distance']['text'];
                    duration = elements['duration']['text'];
                }
            }
            
            if(elementStatus == 'OK') {
                document.getElementById('results').innerHTML = "<p> Distance: " + distance +
                "<br> Duration: " + duration +
                "</p>";

            } else {
                document.getElementById('results').innerHTML = "<p> No available data for this area. </p>";
            }
        }
    };
    
    var json_string_data = JSON.stringify(data);
    alert(json_string_data);
    xhr.send(json_string_data);
    
}
