<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { authStore } from '$lib/stores/auth';

  let email = '';
  let password = '';
  let confirmPassword = '';
  let error = '';
  let loading = false;
  let success = false;

  const eyeSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>
    <circle cx="12" cy="12" r="3"/>
  </svg>`;

  const eyeOffSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/>
    <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/>
    <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/>
    <line x1="2" x2="22" y1="2" y2="22"/>
  </svg>`;

  onMount(() => {
    // Wire up password toggles
    document.querySelectorAll('.toggle-password').forEach(btn => {
      btn.addEventListener('click', () => {
        const input = document.getElementById(btn.getAttribute('data-target') || '') as HTMLInputElement;
        const isHidden = input?.type === 'password';
        if (input) {
          input.type = isHidden ? 'text' : 'password';
          btn.innerHTML = isHidden ? eyeOffSVG : eyeSVG;
        }
      });
    });
  });

  async function handleSubmit(e: Event) {
    e.preventDefault();
    error = '';
    
    if (password !== confirmPassword) {
      error = 'Passwords do not match';
      return;
    }
    
    if (password.length < 8) {
      error = 'Password must be at least 8 characters';
      return;
    }
    
    loading = true;
    
    try {
      await authStore.signUp(email, password);
      success = true;
    } catch (err: any) {
      error = err.message || 'Failed to create account';
    } finally {
      loading = false;
    }
  }

  async function handleOAuth(provider: 'google' | 'azure') {
    try {
      await authStore.signInWithOAuth(provider);
    } catch (err: any) {
      error = err.message || 'Failed to sign up with ' + provider;
    }
  }
</script>

<svelte:head>
  <title>Sign Up - Study Vault</title>
</svelte:head>

