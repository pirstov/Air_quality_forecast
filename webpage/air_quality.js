// Variables
let isAnimating = false;
//let isLooping = false; // TODO: ???
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
const datePicker = document.getElementById("date");
const hourDisplay = document.getElementById("hour-display");
const mapSelector = document.getElementById("source");
const paramSelector = document.getElementById("parameter");


// Initialization functions
function initializeDatePicker() {
    // Initialize dates in datepicker
    // TODO: fetch the data and show dates based on the data, later just list of dates?
    currentDate = new Date();
    datePicker.value = currentDate.toISOString().split("T")[0];
    startOfWeek = new Date();
    // Set the min time to the beginning of current week
    startOfWeek.setDate(currentDate.getDate() - (currentDate.getDay() - 1));
    datePicker.min = startOfWeek.toISOString().split("T")[0]; // Dates need to be strings
    datePicker.max = currentDate.toISOString().split("T")[0];
}

// Read in the selected parameter
let param = paramSelector.value;
// Read in the source to determine which map to show
let mapSource = mapSelector.value;

function initializeForecast(mapSource, param) {
    imagesAirqMap = [];
    imagesMeteoMap = [];

    if (mapSource === "source1") { // Finland
        console.log("Initializing map of Finland");

        airQualityForecastMap.style.display = "inline-block";
        meteoMap.style.display = "inline-block"; // Show the meteorological forecast map

        // Load one day data from a fixed path
        for (let i = 0; i < totHours; i++) {
            const hour = i.toString().padStart(2, "0");
            imagesAirqMap.push(`pm_plots/20240220_${hour}.png`);
            // TODO: Add correct images to meteorological map
            imagesMeteoMap.push(`pm_plots/20240220_${hour}.png`);
        }

        // Set default plots
        airQualityForecastMap.src = imagesAirqMap[0]; //"pm_plots/20240220_00.png";
        meteoMap.src = imagesMeteoMap[0]; //"pm_plots/20240220_00.png";

    } else if (mapSource === "source2") { // Helsinki
        console.log("Initializing placeholder map of Helsinki");
        imagesAirqMap.push(`helsinki_placeholder.png`);

        console.log("images.length:", imagesAirqMap.length);

        // Set default plot
        airQualityForecastMap.src = imagesAirqMap[0];

        airQualityForecastMap.style.display = "inline-block";
        meteoMap.style.display = "none";  // Hide meteorological map for Helsinki
        return;
    } else {
        console.log("Unknown map source:", mapSource);
    }

    // Initialize slider
    timeSlider.max = imagesAirqMap.length - 1;
    timeSlider.step = 1;
    console.log("images.length:", imagesAirqMap.length);

    // Initialize hour display
    hourDisplay.textContent = currentHour.toString().padStart(2, "0");
}

initializeDatePicker();
initializeForecast(mapSource, param);

// Functions
function updateMap() {
    airQualityForecastMap.src = imagesAirqMap[currentHour];
    meteoMap.src = imagesMeteoMap[currentHour];
    hourDisplay.textContent = currentHour.toString().padStart(2, "0");
    timeSlider.value = currentHour.toString();
    //console.log("current time:", currentHour, "image src: ", images[currentHour])
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

datePicker.addEventListener("change", (e) => {
    console.log("Picked date", datePicker.value);
    cDate = new Date();
    console.log(cDate.getDay());
});

timeSlider.addEventListener("input", (e) => {
    updateCurrentHour(Number(e.target.value));
    updateMap();
});

mapSelector.addEventListener("change", () => {
    console.log("Map source changed, reinitializing map");
    let mapSource = mapSelector.value;
    let param = paramSelector.value;
    initializeForecast(mapSource, param);
});

paramSelector.addEventListener("change", () => {
    console.log("Param changed, reinitializing map");
    let mapSource = mapSelector.value;
    let param = paramSelector.value;
    initializeForecast(mapSource, param);
});
