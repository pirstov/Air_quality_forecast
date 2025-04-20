

window.addEventListener("DOMContentLoaded", () => {
    fetch("/get-validation-plots")
        .then(response => response.json())
        .then(images => {
            console.log("Validation plots loaded:", images);
            const container = document.querySelector(".eval-container");
            container.innerHTML = ""; // Clear placeholder <img>s

            images.forEach(plot => {
                const img = document.createElement("img");
                img.src = plot.url;
                img.alt = `Validation plot for ${plot.param}`;
                container.appendChild(img);
            });
        })
        .catch(error => {
            console.error("Error loading validation plots:", error);
        });
});