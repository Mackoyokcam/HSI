function id(element) {
	return document.getElementById(element);
}

var geocoder;
var map;

function initMap() {
	geocoder = new google.maps.Geocoder();
	var addressText = id("address-text").innerText;
	if (addressText == null || addressText.trim() == '') {
		var bellingham = {lat: 48.749, lng: -122.479}; // downtown bellingham
		var map = new google.maps.Map(id('map'), {
			zoom: 12,
			center: bellingham
		});
		var marker = new google.maps.Marker({
			position: bellingham,
			map: map,
			title: 'downtown bellingham'
		});
	} else {
		var addressText = id("address-text").innerText;
		geocoder.geocode( {"address": addressText}, function(results, status) {
			if (status == "OK") {
				var loc = results[0].geometry.location;
				var map = new google.maps.Map(id('map'), {
					zoom: 12,
					center: loc
				});
				var marker = new google.maps.Marker({
					position: loc,
					map: map,
					title: addressText
				});
			} else {
				alert("Geocode was not successful for the folowing reason:" + status);
			}
		});
	}
}

function searchAddress() {
	var addressText = id("search-box").value;
	// id("street-view").src = "https://maps.googleapis.com/maps/api/streetview?size=600x600&location=" + addressText + "&key=AIzaSyCb1JuqcxzEU3MPPJ3oaFN1GkCur7go-oA";
	geocoder.geocode( {"address": addressText}, function(results, status) {
		if (status == "OK") {
			var loc = results[0].geometry.location;
			map.setCenter(loc);
			var marker = new google.maps.Marker({
				position: loc,
				map: map,
				title: addressText
			});
		} else {
			alert("Geocode was not successful for the folowing reason:" + status);
		}
	});
}

window.onload = function() {
	id("search-button").onclick = searchAddress;
}