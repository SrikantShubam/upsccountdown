

document.addEventListener('DOMContentLoaded', function() {
    updateDetailedCountdown();
    setInterval(updateDetailedCountdown, 1000); // Update every second
    quote();
});

function updateDetailedCountdown() {
    let daysBox = document.getElementById('Days');
    let hoursBox = document.getElementById('Hours');
    let minutesBox = document.getElementById('Minutes');
    let secondsBox = document.getElementById('Seconds');

    // Get the exam's exact end date-time from the "Date of Commencement of Exam"
    let examDateString = document.querySelector('h3').textContent.trim();
    let [day, month, year] = examDateString.split('.');
    let examDate = new Date(year, month - 1, day, 0, 0, 0, 0); // JS month is 0-based

    let now = new Date();
    let timeDifference = examDate - now; // In milliseconds

    if (timeDifference > 0) {
        let totalSecondsLeft = Math.floor(timeDifference / 1000);
        let daysLeft = Math.floor(totalSecondsLeft / (24 * 60 * 60));
        totalSecondsLeft -= daysLeft * 24 * 60 * 60;
        let hoursLeft = Math.floor(totalSecondsLeft / (60 * 60));
        totalSecondsLeft -= hoursLeft * 60 * 60;
        let minutesLeft = Math.floor(totalSecondsLeft / 60);
        totalSecondsLeft -= minutesLeft * 60;

        daysBox.textContent = daysLeft;
        hoursBox.textContent = hoursLeft;
        minutesBox.textContent = minutesLeft;
        secondsBox.textContent = totalSecondsLeft;
    } else {
        daysBox.textContent = "0";
        hoursBox.textContent = "0";
        minutesBox.textContent = "0";
        secondsBox.textContent = "0";
    }
}
function quote() {
    fetch("https://type.fit/api/quotes")
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            // Get a random index between 0 and the length of the quotes array
            const randomIndex = Math.floor(Math.random() * data.length);

            // Get the random quote text
            const randomQuoteText = data[randomIndex].text;

            // Display the quote on the page
            let quoteElement = document.getElementById("quote");
            quoteElement.textContent = randomQuoteText;
        });
}
    
