let linkCount = 0;
let redirectCount = 0;

function animateCounter(id, start, end) {
    let current = start;
    const interval = setInterval(() => {
        current++;
        document.getElementById(id).innerText = current;
        if (current >= end) clearInterval(interval);
    }, 30);
}

function shortenUrl() {
    const url = document.getElementById("urlInput").value;
    if (!url) return alert("Enter a URL!");

    const progress = document.querySelector(".progress");
    const bar = document.getElementById("progressBar");
    const result = document.getElementById("result");

    result.classList.remove("show");
    progress.style.display = "block";
    bar.style.width = "0%";

    let width = 0;
    const loading = setInterval(() => {
        width += 10;
        bar.style.width = width + "%";
        if (width >= 100) clearInterval(loading);
    }, 50);

    fetch("/shorten", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `url=${encodeURIComponent(url)}`
    })
    .then(res => res.json())
    .then(data => {
        setTimeout(() => {
            progress.style.display = "none";
            result.innerHTML = `
                Short URL:<br>
                <a href="${data.short_url}" target="_blank">${data.short_url}</a>
            `;
            result.classList.add("show");

            linkCount++;
            redirectCount++;
            animateCounter("links", linkCount - 1, linkCount);
            animateCounter("redirects", redirectCount - 1, redirectCount);
        }, 400);
    });
}
