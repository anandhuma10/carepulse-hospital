// CarePulse AI Doctor Recommendation
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

    // Anatomy selector
    const anatomyOptions =
        document.querySelectorAll(".anatomy-option");

    const bodyAreaError =
        document.getElementById("bodyAreaError");


    // --------------------------------------------------
    // Anatomy selector
    // --------------------------------------------------

    anatomyOptions.forEach((option) => {

        option.addEventListener("click", () => {

            // Remove previous selection
            anatomyOptions.forEach((item) => {
                item.classList.remove("selected");
                item.setAttribute("aria-pressed", "false");
            });

            // Select clicked option
            option.classList.add("selected");
            option.setAttribute("aria-pressed", "true");

            // Store selected body area
            bodyAreaInput.value =
                option.dataset.bodyArea;

            // Hide validation message
            bodyAreaError.style.display = "none";
        });

    });


    // --------------------------------------------------
    // AI recommendation form
    // --------------------------------------------------

    form.addEventListener("submit", async (event) => {

        event.preventDefault();

        const symptom = symptomInput.value.trim();
        const bodyArea = bodyAreaInput.value.trim();


        // Validate body area
        if (!bodyArea) {

            bodyAreaError.style.display = "block";

            return;
        }


        // Validate symptoms
        if (!symptom) {
            symptomInput.focus();
            return;
        }


        // Show loading
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

                console.log(
                    "AI API ERROR:",
                    data
                );

                throw new Error(
                    data.detail ||
                    data.body_area?.[0] ||
                    data.symptom?.[0] ||
                    "Unable to get recommendation."
                );
            }


            // --------------------------------------------------
            // Display department
            // --------------------------------------------------

            department.textContent =
                data.department || "Not available";


            // --------------------------------------------------
            // Display reason
            // --------------------------------------------------

            reason.textContent =
                data.reason || "No reason provided.";


            // --------------------------------------------------
            // Display doctors
            // --------------------------------------------------

            doctorsList.innerHTML = "";


            if (
                data.doctors &&
                data.doctors.length > 0
            ) {

                data.doctors.forEach((doctor) => {

                    const listItem =
                        document.createElement("li");

                    listItem.textContent =
                        doctor.name;

                    doctorsList.appendChild(listItem);

                });

            } else {

                const listItem =
                    document.createElement("li");

                listItem.textContent =
                    "No doctors found for this department.";

                doctorsList.appendChild(listItem);
            }


            // Show result
            recommendationResult.style.display =
                "block";


        } catch (error) {

            console.error(
                "AI recommendation error:",
                error
            );


            errorMessage.textContent =
                error.message ||
                "Something went wrong.";


            errorMessage.style.display =
                "block";


        } finally {

            loading.style.display =
                "none";

            recommendButton.disabled =
                false;
        }

    });

});

