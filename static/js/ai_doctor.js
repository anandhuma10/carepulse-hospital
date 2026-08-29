//AI Doctor Recommendation Script
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

        loading.style.display = "block";
        errorMessage.style.display = "none";
        recommendationResult.style.display = "none";

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


            const data = await response.json();


                    if (!response.ok) {
            console.log("API ERROR RESPONSE:", data);

            throw new Error(
                data.detail ||
                data.body_area?.[0] ||
                data.symptom?.[0] ||
                "Unable to get recommendation."
            );
        }


            department.textContent =
                data.department || "Not available";

            reason.textContent =
                data.reason || "No reason provided.";


            doctorsList.innerHTML = "";


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


            recommendationResult.style.display = "block";

        } catch (error) {

            console.error(
                "AI recommendation error:",
                error
            );

            errorMessage.textContent =
                error.message || "Something went wrong.";

            errorMessage.style.display = "block";

        } finally {

            loading.style.display = "none";
            recommendButton.disabled = false;
        }
    });
});

