// Variables
let isAnimating = false; // TODO: implement animation
//let isLooping = false; // TODO: ???
let currentHour = 0; // TODO: Start from the current hour
let totHours = 24; // TODO: Decide how far to forecast
let images = [];
let interval = null; // Function that repeatedly calls updateMap

// Elements
const forecastMap = document.getElementById("forecast-map");
const toggleBtn = document.getElementById("toggle-play");
const timeSlider = document.getElementById("time-slider");
const currentTime = document.getElementById("current-time");
const datePicker = document.getElementById("date");


// Update dates in datepicker
// TODO: fetch the data and show dates based on the data
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

// Functions
function updateMap() {
    forecastMap.src = images[currentHour];
    document.getElementById("hour-display").textContent=(currentHour + 1).toString().padStart(2, "0");
    console.log("current time:", currentHour, "image src: ", images[currentHour])
}

function startAnimation() {
    interval = setInterval(() => {
        currentHour = (currentHour + 1) % images.length; // Loop through the images
        updateMap();
    }, 1000);
}

function stopAnimation() {
    clearInterval(interval);
    interval = null;
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
