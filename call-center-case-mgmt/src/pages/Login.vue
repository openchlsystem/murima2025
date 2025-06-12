<template>
  <div class="login-container">
    <div class="login-card">
      <!-- Left Flag Strip -->
      <div class="flag-strip left-flag"></div>

      <!-- Left Section - Welcome with Pattern -->
      <div class="welcome-section">
        <!-- Seamless Photo -->
        <img src="/src/assets/images/welcome-helpline.png" alt="Welcome to MURIMA" class="welcome-photo">

        <div class="welcome-content">
          <h1 class="welcome-title">Welcome to <span>MURIMA</span></h1>
          <p class="welcome-description">
            Streamlining client communications and case management for efficient service delivery.
          </p>
        </div>
        <!-- Pattern Background -->
        <div class="pattern-background"></div>
      </div>

      <!-- Right Section - Login Form -->
      <div class="form-section">
        <!-- Logo Container -->
        <div class="logo-container">
          <img src="/Openchs logo-1.png" alt="OpenCHS Logo" class="logo">
        </div>

        <!-- Dynamic Form Title -->
        <h2 class="form-title">
          <span v-if="currentStep === 'email'">Log in to your account</span>
          <span v-else-if="currentStep === 'otp'">Enter verification code</span>
        </h2>

        <!-- Step Indicator -->
        <div class="step-indicator">
          <div class="step" :class="{ active: currentStep === 'email', completed: currentStep === 'otp' }">
            <span class="step-number">1</span>
            <span class="step-label">Email</span>
          </div>
          <div class="step-divider"></div>
          <div class="step" :class="{ active: currentStep === 'otp' }">
            <span class="step-number">2</span>
            <span class="step-label">Verify</span>
          </div>
        </div>

        <form @submit.prevent="handleSubmit" class="login-form">
          <!-- Error Message -->
          <div v-if="error" class="error-message">
            {{ error }}
          </div>

          <!-- Success Message -->
          <div v-if="successMessage" class="success-message">
            {{ successMessage }}
          </div>

          <!-- Step 1: Email and Login Method Selection -->
          <div v-if="currentStep === 'email'" class="step-content">
            <div class="input-group">
              <label class="input-label">Email Address</label>
              <input type="email" v-model="email" class="form-input"
                :class="{ 'input-error': submitted && !email }" placeholder="Enter your email address" required
                :disabled="loading">
              <div v-if="submitted && !email" class="validation-error">
                Email is required
              </div>
            </div>

            <!-- Login Method Selection -->
            <div class="input-group">
              <label class="input-label">How would you like to log in?</label>
              <div class="login-method-container">
                <div class="method-option" 
                     :class="{ active: loginMethod === 'password' }"
                     @click="selectLoginMethod('password')">
                  <div class="method-icon">🔐</div>
                  <div class="method-info">
                    <div class="method-title">Password</div>
                    <div class="method-desc">Use your password</div>
                  </div>
                </div>
                <div class="method-option" 
                     :class="{ active: loginMethod === 'otp' }"
                     @click="selectLoginMethod('otp')">
                  <div class="method-icon">📧</div>
                  <div class="method-info">
                    <div class="method-title">OTP</div>
                    <div class="method-desc">Get verification code</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Password Input (if password method selected) -->
            <div v-if="loginMethod === 'password'" class="input-group">
              <label class="input-label">Password</label>
              <input type="password" v-model="password" class="form-input"
                :class="{ 'input-error': submitted && loginMethod === 'password' && !password }" 
                placeholder="Enter your password" 
                :disabled="loading">
              <div v-if="submitted && loginMethod === 'password' && !password" class="validation-error">
                Password is required
              </div>
            </div>

            <!-- OTP Delivery Method (if OTP method selected) -->
            <div v-if="loginMethod === 'otp'" class="input-group">
              <label class="input-label">How to receive OTP</label>
              <div class="select-container">
                <select v-model="deliveryMethod" class="form-select"
                  :class="{ 'input-error': submitted && loginMethod === 'otp' && !deliveryMethod }" 
                  :disabled="loading">
                  <option value="email">📧 Email</option>
                  <option value="sms">📱 SMS</option>
                  <option value="whatsapp">💬 WhatsApp</option>
                </select>
                <div class="select-arrow">
                  <svg xmlns="http://www.w3.org/2000/svg" class="arrow-icon" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="6,9 12,15 18,9"></polyline>
                  </svg>
                </div>
              </div>
              <div v-if="submitted && loginMethod === 'otp' && !deliveryMethod" class="validation-error">
                Please select a delivery method
              </div>

              <!-- Delivery Method Description -->
              <div v-if="deliveryMethod" class="means-description">
                <p v-if="deliveryMethod === 'email'" class="means-text">
                  📧 OTP will be sent to your email address
                </p>
                <p v-else-if="deliveryMethod === 'sms'" class="means-text">
                  📱 OTP will be sent via SMS to your registered phone number
                </p>
                <p v-else-if="deliveryMethod === 'whatsapp'" class="means-text">
                  💬 OTP will be sent via WhatsApp to your registered number
                </p>
              </div>
            </div>

            <!-- Remember Me Checkbox -->
            <div class="remember-me">
              <label class="checkbox-container">
                <input type="checkbox" v-model="rememberMe" :disabled="loading">
                <span class="checkmark"></span>
                Remember me
              </label>
            </div>
          </div>

          <!-- Step 2: OTP Input -->
          <div v-if="currentStep === 'otp'" class="step-content">
            <div class="otp-info">
              <div class="selected-means-display">
                <div class="means-icon">
                  <span v-if="deliveryMethod === 'sms'">📱</span>
                  <span v-else-if="deliveryMethod === 'email'">📧</span>
                  <span v-else-if="deliveryMethod === 'whatsapp'">💬</span>
                </div>
                <p class="otp-message">
                  We've sent a 6-digit verification code to your 
                  <span v-if="deliveryMethod === 'email'">email address <strong>{{ maskedEmail }}</strong></span>
                  <span v-else-if="deliveryMethod === 'sms'">phone number ending with <strong>***{{ maskedPhone }}</strong></span>
                  <span v-else-if="deliveryMethod === 'whatsapp'">WhatsApp number ending with <strong>***{{ maskedPhone }}</strong></span>
                </p>
              </div>
            </div>

            <div class="input-group">
              <label class="input-label">Enter 6-digit OTP</label>
              <div class="otp-input-container">
                <input v-for="(digit, index) in otpDigits" :key="index" type="text" maxlength="1"
                  v-model="otpDigits[index]" @input="handleOtpInput(index, $event)"
                  @keydown="handleOtpKeydown(index, $event)" :ref="el => otpInputs[index] = el" class="otp-input"
                  :class="{ 'input-error': submitted && !isOtpComplete }" :disabled="loading">
              </div>
              <div v-if="submitted && !isOtpComplete" class="validation-error">
                Please enter the complete 6-digit OTP
              </div>
            </div>

            <!-- Resend OTP -->
            <div class="resend-container">
              <span v-if="resendTimer > 0" class="resend-timer">
                Resend OTP in {{ resendTimer }}s
              </span>
              <button v-else type="button" class="resend-button" @click="resendOtp" :disabled="loading">
                <span v-if="deliveryMethod === 'sms'">📱 Resend SMS</span>
                <span v-else-if="deliveryMethod === 'email'">📧 Resend Email</span>
                <span v-else-if="deliveryMethod === 'whatsapp'">💬 Resend WhatsApp</span>
              </button>
            </div>

            <!-- Back to Email -->
            <button type="button" class="back-button" @click="goBackToEmail" :disabled="loading">
              ← Back to Email
            </button>
          </div>

          <!-- Submit Button -->
          <button type="submit" class="login-button" :disabled="loading || !isFormValid">
            <span v-if="!loading">
              <span v-if="currentStep === 'email' && loginMethod === 'password'">Login</span>
              <span v-else-if="currentStep === 'email' && loginMethod === 'otp'">Send OTP</span>
              <span v-else-if="currentStep === 'otp'">Verify & Login</span>
            </span>
            <span v-else class="loading-content">
              <div class="spinner"></div>
              <span v-if="currentStep === 'email' && loginMethod === 'password'">Logging in...</span>
              <span v-else-if="currentStep === 'email' && loginMethod === 'otp'">Sending OTP...</span>
              <span v-else-if="currentStep === 'otp'">Verifying...</span>
            </span>
          </button>
        </form>

        <!-- Forgot Password Link -->
        <div class="forgot-password">
          <a href="#" class="forgot-link" @click.prevent="handleForgotPassword">Forgot your password?</a>
        </div>

        <!-- Help Text -->
        <div class="help-text">
          Need help? <a href="#" class="help-link" @click.prevent="handleHelp">Contact Support</a>
        </div>
      </div>

      <!-- Right Flag Strip -->
      <div class="flag-strip right-flag"></div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axiosInstance from '../utils/axios';

