  document.addEventListener('DOMContentLoaded', function() {
    updateCountdowns();
    setInterval(updateCountdowns, 3600000); // Update every hour
});

function updateCountdowns() {
    let countdownElements = document.querySelectorAll('.countdown');

    countdownElements.forEach(function(element) {
        let daysBox = element.querySelector('#Days');
        let hoursBox = element.querySelector('#Hours');

        // Get days remaining from the HTML
        let days = parseInt(daysBox.textContent);

        // Calculate the exam's exact end date-time based on days till the exam
        let examDate = new Date();
        examDate.setDate(examDate.getDate() + days);
        examDate.setHours(0, 0, 0, 0); // Assuming exams start at 00:00:00 of the exam day

        let now = new Date();
        let timeDifference = examDate - now; // In milliseconds

        if (timeDifference > 0) {
            let totalHoursLeft = Math.floor(timeDifference / (1000 * 60 * 60)); // Total hours till the exam
            let daysLeft = Math.floor(totalHoursLeft / 24); // Days part of the countdown
            let remainingHours = totalHoursLeft % 24; // Hours part of the countdown

            if (days !== daysLeft) {
                daysBox.textContent = daysLeft; // Update days only if there's a change
            }
            hoursBox.textContent = remainingHours;
        } else {
            daysBox.textContent = "0";
            hoursBox.textContent = "0";
        }
    });
}

