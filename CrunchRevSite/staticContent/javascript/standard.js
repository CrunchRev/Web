document.addEventListener("DOMContentLoaded", function() {
    const crunchTokensElements = document.querySelectorAll('.crunch-tokens');
    crunchTokensElements.forEach(function(element) {
        const number = parseInt(element.textContent.replace(/,/g, ''), 10);
        if (!isNaN(number)) {
            element.textContent = number.toLocaleString();
            element.setAttribute('title', `You have ${number.toLocaleString()} Crunches.`);
        }
    });
});