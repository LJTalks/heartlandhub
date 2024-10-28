document.addEventListener("DOMContentLoaded", function () {
    console.log("Script loaded");

    const listTypeCheckboxes = document.querySelectorAll("input[name='list_type']");
    const unsubscribeModal = new bootstrap.Modal(document.getElementById("unsubscribeModal"));
    const confirmUnsubscribeButton = document.getElementById("confirmUnsubscribe");
    const unsubscribedCheckbox = document.getElementById("unsubscribedCheckbox");
    const form = document.querySelector("form");
    let isUnsubscribing = false;  // To track whether the user confirmed unsubscribing

    /**
     * Function to check if all checkboxes are unchecked
     */
    function checkAllUnchecked() {
        return Array.from(listTypeCheckboxes).every(checkbox => !checkbox.checked);
    }

    /**
     * Event listener for the form submit event
     * If all checkboxes are unchecked, trigger the confirmation modal.
     */
    form.addEventListener("submit", function (e) {
        if (checkAllUnchecked() && !isUnsubscribing) {
            e.preventDefault();  // Prevent form submission
            unsubscribeModal.show();  // Show the confirmation modal
        }
    });

    /**
     * Event listener for the unsubscribe confirmation button
     * If confirmed, check the 'Unsubscribed' checkbox and allow form submission.
     */
    confirmUnsubscribeButton.addEventListener("click", function () {
        isUnsubscribing = true;
        console.log("Form submit triggered!");

        // Add 'Unsubscribed' to the list if no other lists are selected
        if (checkAllUnchecked()) {
            console.log("No list selected. Adding 'Unsubscribed'.");
            if (unsubscribedCheckbox) {
                unsubscribedCheckbox.checked = true;
            } else {
                console.error("'Unsubscribed' checkbox not found.");
            }
        }

        // Log form data just before submission for debugging purposes
        const formData = new FormData(form);
        for (let [key, value] of formData.entries()) {
            console.log(`${key}: ${value}`);
        }

        console.log("Unsubscribing: submitting form...");
        unsubscribeModal.hide();  // Hide the modal
        form.submit();  // Submit the form

        console.log("Form submit completed!");
    });
});
