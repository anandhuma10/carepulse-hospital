// AI Doctor Recommendation Script

document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("aiRecommendationForm");

    // Stop if this page does not contain the AI form
    if (!form) {
        return;
    }

    const symptomInput = document.getElementById("symptom");
    const bodyAreaInput = document.getElementById("bodyArea");
    const recommendButton = document.getElementById("recommendButton");

    const loading = document.getElementById("loading");
    const errorMessage = document.getElementById("errorMessage");
    const recommendationResult =
        document.getElementById("recommendationResult");

    const department = document.getElementById("department");
    const reason = document.getElementById("reason");
    const doctorsList = document.getElementById("doctorsList");


    form.addEventListener("submit", async (event) => {

        event.preventDefault();

        const symptom = symptomInput.value.trim();
        const bodyArea = bodyAreaInput.value.trim();

        if (!symptom || !bodyArea) {
            return;
        }

        // Show loading
        loading.classList.remove("hidden");

        // Hide old messages/results
        errorMessage.classList.add("hidden");
        recommendationResult.classList.add("hidden");

        recommendButton.disabled = true;


        try {

            const response = await fetch(
                "/api/ai/recommend-doctor/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        symptom: symptom,
                        body_area: bodyArea
                    })
                }
            );


            // Read response as text first for debugging
            const responseText = await response.text();

            console.log("API STATUS:", response.status);
            console.log("API RESPONSE:", responseText);


            let data;

            try {

                data = JSON.parse(responseText);

            } catch (error) {

                throw new Error(
                    `Server returned non-JSON response (${response.status})`
                );
            }


            // Handle API errors
            if (!response.ok) {

                console.log("API ERROR RESPONSE:", data);

                throw new Error(
                    data.detail ||
                    data.body_area?.[0] ||
                    data.symptom?.[0] ||
                    "Unable to get recommendation."
                );
            }


            // Display department
            department.textContent =
                data.department || "Not available";


            // Display reason
            reason.textContent =
                data.reason || "No reason provided.";


            // Clear previous doctors
            doctorsList.innerHTML = "";


            // Display recommended doctors
            if (data.doctors && data.doctors.length > 0) {

                data.doctors.forEach((doctor) => {

                    const listItem = document.createElement("li");

                    listItem.textContent = doctor.name;

                    doctorsList.appendChild(listItem);
                });

            } else {

                const listItem = document.createElement("li");

                listItem.textContent =
                    "No doctors found for this department.";

                doctorsList.appendChild(listItem);
            }


            // Show result without overriding CSS layout
            recommendationResult.classList.remove("hidden");


        } catch (error) {

            console.error(
                "AI recommendation error:",
                error
            );

            errorMessage.textContent =
                error.message || "Something went wrong.";

            errorMessage.classList.remove("hidden");


        } finally {

            loading.classList.add("hidden");

            recommendButton.disabled = false;
        }
    });
});

