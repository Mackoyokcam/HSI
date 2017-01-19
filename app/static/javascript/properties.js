function id(element) {
	return document.getElementById(element);
}

var geocoder;
var map;

function initMap() {
	geocoder = new google.maps.Geocoder();
	var addressText = id("address-text").innerText;
	if (addressText == null || addressText.trim() == '') {
		// if nothing is in the search bar the map defaults
		// to downtown bellingham
		var bellingham = {lat: 48.7510528, lng: -122.4812339};
		var map = new google.maps.Map(id('map'), {
			zoom: 12,
			center: bellingham
		});
		var marker = new google.maps.Marker({
			position: bellingham,
			map: map,
			title: 'downtown bellingham'
		});
		id("address-text").innerText = "Bellingham";
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