export default {
  setup() {
    const router = useRouter();
    const route = useRoute();

    // Form data
    const email = ref('');
    const password = ref('');
    const loginMethod = ref('otp'); // 'password' or 'otp'
    const deliveryMethod = ref('email'); // 'email', 'sms', 'whatsapp'
    const rememberMe = ref(false);
    const otpDigits = ref(['', '', '', '', '', '']);
    const otpInputs = ref([]);

    // Form state
    const currentStep = ref('email');
    const loading = ref(false);
    const submitted = ref(false);
    const error = ref('');
    const successMessage = ref('');
    const returnUrl = ref(route.query.returnUrl || '/dashboard');
    const resendTimer = ref(0);
    const resendInterval = ref(null);
    const userId = ref('');
    const maskedEmail = ref('');
    const maskedPhone = ref('');

    // SIP Details 
    const sipConnectionDetails = ref({
      uri: 'sip:6001@54.238.49.155',
      password: 'securepassword',
      websocketURL: 'wss://54.238.49.155:8089/ws'
    });

      // sipDetails 
      const sipConnectionDetails = ref({
        uri: 'sip:1001@18.177.175.202',
        password: '1001pass',
        websocketURL: 'ws://18.177.175.202:8088/websocket'
      })

    const isFormValid = computed(() => {
      if (currentStep.value === 'email') {
        if (loginMethod.value === 'password') {
          return email.value.length > 0 && password.value.length > 0;
        } else if (loginMethod.value === 'otp') {
          return email.value.length > 0 && deliveryMethod.value !== '';
        }
      } else if (currentStep.value === 'otp') {
        return isOtpComplete.value;
      }
      return false;
    });

    // Methods
    const selectLoginMethod = (method) => {
      loginMethod.value = method;
      error.value = '';
    };

    const handleOtpInput = (index, event) => {
      const value = event.target.value;
      if (value && index < 5) {
        otpInputs.value[index + 1]?.focus();
      }
    };

    const handleOtpKeydown = (index, event) => {
      if (event.key === 'Backspace' && !otpDigits.value[index] && index > 0) {
        otpInputs.value[index - 1]?.focus();
      }
    };

    const startResendTimer = () => {
      resendTimer.value = 30;
      resendInterval.value = setInterval(() => {
        resendTimer.value--;
        if (resendTimer.value <= 0) {
          clearInterval(resendInterval.value);
        }
      }, 1000);
    };

    const maskEmail = (email) => {
      const [username, domain] = email.split('@');
      const maskedUsername = username.length > 2 
        ? username.substring(0, 2) + '*'.repeat(username.length - 2)
        : username;
      return `${maskedUsername}@${domain}`;
    };

    const passwordLogin = async () => {
      loading.value = true;
      error.value = '';

      try {
        const response = await axiosInstance.post('/auth/login/', {
          email: email.value,
          password: password.value,
          login_method: 'password',
          remember_me: rememberMe.value
        });

        // Store authentication tokens and user data
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
        localStorage.setItem('session_id', response.data.session_id);

        // Store SIP information
        localStorage.setItem('sipConnectionDetails', JSON.stringify({
          desc: 'SIP Connection Details',
          uri: sipConnectionDetails.value.uri,
          password: sipConnectionDetails.value.password,
          websocketURL: sipConnectionDetails.value.websocketURL
        }));

        // Store remember me preference
        if (rememberMe.value) {
          localStorage.setItem('rememberedEmail', email.value);
          localStorage.setItem('rememberedMethod', loginMethod.value);
        } else {
          localStorage.removeItem('rememberedEmail');
          localStorage.removeItem('rememberedMethod');
        }

        // Redirect to dashboard
        router.push(returnUrl.value);
      } catch (err) {
        error.value = err.response?.data?.detail ||
          err.response?.data?.message ||
          err.response?.data?.non_field_errors?.[0] ||
          'Login failed. Please check your credentials.';
        console.error('Password login error:', err);
      } finally {
        loading.value = false;
      }
    };

    const requestOtp = async () => {
      loading.value = true;
      error.value = '';

      try {
        const response = await axiosInstance.post('/auth/login/', {
          email: email.value,
          login_method: 'otp',
          delivery_method: deliveryMethod.value,
          remember_me: rememberMe.value
        });

        if (response.data.requires_otp) {
          userId.value = response.data.user_id;
          maskedEmail.value = maskEmail(email.value);
          
          currentStep.value = 'otp';
          successMessage.value = `OTP sent successfully via ${deliveryMethod.value}!`;
          startResendTimer();

          setTimeout(() => {
            successMessage.value = '';
          }, 3000);
        } else {
          // This shouldn't happen with OTP method, but handle just in case
          error.value = 'Unexpected response from server.';
        }
      } catch (err) {
        error.value = err.response?.data?.detail ||
          err.response?.data?.message ||
          err.response?.data?.error ||
          'Failed to send OTP. Please try again.';
        console.error('OTP request error:', err);
      } finally {
        loading.value = false;
      }
    };

    const verifyOtp = async () => {
      loading.value = true;
      error.value = '';

      try {
        const otpCode = otpDigits.value.join('');
        const response = await axiosInstance.post('/auth/verify-login-otp/', {
          user_id: userId.value,
          token: otpCode,
          remember_me: rememberMe.value
        });

        // Store authentication tokens and user data
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
        localStorage.setItem('session_id', response.data.session_id);

        // Store SIP information
        localStorage.setItem('sipConnectionDetails', JSON.stringify({
          desc: 'SIP Connection Details',
          uri: sipConnectionDetails.value.uri,
          password: sipConnectionDetails.value.password,
          websocketURL: sipConnectionDetails.value.websocketURL
        }));

        // Store remember me preference
        if (rememberMe.value) {
          localStorage.setItem('rememberedEmail', email.value);
          localStorage.setItem('rememberedMethod', loginMethod.value);
        } else {
          localStorage.removeItem('rememberedEmail');
          localStorage.removeItem('rememberedMethod');
        }

        // Redirect to dashboard
        router.push(returnUrl.value);
      } catch (err) {
        error.value = err.response?.data?.detail ||
          err.response?.data?.message ||
          err.response?.data?.error ||
          'OTP verification failed. Please try again.';
        console.error('OTP verification error:', err);
      } finally {
        loading.value = false;
      }
    };

    const handleSubmit = async () => {
      submitted.value = true;

      if (!isFormValid.value) {
        return;
      }

      if (currentStep.value === 'email') {
        if (loginMethod.value === 'password') {
          await passwordLogin();
        } else if (loginMethod.value === 'otp') {
          await requestOtp();
        }
      } else if (currentStep.value === 'otp') {
        await verifyOtp();
      }
    };

    const resendOtp = async () => {
      loading.value = true;
      error.value = '';

      try {
        await axiosInstance.post('/auth/request-otp/', {
          email: email.value,
          purpose: 'login',
          delivery_method: deliveryMethod.value
        });

        successMessage.value = `OTP resent successfully via ${deliveryMethod.value}!`;
        startResendTimer();

        setTimeout(() => {
          successMessage.value = '';
        }, 3000);
      } catch (err) {
        error.value = err.response?.data?.detail ||
          err.response?.data?.message ||
          'Failed to resend OTP. Please try again.';
      } finally {
        loading.value = false;
      }
    };

    const goBackToEmail = () => {
      currentStep.value = 'email';
      otpDigits.value = ['', '', '', '', '', ''];
      submitted.value = false;
      error.value = '';
      successMessage.value = '';
      userId.value = '';

      if (resendInterval.value) {
        clearInterval(resendInterval.value);
        resendTimer.value = 0;
      }
    };

    const handleForgotPassword = () => {
      // TODO: Implement forgot password logic
      router.push('/forgot-password');
    };

    const handleHelp = () => {
      console.log('Help clicked');
      // TODO: Implement help logic
    };

    // Check for remembered data on component mount
    const checkRememberedData = () => {
      const rememberedEmail = localStorage.getItem('rememberedEmail');
      const rememberedMethod = localStorage.getItem('rememberedMethod');

      if (rememberedEmail) {
        email.value = rememberedEmail;
        rememberMe.value = true;
      }

      if (rememberedMethod) {
        loginMethod.value = rememberedMethod;
      }
    };

        const checkWSConnection = new WebSocket("ws://18.177.175.202:8088/ws", "sip");

    onUnmounted(() => {
      if (resendInterval.value) {
        clearInterval(resendInterval.value);
      }
    });

    return {
      email,
      password,
      loginMethod,
      deliveryMethod,
      rememberMe,
      otpDigits,
      otpInputs,
      currentStep,
      loading,
      submitted,
      error,
      successMessage,
      maskedEmail,
      maskedPhone,
      resendTimer,
      isOtpComplete,
      isFormValid,
      selectLoginMethod,
      handleOtpInput,
      handleOtpKeydown,
      handleSubmit,
      resendOtp,
      goBackToEmail,
      handleForgotPassword,
      handleHelp,
      sipConnectionDetails,
    };
  }
};
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    font-weight: 700;
  }

  body {
    background-color: #f7fafc;
  }

  .login-method-container {
  display: flex;
  gap: 12px;
  margin-bottom: 1rem;
}

