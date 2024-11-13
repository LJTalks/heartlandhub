document.addEventListener("DOMContentLoaded", function () {
    console.log("Script loaded");

    const listTypeCheckboxes = document.querySelectorAll("input[name='list_type']");
    const unsubscribeModal = new bootstrap.Modal(document.getElementById("unsubscribeModal"));
    const confirmUnsubscribeButton = document.getElementById("confirmUnsubscribe");
    const unsubscribedCheckbox = document.getElementById("unsubscribedCheckbox"); // Unsubscribed hidden checkbox
    const form = document.querySelector("form");
    let isUnsubscribing = false; // To track whether user confirmed unsubscribing

    /**
     * Function to check if all checkboxes are unchecked except "Unsubscribe"
     */
    function checkAllUnchecked() {
        return Array.from(listTypeCheckboxes).every(checkbox => checkbox === unsubscribedCheckbox || !checkbox.checked);
    }

    /**
     * Function to handle "Unsubscribe" checkbox selection
     */
    function toggleOtherCheckboxes() {
        if (unsubscribedCheckbox.checked) {
            listTypeCheckboxes.forEach(checkbox => {
                if (checkbox !== unsubscribedCheckbox) checkbox.disabled = true;
            });
        } else {
            listTypeCheckboxes.forEach(checkbox => checkbox.disabled = false);
        }
    }

    // Initial check on page load
    toggleOtherCheckboxes();

    /**
     * Event listener for each checkbox
     */
    listTypeCheckboxes.forEach((checkbox) => {
        checkbox.addEventListener("change", toggleOtherCheckboxes);
    });

    /**
     * Event listener for the form submit event
     * If all checkboxes are unchecked, trigger the confirmation modal.
     */
    form.addEventListener("submit", function (e) {
        if (checkAllUnchecked() && !isUnsubscribing) {
            e.preventDefault(); // Prevent form submission
            unsubscribeModal.show(); // Show the confirmation modal
        }
    });

    /**
     * Event listener for the unsubscribe confirmation button
     * If confirmed, allow form submission.
     */
    confirmUnsubscribeButton.addEventListener("click", function () {
        isUnsubscribing = true;

        if (checkAllUnchecked()) {
            unsubscribedCheckbox.checked = true; // Check the hidden Unsubscribed box
        }

        unsubscribeModal.hide(); // Hide the modal
        form.submit(); // Submit the form
    });
});