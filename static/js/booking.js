document.addEventListener("DOMContentLoaded", () => {
    const departmentSelect = document.getElementById("department");
    const doctorSelect = document.getElementById("doctor");
    const dateInput = document.getElementById("appointmentDate");
    const timeSlotSelect = document.getElementById("timeSlot");

    const doctorsDataElement = document.getElementById("doctors-data");

    if (
        !departmentSelect ||
        !doctorSelect ||
        !dateInput ||
        !timeSlotSelect ||
        !doctorsDataElement
    ) {
        return;
    }

    const doctors = JSON.parse(doctorsDataElement.textContent);

    // Prevent selecting a date in the past.
    const today = new Date();
    const todayString =
        `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;

    dateInput.min = todayString;

    function resetDoctorSelect(message) {
        doctorSelect.innerHTML = "";

        const option = document.createElement("option");
        option.value = "";
        option.textContent = message;
        option.disabled = true;
        option.selected = true;

        doctorSelect.appendChild(option);
        doctorSelect.disabled = true;
    }

    function resetTimeSlotSelect(message) {
        timeSlotSelect.innerHTML = "";

        const option = document.createElement("option");
        option.value = "";
        option.textContent = message;
        option.disabled = true;
        option.selected = true;

        timeSlotSelect.appendChild(option);
        timeSlotSelect.disabled = true;
    }

    // Department → Doctor
    departmentSelect.addEventListener("change", () => {
        const departmentId = Number(departmentSelect.value);

        doctorSelect.innerHTML = "";

        const matchingDoctors = doctors.filter(
            doctor => Number(doctor.department_id) === departmentId
        );

        if (matchingDoctors.length === 0) {
            resetDoctorSelect("No doctors available");
            resetTimeSlotSelect("No doctor available");
            return;
        }

        const defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.textContent = "Select Doctor";
        defaultOption.disabled = true;
        defaultOption.selected = true;

        doctorSelect.appendChild(defaultOption);

        matchingDoctors.forEach(doctor => {
            const option = document.createElement("option");

            option.value = doctor.id;
            option.textContent = `Dr. ${doctor.name}`;

            doctorSelect.appendChild(option);
        });

        doctorSelect.disabled = false;

        resetTimeSlotSelect("Select Doctor and Date First");
    });

    function generateTimeSlots(doctor, selectedDate) {
        if (!doctor || !selectedDate) {
            resetTimeSlotSelect("Select Doctor and Date First");
            return;
        }

        const selectedDateObject = new Date(
            `${selectedDate}T00:00:00`
        );

        const dayNames = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday"
        ];

        const selectedDay = dayNames[
            selectedDateObject.getDay()
        ];

        const workingDays = doctor.working_days
            .split(",")
            .map(day => day.trim());

        timeSlotSelect.innerHTML = "";

        if (!workingDays.includes(selectedDay)) {
            const option = document.createElement("option");

            option.value = "";
            option.textContent =
                `Doctor is not available on ${selectedDay}`;
            option.disabled = true;
            option.selected = true;

            timeSlotSelect.appendChild(option);
            timeSlotSelect.disabled = true;

            return;
        }

        const [fromHour, fromMinute] =
            doctor.available_from.split(":").map(Number);

        const [untilHour, untilMinute] =
            doctor.available_until.split(":").map(Number);

        let currentMinutes =
            fromHour * 60 + fromMinute;

        const endMinutes =
            untilHour * 60 + untilMinute;

        const defaultOption =
            document.createElement("option");

        defaultOption.value = "";
        defaultOption.textContent = "Select Time Slot";
        defaultOption.disabled = true;
        defaultOption.selected = true;

        timeSlotSelect.appendChild(defaultOption);

        // Generate 30-minute appointment slots.
        while (currentMinutes < endMinutes) {
            const hours = Math.floor(currentMinutes / 60);
            const minutes = currentMinutes % 60;

            const value =
                `${String(hours).padStart(2, "0")}:` +
                `${String(minutes).padStart(2, "0")}`;

            const displayDate = new Date(
                1970,
                0,
                1,
                hours,
                minutes
            );

            const displayText =
                displayDate.toLocaleTimeString(
                    "en-IN",
                    {
                        hour: "numeric",
                        minute: "2-digit"
                    }
                );

            const option =
                document.createElement("option");

            option.value = value;
            option.textContent = displayText;

            timeSlotSelect.appendChild(option);

            currentMinutes += 30;
        }

        timeSlotSelect.disabled = false;
    }

    function updateTimeSlots() {
        const doctorId =
            Number(doctorSelect.value);

        const selectedDate =
            dateInput.value;

        if (!doctorId || !selectedDate) {
            resetTimeSlotSelect(
                "Select Doctor and Date First"
            );
            return;
        }

        const doctor = doctors.find(
            item => Number(item.id) === doctorId
        );

        generateTimeSlots(
            doctor,
            selectedDate
        );
    }

    doctorSelect.addEventListener(
        "change",
        updateTimeSlots
    );

    dateInput.addEventListener(
        "change",
        updateTimeSlots
    );

    resetDoctorSelect("Select Department First");
    resetTimeSlotSelect("Select Doctor and Date First");
});