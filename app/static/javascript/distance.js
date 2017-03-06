var data = {};
var origins_array = [];
var destinations_array = [];
var temp = {}
var count = 0;
var orig_text, dest_text;


function addFunction() {

    if ((orig_text.value) == "" || (dest_text.value == "")) {
        alert("Must have Origin and Destination entries.");
    } else {

        document.getElementById('submit').disabled = false;
        document.getElementById('submit').style.opacity = "1";
        document.getElementById('clear').disabled = false;
        document.getElementById('clear').style.opacity = "1";

        count++;
        if (count == 3) {
            document.getElementById('add_button').disabled = true;
            document.getElementById('add_button').style.opacity = "0.5";

        }

        var origin = document.getElementById('origin_address');
        var destination = document.getElementById('destination_address');
        var addresses = document.getElementById('addresses');
        var originValue = origin.value;
        var destinationValue = destination.value;


        origins_array.push(originValue);
        destinations_array.push(destinationValue);
        addresses.innerHTML += "<li>From: " + originValue + " / To: " + destinationValue + "</li>"
    }
}

function clearChoices() {
    document.getElementById('addresses').innerHTML = "";
    origins_array = [];
    destinations_array = [];
    count = 0;
    document.getElementById('add_button').disabled = false;
    document.getElementById('add_button').style.opacity = "1";
    document.getElementById('clear').disabled = true;
    document.getElementById('clear').style.opacity = "0.5";
    document.getElementById('submit').disabled = true;
    document.getElementById('submit').style.opacity = "0.5";


}

function submitFunction() {
    data['origins'] = origins_array;
    data['destinations'] = destinations_array;
    data['key'] = '';


    xhr = new XMLHttpRequest();
    var url = "/test2";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById('results').innerHTML = "";
            var content = JSON.parse(xhr.responseText);
            var google = content['google'];
            var googleStatus = google['status'];

            if (googleStatus == 'OK') {
                var orig = google['origin_addresses'];
                var dest = google['destination_addresses'];
                //var elements = google['rows'][0]['elements'][0];
                var rows = google['rows'];

            }
            var orig_address_count = orig.length;
            var dest_address_count = dest.length;
            for (var i = 0; i < orig_address_count; i++) {
                for (var j = 0; j < dest_address_count; j++) {
                    var start_address = rows[i]['elements'][j];
                    if ((start_address['status'] == 'OK' )) {
                        var distance = start_address['distance']['text'];
                        var duration = start_address['duration']['text'];
                        document.getElementById('results').innerHTML += "<p> From: " + orig[i] + "<br> To: " + dest[j] +
                            "<br>Distance: " + distance + "<br> Duration: " + duration +
                            "</p><br>";

                    } else {
                        document.getElementById('results').innerHTML += "<p> From: " + orig[i] + "<br> To: " + dest[j] +
                            "<br>Distance: No available data. <br> Duration: No available data.</p><br>";
                    }
                }
            }
            document.getElementById('addresses').innerHTML = "";
            origins_array = [];
            destinations_array = [];
            count = 0;
            document.getElementById('add_button').disabled = false;
            document.getElementById('add_button').style.opacity = "1";
            document.getElementById('clear').disabled = true;
            document.getElementById('clear').style.opacity = "0.5";
            document.getElementById('submit').disabled = true;
            document.getElementById('submit').style.opacity = "0.5";

        }
    };
    
    var json_string_data = JSON.stringify(data);
    xhr.send(json_string_data);
    document.getElementById('results').innerHTML = "Requesting data...";
    
}

window.onload = function() {
    orig_text = document.getElementById('origin_address');
    dest_text = document.getElementById('destination_address');

    document.getElementById('clear').disabled = true;
    document.getElementById('clear').style.opacity = "0.5";
    document.getElementById('submit').disabled = true;
    document.getElementById('submit').style.opacity = "0.5";
};
