document.addEventListener('DOMContentLoaded', function() {
    // Initial page load: Fetch and display appointments based on the user's default view
    fetchAppointments();

    // Toggle view when the button is clicked
    document.getElementById('toggleViewBtn').addEventListener('click', function() {
        toggleView();
    });
});

function fetchAppointments() {
    // Fetch appointments based on the user's view and update the UI
    let endpoint = '/get_appointments';  // Update with your actual endpoint
    fetch(endpoint, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        // Update the UI with the fetched appointments
        updateAppointmentsList(data);
    })
    .catch(error => {
        console.error('Error fetching appointments:', error);
    });
}

function toggleView() {
    // Toggle between personal and business views
    let endpoint = '/toggle_view';  // Update with your actual endpoint
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        // Update the UI with the toggled view
        updateAppointmentsList(data);
    })
    .catch(error => {
        console.error('Error toggling view:', error);
    });
}

function updateAppointmentsList(appointments) {
    // Update the appointments list in the UI
    let appointmentsList = document.getElementById('appointmentsList');
    appointmentsList.innerHTML = '';  // Clear existing content

    for (let appointment of appointments) {
        // Create list item for each appointment and append to the list
        let listItem = document.createElement('li');
        listItem.innerHTML = `
            <!-- Display appointment details -->
            <h2>${appointment.business.location}</h2>
            <p>${appointment.business.bio}</p>
            <strong>Date:</strong> ${appointment.date_of_apt}<br>
            <strong>Time:</strong> ${appointment.start_time}<br>
            <!-- Add more appointment details as needed -->
        `;
        appointmentsList.appendChild(listItem);
    }
}
