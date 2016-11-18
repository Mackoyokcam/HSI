function id(element) {
	return document.getElementById(element);
}

var geocoder;
var map;

function initMap() {
	geocoder = new google.maps.Geocoder();
	var bellingham = {lat: 48.749, lng: -122.479}; // downtown bellingham
	map = new google.maps.Map(id('map'), {
		zoom: 12,
		center: bellingham
	});
}

function searchAddress() {
	var addressText = id("search-box").value;
	geocoder.geocode( {"address": addressText}, function(results, status) {
		if (status == "OK") {
			var loc = results[0].geometry.location;
			map.setCenter(loc);
		} else {
			alert("Geocode was not successful for the folowing reason:" + status);
		}
	});
}

window.onload = function() {
	id("search-button").onclick = searchAddress;
}