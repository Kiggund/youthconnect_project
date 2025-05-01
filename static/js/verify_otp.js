document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const resendBtn = document.getElementById('resend-otp-btn');
    const cooldownTimer = document.getElementById('cooldown-timer');
    const otpForm = document.getElementById('otp-form');
    const otpInput = document.getElementById('otp-input');
    const verifyBtn = otpForm.querySelector('button[type="submit"]');
    const lockoutTimer = document.createElement('div'); // For lockout countdown

    // State Management
    let cooldownInterval;
    let lockoutInterval;
    let failedAttempts = 0;
    const MAX_ATTEMPTS = 3;
    const LOCKOUT_DURATION = 300; // 5 minutes in seconds
    let remainingLockoutTime = LOCKOUT_DURATION;

    // Initialize
    initLockoutTimerUI();
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
                credentials: 'include'
            });

            if (response.redirected) {
                window.location.href = response.url;
                return;
            }

            const data = await response.json();
            if (data.valid) {
                handleSuccess(data.redirect_url);
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
                    'X-CSRFToken': window.OTP_CONFIG.csrfToken,
                    'Content-Type': 'application/json'
                },
                credentials: 'include'
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
    // LOCKOUT SYSTEM
    // ======================

    function handleFailedAttempt(errorMessage) {
        failedAttempts++;
        showToast(errorMessage || "Invalid OTP code", "error");
        
        if (failedAttempts >= MAX_ATTEMPTS) {
            startAccountLockout();
        }
    }

    function startAccountLockout() {
        // Disable all inputs
        otpInput.disabled = true;
        verifyBtn.disabled = true;
        resendBtn.disabled = true;
        
        // Show lockout message
        const lockoutMessage = `Account locked. Please wait ${formatTime(LOCKOUT_DURATION)}.`;
        showToast(lockoutMessage, "error", LOCKOUT_DURATION * 1000);
        
        // Start countdown
        remainingLockoutTime = LOCKOUT_DURATION;
        updateLockoutTimer();
        lockoutInterval = setInterval(updateLockoutTimer, 1000);
    }

    function updateLockoutTimer() {
        remainingLockoutTime--;
        
        // Update UI
        lockoutTimer.textContent = `Unlocks in: ${formatTime(remainingLockoutTime)}`;
        
        // Check if lockout expired
        if (remainingLockoutTime <= 0) {
            clearInterval(lockoutInterval);
            resetAccountLock();
        }
    }

    function resetAccountLock() {
        // Enable inputs
        otpInput.disabled = false;
        verifyBtn.disabled = false;
        
        // Reset state
        failedAttempts = 0;
        remainingLockoutTime = LOCKOUT_DURATION;
        
        // Update UI
        lockoutTimer.textContent = '';
        showToast("Account unlocked. You may try again.", "success");
        
        // Restart cooldown
        resetCooldown();
    }

    function initLockoutTimerUI() {
        lockoutTimer.className = 'lockout-timer';
        otpForm.appendChild(lockoutTimer);
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

    // ======================
    // UI HELPERS
    // ======================

    function formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    }

    function updateCooldownUI(seconds) {
        cooldownTimer.textContent = `(${seconds}s)`;
        resendBtn.disabled = true;
    }

    function enableResendButton() {
        resendBtn.disabled = false;
        cooldownTimer.textContent = '';
    }

    function setLoadingState(loading) {
        verifyBtn.disabled = loading;
        verifyBtn.innerHTML = loading 
            ? '<i class="fas fa-spinner fa-spin"></i> Verifying...' 
            : 'Verify';
    }

    function setResendLoadingState(loading) {
        resendBtn.disabled = loading;
        resendBtn.innerHTML = loading
            ? '<i class="fas fa-spinner fa-spin"></i> Sending...'
            : 'Resend OTP';
    }

    function showToast(message, type, duration = 5000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        document.getElementById('toast-container').appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('fade-out');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    function validateOtpFormat(otp) {
        return /^\d{6}$/.test(otp);
    }

    function handleSuccess(redirectUrl) {
        showToast("Verification successful!", "success");
        setTimeout(() => window.location.href = redirectUrl, 1500);
    }

    function handleError(message) {
        console.error(message);
        showToast(message, "error");
    }

    function resetFailedAttempts() {
        failedAttempts = 0;
    }
});
