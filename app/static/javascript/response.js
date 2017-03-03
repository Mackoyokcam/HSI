var content = JSON.parse(json_content);

var orig, dest, elements, elementStatus, distance, duration, results, recycle, compost;

/* Google results */
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

/* HSI DB Query results */
var queryStatus = content['hsi_db']['addr']['status'];

if (queryStatus == 'True') {
    results = content['hsi_db']['addr']['results'];
    if (results['recycle'] == 'True')
        recycle = 'Yes';
    else
        recycle = 'No';
    if (results['compost'] == 'True')
        compost = 'Yes';
    else
        compost = 'No';

}

function loadJson() {
    var destination = document.getElementById('destination');
    var origin = document.getElementById('origin')
    if (googleStatus == 'OK') {
        if (queryStatus == 'True') {
            origin.innerHTML = "<p> Origin: " + orig +
                "<br> Rent: " + results['rent'] +
                "<br> Electric: " + results['electrical'] +
                "<br> Gas: " + results['gas'] +
                "<br> Water: " + results['water'] +
                "<br> Recycle: " + recycle +
                "<br> Compost: " + compost +
                "<br> Date Updated: " + results['updateDate'] +
                "</p><br>";
        } else {
            origin.innerHTML = "<p> No available data for this unit. </p>"
        }

        destination.innerHTML = "<p> Destination: " + dest + "</p>";

        if(elementStatus == 'OK') {
            destination.innerHTML = "" + destination.innerHTML +
                "<p> Distance: " + distance +
                "<br> Duration: " + duration +
                "</p>";

        } else {
            origin.innerHTML = "<p> No available data for this area. </p>";
        }
    }
}

window.onload = loadJson;


