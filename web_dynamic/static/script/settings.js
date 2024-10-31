document.addEventListener('DOMContentLoaded', function () {
    const sessionId = getSessionId();

    // Account Settings link
    const accountSettingsLink = document.getElementById('account-settings-link');
    const accountSettingsForm = document.getElementById('account-settings-form');
    const logoutLink = document.getElementById('logout-link');
    const logoutModal = document.getElementById('logout-modal');

    // Account Settings Elements
    const firstNameInput = document.getElementById('first-name');
    const surnameInput = document.getElementById('surname');
    const ageInput = document.getElementById('age');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const saveSettingsButton = document.getElementById('save-settings');

    // Logout Modal Elements
    const confirmLogoutButton = document.getElementById('confirm-logout');
    const cancelLogoutButton = document.getElementById('cancel-logout');

    // Show Account Settings Form and Fetch User Data
    accountSettingsLink.onclick = async function () {
        accountSettingsForm.style.display = accountSettingsForm.style.display === 'none' ? 'block' : 'none';
        if (accountSettingsForm.style.display === 'block') {
            try {
                const response = await fetch(`http://itohan.tech/api/v1/accountInfo/${sessionId}`);
                const data = await response.json();

                if (data.error) {
                    alert(data.error);
                    return;
                }

                firstNameInput.value = data.firstName;
                surnameInput.value = data.lastName;
                ageInput.value = data.age;
                emailInput.value = data.email;
                passwordInput.value = '';
            } catch (error) {
                console.error("Error fetching account information:", error);
            }
        }
    };

    // Save Updated Account Information
    saveSettingsButton.onclick = async function () {
        const updatedData = {
            firstName: firstNameInput.value,
            lastName: surnameInput.value,
            age: ageInput.value,
	    email: emailInput.value,
	    password: passwordInput.value
        };

        try {
            const response = await fetch(`http://itohan.tech/api/v1/updateAccount/${sessionId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updatedData)
            });
            const result = await response.json();

            if (result.error) {
                alert("Could not update account: " + result.error);
            } else {
                alert(result.message || "Account updated successfully");
                accountSettingsForm.style.display = 'none';
            }
        } catch (error) {
            console.error("Error updating account information:", error);
        }
    };

    // Show Logout Confirmation Modal
    logoutLink.onclick = function () {
        logoutModal.style.display = 'block';
    };

    // Cancel Logout
    cancelLogoutButton.onclick = function () {
        logoutModal.style.display = 'none';
    };

    // Confirm Logout
    confirmLogoutButton.onclick = async function () {
        try {
            const response = await fetch(`http://itohan.tech/api/v1/logout/${sessionId}`, { method: 'DELETE' });
            const result = await response.json();

            if (result.error) {
                alert("Logout failed: " + result.error);
            } else {
                alert(result.message || "Logged out successfully");
                window.location.href = "signup"; // Redirect to login page after logout
            }
        } catch (error) {
            console.error("Error during logout:", error);
        }
    };

    // function to get the session ID from cookies
    function getSessionId() {
        const name = 'session_id=';
        const decodedCookie = decodeURIComponent(document.cookie);
        const cookieArray = decodedCookie.split(';');
        for (let cookie of cookieArray) {
            while (cookie.charAt(0) === ' ') {
                cookie = cookie.substring(1);
            }
            if (cookie.indexOf(name) === 0) {
                return cookie.substring(name.length, cookie.length);
            }
        }
        return '';
    }
});
