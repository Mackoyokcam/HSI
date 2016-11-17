function id(element) {
	return document.getElementById(element);
}

var geocoder;
var map;

function initialize() {
	geocoder = new google.maps.Geocoder();
	var bellingham = new google.maps.LatLng(48.749, -122.479); // downtown bellingham
	var mapOptions = {
		zoom: 8,
		center: bellingham;
	}
	map = new google.maps.Map(id("map"), mapOptions);
}

function searchAddress() {
	var addressText = id("address").value;
	geocoder.geocode( {"address": addressText}, function(results, status) {
		if (status == "OK") {
			map.setCenter(results[0].geometry.location);
		} else {
			alert("Geocode was not successful for the folowing reason:" + status);
		}
	});
}

// window.onload = function() {
// 	id("search-button").onclick = searchAddress;
// }