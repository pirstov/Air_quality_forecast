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
    console.log("Called with source", mapSource, "and param", param);
    if (mapSource === "source1") {
        console.log("Initializing map of Finland");
    } else if (mapSource === "source2") { // TODO: Actual implementation
        console.log("Initializing placeholder maps of Europe");
        // Clear current map arrays and fill with correct plots
        imagesAirqMap = [];
        imagesMeteoMap = [];
        imagesAirqMap.push(`europe_placeholder.png`);
        imagesMeteoMap.push(`europe_placeholder.png`);
        // Set default plots
        airQualityForecastMap.src = "europe_placeholder.png";
        meteoMap.src = "europe_placeholder.png";
        // Initialize slider
        timeSlider.value = 0;
        timeSlider.max = imagesAirqMap.length - 1;
        timeSlider.step = 1;
        console.log("images.length:", imagesAirqMap.length);

        // Initialize hour display
        hourDisplay.textContent = currentHour.toString().padStart(2, "0");
        return;
    } else {
        console.log("Unknown map source:", mapSource);
    }

    // Load one day data from a fixed path
    for (let i = 0; i < totHours; i++) {
        const hour = i.toString().padStart(2, "0");
        imagesAirqMap.push(`pm_plots/20240220_${hour}.png`);
        // TODO: Add correct images to meteorological map
        imagesMeteoMap.push(`pm_plots/20240220_${hour}.png`);
    }

    // Set default plot
    airQualityForecastMap.src = "pm_plots/20240220_00.png";
    meteoMap.src = "pm_plots/20240220_00.png";

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
