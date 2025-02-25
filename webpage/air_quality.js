// Variables
let isAnimating = false;
//let isLooping = false; // TODO: ???
let currentHour = 0; // TODO: Start from the current hour?
let totHours = 24; // TODO: determine from the selection, default to 3-day forecast?
let images = [];
let interval = null; // Function that repeatedly calls updateMap

// Elements
const forecastMap = document.getElementById("forecast-map");
const toggleBtn = document.getElementById("toggle-play");
const timeSlider = document.getElementById("time-slider");
const currentTime = document.getElementById("current-time");
const datePicker = document.getElementById("date");
const hourDisplay = document.getElementById("hour-display");


// Initialize dates in datepicker
// TODO: fetch the data and show dates based on the data, later just list of dates?
currentDate = new Date();
datePicker.value = currentDate.toISOString().split("T")[0];
startOfWeek = new Date();
// Set the min time to the beginning of current week
startOfWeek.setDate(currentDate.getDate() - (currentDate.getDay() - 1));
datePicker.min = startOfWeek.toISOString().split("T")[0]; // Dates need to be strings
datePicker.max = currentDate.toISOString().split("T")[0];

// TODO: load images based on the forecast length
// Load one day data
for (let i = 0; i < totHours; i++) {
    const hour = i.toString().padStart(2, "0");
    images.push(`pm_plots/20240220_${hour}.png`);
}

// Set default plot
forecastMap.src = "pm_plots/20240220_00.png"

// Initialize slider
timeSlider.max = images.length - 1;
timeSlider.step = 1;
console.log("images.length:", images.length);

// Initialize hour display
hourDisplay.textContent = currentHour.toString().padStart(2, "0");

// Functions
function updateMap() {
    forecastMap.src = images[currentHour];
    hourDisplay.textContent = currentHour.toString().padStart(2, "0");
    timeSlider.value = currentHour.toString();
    //console.log("current time:", currentHour, "image src: ", images[currentHour])
}

function startAnimation() {
    interval = setInterval(() => {
        updateCurrentHour((currentHour + 1) % images.length); // Update the next hour
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
