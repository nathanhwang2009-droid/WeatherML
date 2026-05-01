// This file contains JavaScript code for client-side functionality, such as form validation or dynamic content updates.

document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("prediction-form");
    const resultDiv = document.getElementById("result");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            resultDiv.innerHTML = `<h3>Prediction Result: ${data.prediction}</h3>`;
        })
        .catch(error => {
            console.error("Error:", error);
            resultDiv.innerHTML = "<h3>There was an error processing your request.</h3>";
        });
    });
});