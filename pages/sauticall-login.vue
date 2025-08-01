<template>
  <div class="login-outer-wrapper">
    <div class="login-container">
      <div class="side-panel left-panel">
        <div class="flag-strip left-flag">
          <div class="flag-segment black"></div>
          <div class="flag-segment yellow"></div>
          <div class="flag-segment red"></div>
          <div class="flag-segment yellow"></div>
          <div class="flag-segment black"></div>
        </div>
        <div class="pattern-bg pattern-bg-left"></div>
      </div>
      <div class="center-panel">
        <div class="form-section">
          <div class="coat-of-arms-container">
            <!-- Placeholder for Uganda Coat of Arms -->
            <img src="@/assets/images/uganda-coat-of-arms.png" alt="Uganda Coat of Arms" class="coat-of-arms" />
          </div>
          <h2 class="form-title">
            <span v-if="currentStep === 'email'">
              Welcome to <span class="openchs-uganda-flag">OPENCHS</span>
            </span>
            <span v-else-if="currentStep === 'otp'">Enter verification code</span>
            <span v-else-if="currentStep === 'password'">Enter your password</span>
          </h2>
          <!-- ... existing code ... -->
          <div class="partners-section partners-section-noframe">
            <div class="partners-label partners-label-colored">
              <span class="c-black">O</span><span class="c-yellow">u</span><span class="c-red">r</span>
              <span class="c-black"> </span>
              <span class="c-yellow">P</span><span class="c-red">a</span><span class="c-black">r</span><span class="c-yellow">t</span><span class="c-red">n</span><span class="c-black">e</span><span class="c-yellow">r</span><span class="c-red">s</span>
            </div>
            <div class="partners-logos-row">
              <!-- You may want to update these logos to Ugandan partners -->
              <img src="@/assets/images/welcome-helpline.png" alt="Uganda Helpline" class="partner-logo" />
              <img src="@/assets/images/MOH.png" alt="Ministry of Health" class="partner-logo" />
              <img src="@/assets/images/unicef.png" alt="UNICEF" class="partner-logo" />
              <img src="@/assets/images/GIZ.png" alt="GIZ" class="partner-logo" />
              <img src="@/assets/images/UNFPA.png" alt="UNFPA" class="partner-logo" />
            </div>
          </div>
        </div>
      </div>
      <div class="side-panel right-panel">
        <div class="flag-strip right-flag-bar">
          <div class="flag-segment black"></div>
          <div class="flag-segment yellow"></div>
          <div class="flag-segment red"></div>
          <div class="flag-segment yellow"></div>
          <div class="flag-segment black"></div>
        </div>
        <div class="pattern-bg pattern-bg-right"></div>
      </div>
    </div>
  </div>
</template>

<script>
// ... existing code from Login.vue ...
</script>

<style>
@font-face {
  font-family: 'Lequire';
  src: url('@/assets/fonts/Lequire.otf') format('opentype');
  font-weight: normal;
  font-style: normal;
}
.openchs-lequire {
  font-family: 'Lequire', sans-serif !important;
  letter-spacing: 0.04em;
  font-weight: normal;
}
.openchs-uganda-flag {
  background: linear-gradient(
    to right,
    #000 0%, #000 33%,      /* Black */
    #ffe600 33%, #ffe600 66%, /* Yellow */
    #d90000 66%, #d90000 100% /* Red */
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
  font-family: 'Lequire', sans-serif !important;
  letter-spacing: 0.04em;
}
</style>

<style scoped>
/* ... existing code from Login.vue, but update flag-segment and partners-label colors ... */
.flag-segment.black {
  background: #000;
  height: 32%;
}
.flag-segment.yellow {
  background: #ffe600;
  height: 4%;
}
.flag-segment.red {
  background: #d90000;
  height: 28%;
}
.partners-label-colored .c-black { color: #222; }
.partners-label-colored .c-yellow { color: #ffe600; }
.partners-label-colored .c-red { color: #d90000; }
/* ... rest of the styles from Login.vue ... */
</style> 