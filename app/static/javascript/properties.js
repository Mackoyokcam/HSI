function id(element) {
	return document.getElementById(element);
}

var geocoder;
var map;

window.initMap = function() {
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
				console.log("Geocode was not successful for the folowing reason:" + status);
				var sorryMessage = document.createElement("p");
				sorryMessage.appendChild(document.createTextNode("Sorry, Google couldn't figure that address out..."));
				id("map").appendChild(sorryMessage);
			}
		});
	}
}

// var addressData = JSON.parse(addressDataJSON.replace(/'&#34;'/, '"'));

function newUnitSelected () {
	var unitList = id("unit-list");
	var selectedUnit = unitList.options[unitList.selectedIndex].text;
	console.log(selectedUnit);
	console.log(addressDataJSON);
}

window.onload = function () {
	id("unit-list").onchange = newUnitSelected;
};