<div class="auth-page">
  <div class="auth-card">
    <!-- Logo -->
    <div class="auth-logo">
      <div class="logo-mark">SV</div>
      <span class="logo-text">Study Vault</span>
    </div>

    <!-- Header -->
    <div class="auth-header">
      <h1 class="auth-title">Create account</h1>
      <p class="auth-subtitle">Start your optimized study journey today</p>
    </div>

    <!-- Success Message -->
    {#if success}
      <div class="success-message">
        <div class="success-icon">✉️</div>
        <div class="success-content">
          <h3>Check your email</h3>
          <p>We've sent you a confirmation link to activate your account.</p>
        </div>
      </div>
    {:else}
      <!-- Form -->
      <form class="auth-form" on:submit={handleSubmit}>
        {#if error}
          <div class="error-message">
            <span class="error-icon">⚠️</span>
            {error}
          </div>
        {/if}

        <div class="form-fields">
          <div class="field-group">
            <label for="email" class="field-label">Email</label>
            <input
              id="email"
              type="email"
              bind:value={email}
              class="field-input"
              placeholder="Enter your email"
              required
              disabled={loading}
            />
          </div>

          <div class="field-group">
            <label for="password" class="field-label">Password</label>
            <div class="field-wrapper">
              <input
                id="password"
                type="password"
                bind:value={password}
                class="field-input"
                placeholder="Create a strong password"
                required
                disabled={loading}
              />
              <button type="button" class="toggle-password" data-target="password" aria-label="Show password">
                {@html eyeSVG}
              </button>
            </div>
            <p class="field-hint">Minimum 8 characters</p>
          </div>

          <div class="field-group">
            <label for="confirmPassword" class="field-label">Confirm Password</label>
            <div class="field-wrapper">
              <input
                id="confirmPassword"
                type="password"
                bind:value={confirmPassword}
                class="field-input"
                placeholder="Confirm your password"
                required
                disabled={loading}
              />
              <button type="button" class="toggle-password" data-target="confirmPassword" aria-label="Show password">
                {@html eyeSVG}
              </button>
            </div>
          </div>
        </div>

        <button type="submit" class="btn-primary" disabled={loading}>
          {#if loading}
            <span class="loading-spinner"></span>
            Creating account...
          {:else}
            Create Account
          {/if}
        </button>
      </form>

      <!-- Divider -->
      <div class="divider">
        <span class="divider-text">Or sign up with</span>
      </div>

      <!-- Social Auth -->
      <div class="social-buttons">
        <button class="btn-social google" on:click={() => handleOAuth('google')}>
          <svg class="social-icon" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          Google
        </button>
        
        <button class="btn-social microsoft" on:click={() => handleOAuth('azure')}>
          <svg class="social-icon" viewBox="0 0 24 24">
            <rect x="2" y="2" width="9" height="9" fill="#f25022"/>
            <rect x="13" y="2" width="9" height="9" fill="#7fba00"/>
            <rect x="2" y="13" width="9" height="9" fill="#00a4ef"/>
            <rect x="13" y="13" width="9" height="9" fill="#ffb900"/>
          </svg>
          Microsoft
        </button>
      </div>
    {/if}

    <!-- Footer -->
    <div class="auth-footer">
      <p>Already have an account? <a href="/login">Sign in</a></p>
    </div>
  </div>
</div>

<style>
  /* Design Tokens */
  :root {
    --bg:             #0A0A0B;
    --surface:        #111114;
    --border:         rgba(255, 255, 255, 0.08);
    --border-focus:   rgba(200, 255, 0, 0.5);
    --accent:         #C8FF00;
    --accent-glow:    rgba(200, 255, 0, 0.25);
    --text-primary:   #F2F2F2;
    --text-muted:     #555560;
    --text-placeholder: rgba(255, 255, 255, 0.2);
    --radius-card:    16px;
    --radius-input:   10px;
    --radius-btn:     10px;
    --font-sans:      'Inter', sans-serif;
    --font-mono:      'JetBrains Mono', monospace;
  }

  /* Page Background */
  .auth-page {
    background: #0A0A0B;
    background-image: 
      radial-gradient(ellipse at 20% 50%, rgba(124, 92, 252, 0.06) 0%, transparent 60%),
      radial-gradient(ellipse at 80% 20%, rgba(200, 255, 0, 0.04) 0%, transparent 50%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
  }

  /* Card Container */
  .auth-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 48px 40px;
    width: 100%;
    max-width: 440px;
    box-shadow: 
      0 0 0 1px rgba(255, 255, 255, 0.03),
      0 32px 80px rgba(0, 0, 0, 0.4),
      0 0 120px rgba(124, 92, 252, 0.06);
  }

  /* Logo */
  .auth-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 32px;
  }

  .logo-mark {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-mono);
    font-size: 12px;
    font-weight: 700;
    color: #0A0A0B;
    letter-spacing: -0.02em;
    flex-shrink: 0;
  }

  .logo-text {
    font-family: var(--font-sans);
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.01em;
  }

  /* Typography */
  .auth-header {
    margin-bottom: 32px;
  }

  .auth-title {
    font-family: var(--font-sans);
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--text-primary);
    margin: 0 0 6px 0;
    line-height: 1.2;
  }

  .auth-subtitle {
    font-family: var(--font-sans);
    font-size: 14px;
    color: var(--text-muted);
    margin: 0;
    line-height: 1.5;
  }

  /* Form Fields */
  .form-fields {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .field-group {
    display: flex;
    flex-direction: column;
  }

  .field-label {
    display: block;
    font-size: 13px;
    font-weight: 500;
    color: var(--text-primary);
    margin-bottom: 8px;
    letter-spacing: -0.01em;
  }

  .field-input {
    width: 100%;
    height: 48px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border);
    border-radius: var(--radius-input);
    padding: 0 16px;
    font-family: var(--font-sans);
    font-size: 14px;
    color: var(--text-primary);
    outline: none;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    box-sizing: border-box;
  }

  .field-input::placeholder {
    color: var(--text-placeholder);
  }

  .field-input:focus {
    border-color: var(--border-focus);
    box-shadow: 0 0 0 3px rgba(200, 255, 0, 0.08);
    background: rgba(200, 255, 0, 0.02);
  }

  .field-input:not(:placeholder-shown):valid {
    border-color: rgba(200, 255, 0, 0.2);
  }

  .field-hint {
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 6px;
  }

  .field-wrapper {
    position: relative;
  }

  .field-wrapper .field-input {
    padding-right: 44px;
  }

  /* Password Toggle */
  .toggle-password {
    position: absolute;
    right: 14px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    cursor: pointer;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    padding: 0;
    transition: color 0.2s ease;
  }

  .toggle-password:hover {
    color: var(--text-primary);
  }

  /* Primary Button */
  .btn-primary {
    width: 100%;
    height: 52px;
    background: var(--accent);
    color: #0A0A0B;
    font-family: var(--font-sans);
    font-size: 14px;
    font-weight: 700;
    letter-spacing: -0.01em;
    border: none;
    border-radius: var(--radius-btn);
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.25s ease, transform 0.15s ease;
    margin-top: 8px;
  }

  .btn-primary::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, 
      rgba(255,255,255,0.15) 0%, 
      rgba(255,255,255,0) 60%);
    pointer-events: none;
  }

  .btn-primary::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, 
      transparent 0%, 
      rgba(255,255,255,0.1) 50%, 
      transparent 100%);
    transform: translateX(-100%);
    transition: transform 0.4s ease;
    pointer-events: none;
  }

  .btn-primary:hover {
    box-shadow: 0 0 30px var(--accent-glow), 0 8px 24px rgba(0,0,0,0.3);
    transform: translateY(-1px);
  }

  .btn-primary:hover::after {
    transform: translateX(100%);
  }

  .btn-primary:active {
    transform: translateY(0px);
    box-shadow: 0 0 16px var(--accent-glow);
  }

  .loading-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid transparent;
    border-top: 2px solid currentColor;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    display: inline-block;
    margin-right: 8px;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  /* Divider */
  .divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 24px 0;
  }

  .divider::before,
  .divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }

  .divider-text {
    font-size: 12px;
    color: var(--text-muted);
    white-space: nowrap;
    letter-spacing: 0.02em;
  }

  /* Social Buttons */
  .social-buttons {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 10px;
  }

  .btn-social {
    width: 100%;
    height: 48px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border);
    border-radius: var(--radius-btn);
    color: var(--text-primary);
    font-family: var(--font-sans);
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    transition: background 0.2s ease, border-color 0.2s ease;
  }

  .btn-social:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.14);
  }

  .social-icon {
    width: 18px;
    height: 18px;
  }

  /* Error/Success Messages */
  .error-message {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px;
    background-color: rgba(255, 69, 69, 0.1);
    border: 1px solid rgba(255, 69, 69, 0.3);
    border-radius: var(--radius-input);
    color: var(--text-primary);
    font-size: 14px;
    margin-bottom: 20px;
  }

  .success-message {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px;
    background-color: rgba(0, 255, 148, 0.1);
    border: 1px solid rgba(0, 255, 148, 0.3);
    border-radius: var(--radius-input);
    color: var(--text-primary);
    text-align: center;
    margin-bottom: 20px;
  }

  .success-icon {
    font-size: 24px;
  }

  .success-content h3 {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 4px;
  }

  .success-content p {
    font-size: 14px;
    opacity: 0.8;
    margin: 0;
  }

  /* Footer */
  .auth-footer {
    text-align: center;
    margin-top: 24px;
    font-size: 13px;
    color: var(--text-muted);
  }

  .auth-footer a {
    color: var(--accent);
    text-decoration: none;
    font-weight: 500;
    transition: opacity 0.2s ease;
  }

  .auth-footer a:hover {
    opacity: 0.8;
  }

  /* Mobile Responsive */
  @media (max-width: 480px) {
    .auth-card {
      padding: 32px 24px;
      border-radius: 0;
      border-left: none;
      border-right: none;
      min-height: 100vh;
      justify-content: flex-start;
      padding-top: 48px;
    }
  }
</style>
