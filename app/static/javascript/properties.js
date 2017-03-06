function id(element) {
	return document.getElementById(element);
}

if (id("address-data") !== null) {
	var addressData = JSON.parse(addressDataJSON);
	var nearbyData = JSON.parse(nearbyDataJSON);
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
					zoom: 15,
					center: loc
				});
				var marker = new google.maps.Marker({
					position: loc,
					map: map,
					title: addressText
				});
				if (id("address-data") !== null) {
					loadNearby(map);
					console.log(nearbyData);
				}
			} else {
				console.log("Geocode was not successful for the folowing reason:" + status);
				var sorryMessage = document.createElement("p");
				sorryMessage.appendChild(document.createTextNode("Sorry, Google couldn't figure that address out..."));
				id("map").appendChild(sorryMessage);
			}
		});
	}
}

// populates the map with nearby locations present in the db
function loadNearby(map) {
	for (unit in nearbyData) {
		var lati = unit["lat"];
		var longi = unit["long"];
		console.log(lati)
		console.log(longi)
		var loc = {lat: lati, lng: longi};
		var marker = new google.maps.Marker({
			position: loc,
			map: map,
			title: unit["address"],
			icon: "http://maps.google.com/mapfiles/ms/icons/green-dot.png" // to differentiate
		});
	}
}

function newUnitSelected () {
	var unitList = id("unit-list");
	var selectedUnit = unitList.options[unitList.selectedIndex].text;
	var unitData = addressData[selectedUnit];
	populateData(unitData, selectedUnit);
}

function populateData(unitData, apartment) {
	id("apartment").innerHTML = "Apartment: ".concat(apartment);
	id("update-date").innerHTML = "Last Updated: ".concat(unitData["updateDate"]);
	id("rent").innerHTML = "Monthly Rent: ".concat(unitData["rent"]);
	id("gas").innerHTML = "Gas: ".concat(unitData["gas"]);
	id("electrical").innerHTML = "Electrical: ".concat(unitData["electrical"]);
	id("water").innerHTML = "Water: ".concat(unitData["water"]);
	id("recycle").innerHTML = "Recycle: ".concat((unitData["recycle"] === "True"?"yes":"no"));
	id("compost").innerHTML = "Compost: ".concat((unitData["compost"] === "True"?"yes":"no"));
}

window.onload = function () {
	if (id("address-data") !== null) {
		if (id("unit-list") !== null) {
			id("unit-list").onchange = newUnitSelected;
			id("unit-list")[0].selected = "selected";
			newUnitSelected();
		} else {
			var apartment = Object.keys(addressData)[0]
			populateData(addressData[apartment], apartment)
		}
	}

};