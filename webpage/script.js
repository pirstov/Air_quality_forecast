// Variables
let isAnimating = false; // TODO: implement animation
//let isLooping = false; // TODO: ???
let currentHour = 0; // TODO: Start from the current hour
let totHours = 3; // TODO: Decide how far to forecast
let images = [];
let interval = null; // Function that repeatedly calls updateMap

// Elements
const forecastMap = document.getElementById("forecast-map");
const toggleBtn = document.getElementById("toggle-play");
const timestepContainer = document.getElementById("timestep-container");
const currentTime = document.getElementById("current-time");
const datePicker = document.getElementById("date");


// Add time steps and add images to the images array
for (let i = 0; i < totHours; i++) {
    const hour = (i + 1).toString().padStart(2, "0");
    //console.log(hour);
    images.push(`data/heatmap-${hour}.png`);
    const timeStep = document.createElement("div");
    timeStep.classList.add("time-step");
    timeStep.textContent = hour;
    //timeStep.addEventListener("click", () => goToHour(i)); // TODO: Add time step button functionality
    timestepContainer.appendChild(timeStep);
}

// Functions
function updateMap() {
    console.log("current time:", currentHour);
    forecastMap.src = images[currentHour];
    document.getElementById("hour-display").textContent=(currentHour + 1).toString().padStart(2, "0");
    console.log("image src: ", images[currentHour])
}

function startAnimation() {
    interval = setInterval(() => {
        currentHour = (currentHour + 1) % totHours; // Loop through the images
        updateMap();
        //updateTimesteps(); // TODO: highlight the current timestep
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
