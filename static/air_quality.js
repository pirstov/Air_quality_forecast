// Variables
let isAnimating = false;
let currentHour = 0; // TODO: Start from the current hour?
let totHours = 24; // Show only one day forecast
let imagesAirqMap = [];
let imagesMeteoMap = [];
let interval = null; // Function that repeatedly calls updateMap
let plotsPreloaded = false;

// Elements
const airQualityForecastMap = document.getElementById("air-quality-map");
const meteoMap = document.getElementById("airq-meteo-map");
const toggleBtn = document.getElementById("airq-toggle-play");
const timeSlider = document.getElementById("airq-time-slider");
const hourDisplay = document.getElementById("airq-hour-display");
const paramSelector = document.getElementById("parameter");


// Read in the selected parameter
let param = paramSelector.value;

function initializeMaps(airq_plots, meteo_plots) {
    // Reset air quality map vector
    imagesAirqMap = [];
    imagesMeteoMap = [];
    currentHour = 0;

    airq_plots.forEach((plot) => {
        const imgSrc = plot.url;
        imagesAirqMap.push(imgSrc);
    });

    meteo_plots.forEach((plot) => {
        const imgSrc = plot.url;
        imagesMeteoMap.push(imgSrc);
    });

    // Continue setup only after all images have been loaded to avoid forecast
    // plots going out of sync
    Promise.all([
        preloadImages(imagesAirqMap),
        preloadImages(imagesMeteoMap)
    ]).then(() => {
        plotsPreloaded = true;
        // Set first images
        airQualityForecastMap.src = imagesAirqMap[0];
        meteoMap.src = imagesMeteoMap[0];

        // Slider settings
        timeSlider.value = 0;
        timeSlider.max = imagesAirqMap.length - 1;
        timeSlider.step = 1;

        // Hour display
        updateCurrentHour(0);
    }).catch(err => {
        console.log("Error initializing forecast plots:", err);        
    })
}

function updateForecastMap(airq_plots, param) {
    console.log("Updating forecast for param:", param);

    imagesAirqMap = [];
    currentHour = 0;

    airq_plots.forEach((plot) => {
        const imgSrc = plot.url;
        imagesAirqMap.push(imgSrc);
    });

    // Set slider to 0 for both maps after param change
    airQualityForecastMap.src = imagesAirqMap[0];
    meteoMap.src = imagesMeteoMap[0];

    timeSlider.value = 0;
    timeSlider.max = imagesAirqMap.length - 1;
    timeSlider.step = 1;

    // Resetting hour display for debugging
    updateCurrentHour(0);
}

// Functions
function updateMaps() {
    if (!plotsPreloaded) {
        console.log("Plots not yet preloaded, can't update maps");
        return;
    }
    // console.log("Displaying hour:", currentHour); // debug log
    airQualityForecastMap.src = imagesAirqMap[currentHour];
    meteoMap.src = imagesMeteoMap[currentHour];
    //hourDisplay.textContent = currentHour.toString().padStart(2, "0");
    timeSlider.value = currentHour.toString();
}

function preloadImages(urls) {
    plotsPreloaded = false;
    return Promise.all(urls.map((url) => {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.src = url;
            img.onload = resolve;
            img.onerror = reject;
        });
    }));
}

function startAnimation() {
    interval = setInterval(() => {
        updateCurrentHour((currentHour + 1) % imagesAirqMap.length); // Update the next hour
        updateMaps();
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
    // If the plots preloading is not done, do nothing
    if (!plotsPreloaded) {
        return;
    }

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

    Promise.all([
    fetch(`/get-forecast-plots?variable=${defaultParam}`)
            .then(res => res.json()),
        fetch(`/get-meteo-plots`)
            .then(res => res.json())
    ])
    .then(([forecastData, meteoData]) => {
        console.log("Both forecast and meteo data loaded");
        initializeMaps(forecastData, meteoData)
    })
    .catch(error => {
        console.error("Error loading forecast or meteo data:", error);
    });
});
