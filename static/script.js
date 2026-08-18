const fileInput = document.getElementById("resumes");
const fileList = document.getElementById("fileList");
const form = document.getElementById("analyzeForm");
const analyzeButton = document.getElementById("analyzeButton");


fileInput.addEventListener("change", function () {

    fileList.innerHTML = "";

    const files = fileInput.files;

    for (const file of files) {

        const item = document.createElement("div");

        item.className = "file-item";

        item.textContent = file.name;

        fileList.appendChild(item);
    }
});


form.addEventListener("submit", function () {

    analyzeButton.disabled = true;

    analyzeButton.textContent = "Analyzing Candidates...";
});