// Variables
let isAnimating = false;
let currentHour = 0; // TODO: Start from the current hour?
let totHours = 24; // Show only one day forecast
let imagesAirqMap = [];
let imagesMeteoMap = [];
let interval = null; // Function that repeatedly calls updateMap

// Elements
const airQualityForecastMap = document.getElementById("air-quality-map");
const meteoMap = document.getElementById("meteo-map");
const toggleBtn = document.getElementById("toggle-play");
const timeSlider = document.getElementById("time-slider");
const currentTime = document.getElementById("current-time");
const hourDisplay = document.getElementById("hour-display");
const paramSelector = document.getElementById("parameter");


// Read in the selected parameter
let param = paramSelector.value;

function updateForecast(plots, param) {
    console.log("Updating forecast for param:", param);

    // Reset forecast vectors
    imagesAirqMap = [];
    currentHour = 0;

    plots.forEach((plot, index) => {
        const imgSrc = plot.url;
        imagesAirqMap.push(imgSrc);
    });

    // Set first images
    airQualityForecastMap.src = imagesAirqMap[0];

    // Slider settings
    timeSlider.value = 0;
    timeSlider.max = imagesAirqMap.length - 1;
    timeSlider.step = 1;

    // Hour display
    updateCurrentHour(0);
}

function updateMeteoMap(plots) {
    imagesMeteoMap = [];

    plots.forEach((plot, index) => {
        const imgSrc = plot.url;
        imagesMeteoMap.push(imgSrc);
    })

    meteoMap.src = imagesMeteoMap[0];
}

// Functions
function updateMap() {
    airQualityForecastMap.src = imagesAirqMap[currentHour];
    meteoMap.src = imagesMeteoMap[currentHour];
    //hourDisplay.textContent = currentHour.toString().padStart(2, "0");
    timeSlider.value = currentHour.toString();
}

function startAnimation() {
    interval = setInterval(() => {
        updateCurrentHour((currentHour + 1) % imagesAirqMap.length); // Update the next hour
        updateMap();
    }, 1000);
}

function stopAnimation() {
    clearInterval(interval);
    interval = null;
}

function updateCurrentHour(hour) {
    currentHour = Number(hour);
}

function clearOptions(selectElement) {
    var i, L = selectElement.options.length - 1;
    for(i = L; i >= 0; i--) {
       selectElement.remove(i);
    }
 }

// Event listeners
toggleBtn.addEventListener("click", () => {
    isAnimating = !isAnimating;

    if (isAnimating) {
        toggleBtn.textContent = "Pause";
        startAnimation();
    } else {
        toggleBtn.textContent = "Start";
        stopAnimation();
    }
});

timeSlider.addEventListener("input", (e) => {
    updateCurrentHour(Number(e.target.value));
    updateMap();
});

paramSelector.addEventListener("change", () => {
    console.log("Param changed, reinitializing map");
    let param = paramSelector.value;

    // Send the selected param backend
    fetch(`/get-forecast-plots?variable=${param}`)
        .then(response => response.json())
        .then(images => {
            console.log("Images returned from backend:", images);

            updateForecast(images, param);
        })
        .catch(error => {
            console.error("Error fetching images:", error);
        });


    updateCurrentHour(0);
});

// Load data for default parameter
window.addEventListener("DOMContentLoaded", () => {
    const defaultParam = "PM25";
    paramSelector.value = defaultParam; // Set default variable selected

    console.log("loading default images for ", defaultParam);

    fetch(`/get-forecast-plots?variable=${defaultParam}`)
        .then(response => response.json())
        .then(images => {
            console.log("Default images loaded");
            updateForecast(images, defaultParam);
            updateCurrentHour(0);
        })
        .catch(error => {
            console.error("Error loading default images:", error);
        });
    
    fetch(`get-meteo-plots`)
        .then(response => response.json())
        .then(images => {
            console.log("Meteorological map loaded");
            updateMeteoMap(images);
        })
        .catch(error => {
            console.error("Error loading meteorological forecast data:", error);
        })
});
