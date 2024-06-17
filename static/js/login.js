// static/js/login.js

document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    fetch('/custom-login/', {  // Make sure the URL matches the endpoint in your urls.py
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        },
        
    })
    .then(response => {
        console.log("Hello");
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        console.log(response);
        return response.json();
    })
    .then(data => {
        if (data.success) {
            window.location.href = '/student/dashboard';  // Redirect to home page after successful login
        } else {
            document.getElementById('error-message').innerText = data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});




function fetchProjectDetails() {
    fetch('/get-project-details/')
        .then(response => response.json())
        .then(data => displayProjectDetails(data))
        .catch(error => console.error('Error fetching project details:', error));
}

// Function to display project details on the webpage
function displayProjectDetails(projects) {
    var projectDetailsElement = document.getElementById("projectDetails");

    // Clear previous content
    projectDetailsElement.innerHTML = "";

    // Loop through each project and create HTML elements to display details
    projects.forEach(function(project) {
        var projectDiv = document.createElement("div");

        // Create HTML elements for each project detail
        var collegeNameElement = document.createElement("p");
        collegeNameElement.textContent = "College Name: " + project.college_name;

        var projectNameElement = document.createElement("p");
        projectNameElement.textContent = "Project Name: " + project.project_name;

        var descriptionElement = document.createElement("p");
        descriptionElement.textContent = "Description: " + project.description;

        var techStackElement = document.createElement("p");
        techStackElement.textContent = "Tech Stack: " + project.tech_stack;

        // Append project details to the projectDiv
        projectDiv.appendChild(collegeNameElement);
        projectDiv.appendChild(projectNameElement);
        projectDiv.appendChild(descriptionElement);
        projectDiv.appendChild(techStackElement);

        // Append projectDiv to the projectDetailsElement
        projectDetailsElement.appendChild(projectDiv);
    });
}

//Call the fetchProjectDetails function to fetch and display the project details
fetchProjectDetails();