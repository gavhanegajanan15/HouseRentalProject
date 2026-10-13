document.addEventListener("DOMContentLoaded", function () {
    const sendBtn = document.getElementById("send-otp-btn");
    const verifyBtn = document.getElementById("verify-otp-btn");
    const otpSection = document.getElementById("otp-section");
    const otpInput = document.getElementById("otp-code");
    const registerBtn = document.getElementById("register-btn");
    const emailInput = document.getElementById("id_email");

    if (!sendBtn || !emailInput) return;

    sendBtn.addEventListener("click", async function () {
        const email = emailInput.value.trim();
        const csrf = document.querySelector(
            '[name="csrfmiddlewaretoken"]'
        )?.value;

        if (!email) {
            alert("Please enter your email address.");
            return;
        }

        sendBtn.disabled = true;

        try {
            const response = await fetch("/send-email-otp/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": csrf
                },
                body: new URLSearchParams({
                    email: email,
                    csrfmiddlewaretoken: csrf
                })
            });

            const data = await response.json();

            if (data.success) {
                otpSection.style.display = "block";
                alert("OTP sent successfully. Check your email.");
            } else {
                alert(data.message || "OTP could not be sent.");
            }
        } catch (error) {
            console.error(error);
            alert("Request failed. Check the Django terminal.");
        } finally {
            sendBtn.disabled = false;
        }
    });

    if (verifyBtn) {
        verifyBtn.addEventListener("click", async function () {
            const csrf = document.querySelector(
                '[name="csrfmiddlewaretoken"]'
            )?.value;

            try {
                const response = await fetch("/verify-email-otp/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-CSRFToken": csrf
                    },
                    body: new URLSearchParams({
                        otp: otpInput.value.trim(),
                        csrfmiddlewaretoken: csrf
                    })
                });

                const data = await response.json();

                if (data.success) {
                    alert("Email verified successfully!");
                    if (registerBtn) registerBtn.disabled = false;
                    otpInput.disabled = true;
                    verifyBtn.disabled = true;
                } else {
                    alert(data.message || "Invalid OTP.");
                }
            } catch (error) {
                console.error(error);
                alert("OTP verification failed.");
            }
        });
    }
});