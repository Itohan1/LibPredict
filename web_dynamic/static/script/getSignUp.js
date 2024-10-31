document.addEventListener("DOMContentLoaded", () => {
    const signUpForm = document.getElementById("signup-form");
    const loginButton = document.getElementById("login");
    const signInBlock = document.getElementById("signin-block");
    const signInSubmit = document.getElementById("signin-submit");

    // Sign-Up Form Submission
    signUpForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        
        const firstName = document.getElementById('first-name').value;
        const lastName = document.getElementById('last-name').value;
        const age = document.getElementById('age').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('http://itohan.tech/api/v1/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "firstName": firstName,
                    "lastName": lastName,
                    "age": age,
                    "email": email,
                    "password": password
                }),
		credentials: 'include'
            });

            if (response.ok) {
		const user = await response.json();
                document.cookie = `session_id=${user.session_id}; max-age=86400`;
                await showAlert("User signed up successfully!");
                window.location.href = "mainapp"; // Redirect to main app after signup
            } else {
                const result = await response.json();
                if (result.error.includes("already exists")) {
                    validatePassword(email, password);
                } else {
                    await showAlert("Sign-up failed");
                }
            }
        } catch (error) {
            console.error('Error:', error);
            await showAlert("An error occurred while signing up");
        }
    });

    // Login Button Click
    loginButton.addEventListener("click", async function () {
        try {
            const sessionId = getCookie('session_id');
            if (sessionId) {
                // Check if session ID is valid
                const response = await fetch(`http://itohan.tech/api/v1/session/${sessionId}`, { method: 'GET' });
                if (response.ok) {
                    const user = await response.json();
                    await showAlert(`Welcome back, ${user.firstName}`);
                    window.location.href = "mainapp";
                } else {
                    throw new Error("Session expired");
                }
            } else {
	      signInBlock.classList.remove("hidden");
            }
        } catch (error) {
            console.log(error.message);
            signInBlock.classList.remove("hidden"); // Show the sign-in block if session expired or not found
        }
    });

    // Sign-In Form Submission
    signInSubmit.addEventListener("click", async function () {
        const email = document.getElementById("signin-email").value;
        const password = document.getElementById("signin-password").value;

        try {
            const response = await fetch('http://itohan.tech/api/v1/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password }),
            });

            if (response.ok) {
                const user = await response.json();
		document.cookie = `session_id=${user.session_id}; max-age=86400`;
		console.log(document.cookie);
                await showAlert(`Welcome, ${user.firstName}`);
                window.location.href = "mainapp"; // Redirect to main app after login
            } else {
		const result = await response.json();
                await showAlert(`Invalid credentials. Please try again: result.error`);
            }
        } catch (error) {
            console.error('Error:', error);
            await showAlert("An error occurred while signing in");
        }
    });

    function getCookie(name) {
        const cookieArr = document.cookie.split(";").map(cookie => cookie.trim());
        for (const cookie of cookieArr) {
            if (cookie.startsWith(`${name}=`)) {
                return cookie.split("=")[1];
            }
        }
        return null;
    }

    async function validatePassword(email, password) {
        try {
            const response = await fetch('http://itohan.tech/api/v1/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            if (response.ok) {
                const user = await response.json();
                await showAlert(`Welcome, ${user.firstName}`);
                window.location.href = "mainapp";
            } else {
                await showAlert("Invalid password.");
            }
        } catch (error) {
            console.error("Error validating password:", error);
            await showAlert("An error occurred.");
        }
    }

   let alertInProgress = false;
   async function showAlert(message) {
      try {
        const alertContainer = document.getElementById('alert-container');
        const alertMessage = document.getElementById('alert-message');

        if (!alertContainer || !alertMessage) {
            console.error("Alert elements are missing from the DOM.");
            return;
        }

        if (alertInProgress) {
            console.log("Waiting for current alert to finish");
            return; // Exit if another alert is already in progress
        }

        alertInProgress = true;
        alertMessage.textContent = message;
        alertContainer.style.display = 'block';

        setTimeout(() => {
            alertContainer.style.display = 'none';
            alertInProgress = false;
        }, 3000); // Time for the alert to stay visible
      } catch (error) {
        console.error("Couldn't display alert:", error);
        alertInProgress = false; // Reset on error
      }
   }
});
