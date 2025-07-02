document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const resendBtn = document.getElementById('resend-otp-btn');
    const cooldownTimer = document.getElementById('cooldown-timer');
    const otpForm = document.getElementById('otp-form');
    const otpInput = document.getElementById('otp-code');
    const verifyBtn = document.getElementById('verify-btn');
    const lockoutTimer = document.createElement('div');
    lockoutTimer.className = 'lockout-timer';

    // State Management
    let cooldownInterval;
    let lockoutInterval;
    let failedAttempts = 0;
    const MAX_ATTEMPTS = window.OTP_CONFIG?.maxAttempts || 3;
    const LOCKOUT_DURATION = 300; // 5 minutes in seconds
    let remainingLockoutTime = LOCKOUT_DURATION;

    // Initialize
    otpForm.appendChild(lockoutTimer);
    startCooldown();

    // Event Listeners
    otpForm.addEventListener('submit', handleSubmit);
    resendBtn.addEventListener('click', handleResendOtp);

    // ======================
    // MAIN FUNCTIONS
    // ======================

    async function handleSubmit(e) {
        e.preventDefault();

        if (!validateOtpFormat(otpInput.value)) {
            showToast("Please enter a valid 6-digit code", "error");
            return;
        }

        setLoadingState(true);

        try {
            const response = await fetch(otpForm.action, {
                method: 'POST',
                body: new FormData(otpForm),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRF-TOKEN': window.OTP_CONFIG.csrfToken
                },
                credentials: 'same-origin'
            });

            if (response.redirected) {
                window.location.href = response.url;
                return;
            }

            const data = await response.json();
            if (data.valid) {
                handleSuccess(data.redirect);
            } else {
                handleFailedAttempt(data.message);
            }
        } catch (error) {
            handleError("Verification failed. Please try again.");
        } finally {
            setLoadingState(false);
        }
    }

    async function handleResendOtp() {
        if (resendBtn.disabled) return;

        setResendLoadingState(true);

        try {
            const response = await fetch(window.OTP_CONFIG.resendUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': window.OTP_CONFIG.csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `email=${encodeURIComponent(window.OTP_CONFIG.email)}`,
                credentials: 'same-origin'
            });

            const data = await response.json();
            if (response.ok && data.status === 'success') {
                showToast("New OTP sent successfully!", "success");
                resetFailedAttempts();
                resetCooldown();
            } else {
                throw new Error(data.message || 'Failed to resend OTP');
            }
        } catch (error) {
            handleError(error.message);
        } finally {
            setResendLoadingState(false);
        }
    }

    // ======================
    // SECURITY FUNCTIONS
    // ======================

    function handleFailedAttempt(errorMessage) {
        failedAttempts++;
        showToast(errorMessage || "Invalid OTP code", "error");

        if (failedAttempts >= MAX_ATTEMPTS) {
            startAccountLockout();
        }
    }

    function startAccountLockout() {
        otpInput.disabled = true;
        verifyBtn.disabled = true;
        resendBtn.disabled = true;

        const lockoutMessage = `Account locked. Please wait ${formatTime(LOCKOUT_DURATION)}.`;
        showToast(lockoutMessage, "error", LOCKOUT_DURATION * 1000);

        remainingLockoutTime = LOCKOUT_DURATION;
        updateLockoutTimer();
        lockoutInterval = setInterval(updateLockoutTimer, 1000);
    }

    function updateLockoutTimer() {
        remainingLockoutTime--;
        lockoutTimer.textContent = `Unlocks in: ${formatTime(remainingLockoutTime)}`;

        if (remainingLockoutTime <= 0) {
            clearInterval(lockoutInterval);
            resetAccountLock();
        }
    }

    function resetAccountLock() {
        otpInput.disabled = false;
        verifyBtn.disabled = false;
        failedAttempts = 0;
        remainingLockoutTime = LOCKOUT_DURATION;
        lockoutTimer.textContent = '';
        showToast("Account unlocked. You may try again.", "success");
        resetCooldown();
    }

    // ======================
    // COOLDOWN SYSTEM
    // ======================

    function startCooldown() {
        let seconds = window.OTP_CONFIG?.cooldownDuration || 30;
        updateCooldownUI(seconds);

        cooldownInterval = setInterval(() => {
            seconds--;
            updateCooldownUI(seconds);

            if (seconds <= 0) {
                clearInterval(cooldownInterval);
                enableResendButton();
            }
        }, 1000);
    }

    function resetCooldown() {
        clearInterval(cooldownInterval);
        startCooldown();
    }

    function updateCooldownUI(seconds) {
        cooldownTimer.textContent = `(${seconds}s)`;
        resendBtn.disabled = true;
    }

    function enableResendButton() {
        resendBtn.disabled = false;
        cooldownTimer.textContent = '';
    }

    // ======================
    // UI HELPERS
    // ======================

    function setLoadingState(loading) {
        const btnText = verifyBtn.querySelector('.btn-text');
        const spinner = verifyBtn.querySelector('.spinner');
        
        verifyBtn.disabled = loading;
        btnText.classList.toggle('hidden', loading);
        spinner.classList.toggle('hidden', !loading);
    }

    function setResendLoadingState(loading) {
        resendBtn.disabled = loading;
        resendBtn.innerHTML = loading
            ? '<span class="spinner" aria-hidden="true"></span> Sending...'
            : 'Resend OTP';
    }

    function showToast(message, type, duration = 5000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.setAttribute('role', 'alert');

        document.getElementById('toast-container').appendChild(toast);

        setTimeout(() => {
            toast.classList.add('fade-out');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    function formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    }

    function validateOtpFormat(otp) {
        return /^\d{6}$/.test(otp);
    }

    function handleSuccess(redirectUrl) {
        showToast("Verification successful!", "success");
        setTimeout(() => window.location.href = redirectUrl, 1500);
    }

    function handleError(message) {
        console.error('OTP Error:', message);
        showToast(message, "error");
    }

    function resetFailedAttempts() {
        failedAttempts = 0;
    }
});
