// Update the active link in the navigation bar
document.addEventListener("DOMContentLoaded", function () {
    let currentPage = window.location.pathname.split("/").pop();
    let navItems = document.querySelectorAll(".topnav a");

    navItems.forEach(link => {
        if (link.getAttribute("href") == currentPage) {
            link.classList.add("active");
        }
    });
})