.method-option {
  flex: 1;
  padding: 12px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: white;
}

.method-option:hover {
  border-color: #1e7e34;
  background-color: rgba(30, 126, 52, 0.05);
}

.method-option.active {
  border-color: #1e7e34;
  background-color: rgba(30, 126, 52, 0.1);
  box-shadow: 0 0 0 3px rgba(30, 126, 52, 0.1);
}

.method-icon {
  font-size: 1.5rem;
}

.method-info {
  flex: 1;
}

.method-title {
  font-size: 14px;
  font-weight: 700;
  color: #000000;
  margin-bottom: 2px;
}

.method-desc {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
}

.forgot-password {
  text-align: center;
  margin-bottom: 1rem;
}

.forgot-link {
  color: #1e7e34;
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
}

.forgot-link:hover {
  text-decoration: underline;
}

  .login-container {
    min-height: 100vh;
    background-color: #ffffff;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
    position: relative;
  }

  .login-card {
    display: flex;
    width: 930px;
    max-width: 95%;
    min-height: 550px;
    background-color: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    position: relative;
  }

  /* Kenyan Flag Strips */
  .flag-strip {
    width: 20px;
    min-width: 20px;
    background: linear-gradient(to bottom,
        #000000 0%,
        #000000 33.33%,
        #bc0103 33.33%,
        #bc0103 66.66%,
        #006817 66.66%,
        #006817 100%);
    flex-shrink: 0;
    height: 100%;
  }

  .left-flag {
    border-top-left-radius: 20px;
    border-bottom-left-radius: 20px;
  }

  .right-flag {
    border-top-right-radius: 20px;
    border-bottom-right-radius: 20px;
  }

  /* Left Section - Welcome */
  .welcome-section {
    flex: 1;
    background-color: #f8f9fa;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    padding: 2rem;
  }

  .welcome-photo {
    width: 160px;
    height: 160px;
    object-fit: contain;
    margin-bottom: 1.5rem;
    z-index: 5;
  }

  .welcome-content {
    position: relative;
    z-index: 2;
    text-align: center;
    padding: 1rem;
  }

  .welcome-title {
    font-size: 2.5rem;
    color: #000000;
    margin-bottom: 1.5rem;
    font-weight: 900;
    line-height: 1.2;
  }

  .welcome-title span {
    display: block;
    font-size: 3rem;
    color: #1e7e34;
  }

  .welcome-description {
    font-size: 1rem;
    line-height: 1.6;
    color: #4a5568;
    max-width: 320px;
    margin: 0 auto;
  }

  .pattern-background {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    opacity: 0.1;
    background:
      linear-gradient(45deg, #000000 25%, transparent 25%, transparent 75%, #000000 75%, #000000),
      linear-gradient(45deg, #000000 25%, transparent 25%, transparent 75%, #000000 75%, #000000),
      linear-gradient(45deg, #bc0103 25%, transparent 25%, transparent 75%, #bc0103 75%, #bc0103),
      linear-gradient(45deg, #006817 25%, transparent 25%, transparent 75%, #006817 75%, #006817);
    background-size: 60px 60px;
    background-position: 0 0, 30px 30px, 15px 15px, 45px 45px;
    z-index: 1;
  }

  /* Right Section - Form */
  .form-section {
    flex: 1;
    padding: 3rem 2rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
    background-color: white;
  }

  .logo-container {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    border: 2px solid #e2e8f0;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0 auto 1.5rem;
    background-color: white;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .logo {
    width: 40px;
    height: 40px;
    object-fit: contain;
  }

  .form-title {
    font-size: 1.5rem;
    color: #000000;
    text-align: center;
    margin-bottom: 1rem;
    font-weight: 800;
  }

  /* Step Indicator */
  .step-indicator {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 2rem;
    gap: 1rem;
  }

  .step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }

  .step-number {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 700;
    background-color: #e2e8f0;
    color: #64748b;
    transition: all 0.3s ease;
  }

  .step.active .step-number {
    background-color: #1e7e34;
    color: white;
  }

  .step.completed .step-number {
    background-color: #006817;
    color: white;
  }

  .step-label {
    font-size: 12px;
    color: #64748b;
    font-weight: 600;
  }

  .step.active .step-label,
  .step.completed .step-label {
    color: #000000;
  }

  .step-divider {
    width: 40px;
    height: 2px;
    background-color: #e2e8f0;
    margin-top: -16px;
  }

  .login-form {
    width: 100%;
    max-width: 320px;
    margin: 0 auto;
  }

  .step-content {
    animation: slideIn 0.3s ease-out;
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateX(20px);
    }

    to {
      opacity: 1;
      transform: translateX(0);
    }
  }

  .error-message {
    background-color: rgba(229, 62, 62, 0.1);
    border: 1px solid #e53e3e;
    color: #e53e3e;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    font-size: 14px;
    text-align: center;
  }

  .success-message {
    background-color: rgba(34, 197, 94, 0.1);
    border: 1px solid #22c55e;
    color: #16a34a;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    font-size: 14px;
    text-align: center;
  }

  .input-group {
    margin-bottom: 1.5rem;
    position: relative;
  }

  .input-label {
    display: block;
    font-size: 14px;
    color: #000000;
    margin-bottom: 0.5rem;
    font-weight: 700;
  }

  .form-input {
    width: 100%;
    padding: 12px 16px;
    border: 3px dotted #2d3748;
    border-radius: 10px;
    font-size: 14px;
    color: #000000;
    background-color: white;
    transition: all 0.3s ease;
    font-weight: 600;
  }

  .form-input::placeholder {
    color: #a0aec0;
    font-weight: 500;
  }

  .form-input:focus {
    border-color: #1e7e34;
    border-style: dotted;
    box-shadow: 0 0 0 3px rgba(30, 126, 52, 0.1);
    outline: none;
  }

  .form-input:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  /* Select Dropdown Styles */
  .select-container {
    position: relative;
  }

  .form-select {
    width: 100%;
    padding: 12px 40px 12px 16px;
    border: 3px dotted #2d3748;
    border-radius: 10px;
    font-size: 14px;
    color: #000000;
    background-color: white;
    transition: all 0.3s ease;
    font-weight: 600;
    appearance: none;
    cursor: pointer;
  }

  .form-select:focus {
    border-color: #1e7e34;
    border-style: dotted;
    box-shadow: 0 0 0 3px rgba(30, 126, 52, 0.1);
    outline: none;
  }

  .form-select:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .form-select option {
    padding: 8px;
    font-weight: 600;
  }

  .select-arrow {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    pointer-events: none;
    color: #718096;
  }

  .arrow-icon {
    width: 1.25rem;
    height: 1.25rem;
  }

  .input-error {
    border-color: #e53e3e !important;
    border-style: dotted !important;
  }

  .validation-error {
    color: #e53e3e;
    font-size: 12px;
    margin-top: 0.5rem;
  }

  /* Means Description */
  .means-description {
    margin-top: 0.75rem;
    padding: 8px 12px;
    background-color: rgba(30, 126, 52, 0.05);
    border-radius: 6px;
    border-left: 3px solid #1e7e34;
  }

  .means-text {
    font-size: 12px;
    color: #1e7e34;
    font-weight: 600;
    margin: 0;
  }

  .remember-me {
    display: flex;
    align-items: center;
    margin-bottom: 1.5rem;
  }

  .checkbox-container {
    display: flex;
    align-items: center;
    cursor: pointer;
    font-size: 14px;
    color: #000000;
    user-select: none;
  }

  .checkbox-container input {
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
  }

  .checkmark {
    position: relative;
    display: inline-block;
    height: 18px;
    width: 18px;
    background-color: white;
    border: 2px solid #cbd5e0;
    border-radius: 4px;
    margin-right: 10px;
  }

  .checkbox-container:hover input~.checkmark {
    border-color: #1e7e34;
  }

  .checkbox-container input:checked~.checkmark {
    background-color: #1e7e34;
    border-color: #1e7e34;
  }

  .checkmark:after {
    content: "";
    position: absolute;
    display: none;
  }

  .checkbox-container input:checked~.checkmark:after {
    display: block;
  }

  .checkbox-container .checkmark:after {
    left: 5px;
    top: 1px;
    width: 5px;
    height: 10px;
    border: solid white;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg);
  }

  /* OTP Specific Styles */
  .otp-info {
    margin-bottom: 1.5rem;
  }

  .selected-means-display {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem;
    background-color: #f8f9fa;
    border-radius: 10px;
    border: 2px solid #e2e8f0;
  }

  .means-icon {
    font-size: 2rem;
  }

  .otp-message {
    font-size: 14px;
    color: #4a5568;
    text-align: center;
    line-height: 1.5;
    margin: 0;
  }

  .otp-input-container {
    display: flex;
    gap: 8px;
    justify-content: center;
  }

  .otp-input {
    width: 45px;
    height: 45px;
    text-align: center;
    border: 3px dotted #2d3748;
    border-radius: 8px;
    font-size: 18px;
    font-weight: 700;
    color: #000000;
    background-color: white;
    transition: all 0.3s ease;
  }

  .otp-input:focus {
    border-color: #1e7e34;
    border-style: dotted;
    box-shadow: 0 0 0 3px rgba(30, 126, 52, 0.1);
    outline: none;
  }

  .otp-input:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .resend-container {
    text-align: center;
    margin-bottom: 1rem;
  }

  .resend-timer {
    font-size: 14px;
    color: #64748b;
  }

  .resend-button {
    background: none;
    border: none;
    color: #1e7e34;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    text-decoration: underline;
    padding: 4px 0;
  }

  .resend-button:hover {
    color: #167029;
  }

  .resend-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .back-button {
    background: none;
    border: none;
    color: #64748b;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    margin-bottom: 1rem;
    padding: 8px 0;
    width: 100%;
    text-align: center;
  }

  .back-button:hover {
    color: #000000;
  }

  .back-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .login-button {
    width: 100%;
    padding: 14px;
    background-color: #1e7e34;
    color: white;
    border: none;
    border-radius: 30px;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(30, 126, 52, 0.2);
  }

  .login-button:hover:not(:disabled) {
    background-color: #167029;
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(30, 126, 52, 0.3);
  }

  .login-button:active:not(:disabled) {
    background-color: #bc0103;
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(188, 1, 3, 0.3);
  }

  .login-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .loading-content {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  .spinner {
    width: 1rem;
    height: 1rem;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .help-text {
    font-size: 14px;
    color: #000000;
    text-align: center;
    font-weight: 600;
  }

  .help-link {
    color: #bc0103;
    text-decoration: none;
    font-weight: 700;
  }

  .help-link:hover {
    text-decoration: underline;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .login-card {
      flex-direction: column;
      max-width: 95%;
      width: auto;
    }

    .flag-strip {
      width: 15px;
      height: 15px;
    }

    .left-flag {
      border-radius: 20px 20px 0 0;
      background: linear-gradient(to right,
          #000000 0%,
          #000000 33.33%,
          #bc0103 33.33%,
          #bc0103 66.66%,
          #006817 66.66%,
          #006817 100%);
    }

    .right-flag {
      border-radius: 0 0 20px 20px;
      background: linear-gradient(to right,
          #000000 0%,
          #000000 33.33%,
          #bc0103 33.33%,
          #bc0103 66.66%,
          #006817 66.66%,
          #006817 100%);
    }

    .otp-input {
      width: 40px;
      height: 40px;
      font-size: 16px;
    }

    .otp-input-container {
      gap: 6px;
    }

    .means-icon {
      font-size: 1.5rem;
    }
  }

  @media (max-width: 480px) {
    .login-card {
      min-height: auto;
    }

    .flag-strip {
      width: 12px;
      height: 12px;
    }

    .otp-input {
      width: 35px;
      height: 35px;
      font-size: 14px;
    }

    .otp-input-container {
      gap: 4px;
    }
  }

  /* Animation */
  .login-card {
    animation: floatIn 0.6s ease-out;
  }

  @keyframes floatIn {
    from {
      opacity: 0;
      transform: translateY(30px);
    }

    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>