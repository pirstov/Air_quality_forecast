// Variables
let isAnimating = false;
let currentHour = 0; // TODO: Start from the current hour?
let totHours = 24; // Show only one day forecast
let imagesAeroMap = [];
let imagesMeteoMap = [];
let interval = null; // Function that repeatedly calls updateMaps
let plotsPreloaded = false;

// Elements
const aerosolForecastMap = document.getElementById("aerosol-map");
const meteoMap = document.getElementById("aero-meteo-map");
const toggleBtn = document.getElementById("aero-toggle-play");
const timeSlider = document.getElementById("aero-time-slider");
const hourDisplay = document.getElementById("aero-hour-display");
const aeroSelector = document.getElementById("aerosol");


// Read in the selected parameter
let param = aeroSelector.value;

function initializeMaps(aero_plots, meteo_plots) {
    // Reset forecast vectors
    imagesAeroMap = [];
    imagesMeteoMap = [];

    currentHour = 0;

    aero_plots.forEach((plot) => {
        const imgSrc = plot.url;
        imagesAeroMap.push(imgSrc);
    });

    meteo_plots.forEach((plot) => {
        const imgSrc = plot.url;
        imagesMeteoMap.push(imgSrc);
    });
    
    // Continue setup only after all images have been loaded to avoid forecast
    // plots going out of sync
    Promise.all([
        preloadImages(imagesAeroMap),
        preloadImages(imagesMeteoMap)
    ]).then(() => {
        plotsPreloaded = true;
        // Set first images
        aerosolForecastMap.src = imagesAeroMap[0];
        meteoMap.src = imagesMeteoMap[0];

        // Slider settings
        timeSlider.value = 0;
        timeSlider.max = imagesAeroMap.length - 1;
        timeSlider.step = 1;

        // Update hour display: now only for debugging
        updateCurrentHour(0);
    }).catch(err => {
        console.log("Error initializing forecast plots:", err);
    });
}

function updateForecastMap(aero_plots, param) {
    console.log("Updating forecast for param:", param);

    imagesAeroMap = [];
    currentHour = 0;

    aero_plots.forEach((plot) => {
        const imgSrc = plot.url;
        imagesAeroMap.push(imgSrc);
    });

    // Set slider to 0 for both maps after param change
    aerosolForecastMap.src = imagesAeroMap[0];
    meteoMap.src = imagesMeteoMap[0];

    timeSlider.value = 0;
    timeSlider.max = imagesAeroMap.length - 1;
    timeSlider.step = 1;

    // Hour display, remove if unnecessary
    updateCurrentHour(0);
}

function updateMaps() {
    if (!plotsPreloaded) {
        console.log("Plots not yet preloaded, can't update maps");
        return;
    }
    // console.log("Displaying hour:", currentHour); // debug log
    aerosolForecastMap.src = imagesAeroMap[currentHour];
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

// Shared functions
function startAnimation() {
    interval = setInterval(() => {
        updateCurrentHour((currentHour + 1) % imagesAeroMap.length); // Update the next hour
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
    updateMaps();
});
// Shared functions 


aeroSelector.addEventListener("change", () => {
    console.log("Param changed, reinitializing map");
    let param = aeroSelector.value;

    // Send the selected param backend
    fetch(`/get-aerosol-plots?variable=${param}`)
        .then(response => response.json())
        .then(images => {
            console.log("Images returned from backend:", images);

            updateForecastMap(images, param);
        })
        .catch(error => {
            console.error("Error fetching images:", error);
        });


    updateCurrentHour(0);
});


// Load data for default parameter
window.addEventListener("DOMContentLoaded", () => {
    const defaultParam = "BCAR";
    aeroSelector.value = defaultParam;

    console.log("loading default images for ", defaultParam);

    Promise.all([
        fetch(`/get-aerosol-plots?variable=${defaultParam}`)
            .then(res => res.json()),
        fetch(`/get-meteo-plots`).
            then(res => res.json())
    ])
    .then(([forecastData, meteoData]) => {
        console.log("Both forecast and meteo data loaded");
        initializeMaps(forecastData, meteoData, defaultParam);
    })
    .catch(error => {
        console.error("Error loading forecast or meteo data:", error);
    });

});