<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { user } from '$lib/stores/auth';
  import { MessageSquare, Brain, Calendar, Target, Zap, BookOpen, ArrowRight } from 'lucide-svelte';

  let mounted = false;
  let loading = true;

  $: currentUser = $user;

  onMount(() => {
    mounted = true;
    loading = false;
  });

  function handleGetStarted() {
    if (currentUser) {
      goto('/dashboard');
    } else {
      goto('/login');
    }
  }
</script>

<svelte:head>
  <title>StudyVault - AI-Powered Study Assistant</title>
</svelte:head>

<div class="landing-page" class:mounted>
  <!-- Navigation -->
  <nav class="navbar">
    <div class="nav-container">
      <div class="nav-logo">
        <div class="logo-mark">SV</div>
        <span class="logo-text">StudyVault</span>
      </div>
      <div class="nav-actions">
        {#if currentUser}
          <button class="btn-secondary" on:click={() => goto('/dashboard')}>Dashboard</button>
        {:else}
          <button class="btn-secondary" on:click={() => goto('/login')}>Sign In</button>
          <button class="btn-primary" on:click={() => goto('/register')}>Get Started</button>
        {/if}
      </div>
    </div>
  </nav>

  <!-- Hero Section -->
  <section class="hero">
    <div class="hero-container">
      <div class="hero-content">
        <div class="hero-badge">
          <Zap class="badge-icon" />
          <span>Classical AI-Powered Learning</span>
        </div>
        <h1 class="hero-title">
          Study Smarter with<br>
          <span class="accent">AI-Powered</span> Assistance
        </h1>
        <p class="hero-description">
          Experience the future of learning with our advanced AI study assistant. 
          Built with classical AI algorithms, not just chatbots - we understand how you learn.
        </p>
        <div class="hero-actions">
          <button class="btn-primary btn-large" on:click={handleGetStarted}>
            {currentUser ? 'Go to Dashboard' : 'Start Learning Free'}
            <ArrowRight class="btn-icon" />
          </button>
          <button class="btn-outline btn-large" on:click={() => goto('/demo')}>
            <MessageSquare class="btn-icon" />
            Try Demo Chat
          </button>
        </div>
      </div>
      <div class="hero-visual">
        <div class="chat-preview">
          <div class="chat-header">
            <div class="chat-avatar">🧠</div>
            <div class="chat-info">
              <div class="chat-name">StudyVault AI</div>
              <div class="chat-status">Online</div>
            </div>
          </div>
          <div class="chat-messages">
            <div class="message ai">
              How can I help you study today?
            </div>
            <div class="message user">
              Can you explain algorithms?
            </div>
            <div class="message ai typing">
              I'll break down algorithms step by step...
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Features Section -->
  <section class="features">
    <div class="section-container">
      <div class="section-header">
        <h2 class="section-title">Advanced Learning Features</h2>
        <p class="section-description">
          Built with cutting-edge AI research and proven learning science
        </p>
      </div>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">
            <Brain />
          </div>
          <h3>Classical AI Pipeline</h3>
          <p>6-layer AI system using fuzzy logic, Dempster-Shafer theory, and hierarchical planning</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <Calendar />
          </div>
          <h3>Smart Scheduling</h3>
          <p>AI-powered study schedules that adapt to your learning patterns and exam deadlines</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <Target />
          </div>
          <h3>Personalized Learning</h3>
          <p>Adapts to your learning style and tracks your progress in real-time</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <BookOpen />
          </div>
          <h3>Syllabus Analysis</h3>
          <p>Upload your syllabus and get personalized study plans and topic prioritization</p>
        </div>
      </div>
    </div>
  </section>

  <!-- CTA Section -->
  <section class="cta">
    <div class="section-container">
      <div class="cta-content">
        <h2>Ready to Transform Your Study Experience?</h2>
        <p>Join thousands of students using AI to study smarter, not harder</p>
        <button class="btn-primary btn-large" on:click={handleGetStarted}>
          {currentUser ? 'Go to Dashboard' : 'Start Free Trial'}
          <ArrowRight class="btn-icon" />
        </button>
      </div>
    </div>
  </section>
</div>

<style>
  /* Design Tokens */
  :root {
    --bg: #0A0A0B;
    --surface: #111114;
    --accent: #C8FF00;
    --text-primary: #F2F2F2;
    --text-muted: #555560;
    --border: rgba(255, 255, 255, 0.08);
  }

  /* Base Styles */
  .landing-page {
    background: var(--bg);
    color: var(--text-primary);
    min-height: 100vh;
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }

  .landing-page.mounted {
    opacity: 1;
    transform: translateY(0);
  }

  /* Navigation */
  .navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: rgba(10, 10, 11, 0.8);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
    z-index: 1000;
  }

  .nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .nav-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .logo-mark {
    width: 32px;
    height: 32px;
    background: var(--accent);
    color: var(--bg);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 12px;
  }

  .logo-text {
    font-size: 1.25rem;
    font-weight: 600;
  }

  .nav-actions {
    display: flex;
    gap: 1rem;
    align-items: center;
  }

  /* Hero Section */
  .hero {
    padding: 8rem 2rem 4rem;
    min-height: 100vh;
    display: flex;
    align-items: center;
  }

  .hero-container {
    max-width: 1200px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
  }

  .hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(200, 255, 0, 0.1);
    border: 1px solid rgba(200, 255, 0, 0.2);
    padding: 0.5rem 1rem;
    border-radius: 2rem;
    font-size: 0.875rem;
    margin-bottom: 2rem;
  }

  .badge-icon {
    width: 16px;
    height: 16px;
    color: var(--accent);
  }

  .hero-title {
    font-size: 4rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 1.5rem;
  }

  .accent {
    color: var(--accent);
  }

  .hero-description {
    font-size: 1.25rem;
    color: var(--text-muted);
    margin-bottom: 2rem;
    line-height: 1.6;
  }

  .hero-actions {
    display: flex;
    gap: 1rem;
  }

  .hero-visual {
    display: flex;
    justify-content: center;
  }

  .chat-preview {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 1rem;
    width: 100%;
    max-width: 400px;
    overflow: hidden;
  }

  .chat-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    border-bottom: 1px solid var(--border);
  }

  .chat-avatar {
    width: 40px;
    height: 40px;
    background: var(--accent);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
  }

  .chat-name {
    font-weight: 600;
  }

  .chat-status {
    font-size: 0.875rem;
    color: var(--text-muted);
  }

  .chat-messages {
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .message {
    padding: 0.75rem;
    border-radius: 0.75rem;
    max-width: 80%;
  }

  .message.ai {
    background: rgba(200, 255, 0, 0.1);
    border: 1px solid rgba(200, 255, 0, 0.2);
    align-self: flex-start;
  }

  .message.user {
    background: rgba(255, 255, 255, 0.1);
    align-self: flex-end;
  }

  .message.typing::after {
    content: '...';
    animation: typing 1.5s infinite;
  }

  @keyframes typing {
    0%, 60%, 100% { opacity: 1; }
    30% { opacity: 0.3; }
  }

  /* Features Section */
  .features {
    padding: 6rem 2rem;
  }

  .section-container {
    max-width: 1200px;
    margin: 0 auto;
  }

  .section-header {
    text-align: center;
    margin-bottom: 4rem;
  }

  .section-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 1rem;
  }

  .section-description {
    font-size: 1.25rem;
    color: var(--text-muted);
  }

  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
  }

  .feature-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 1rem;
    padding: 2rem;
    text-align: center;
  }

  .feature-icon {
    width: 48px;
    height: 48px;
    background: rgba(200, 255, 0, 0.1);
    border: 1px solid rgba(200, 255, 0, 0.2);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1.5rem;
    color: var(--accent);
  }

  .feature-card h3 {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 1rem;
  }

  .feature-card p {
    color: var(--text-muted);
    line-height: 1.6;
  }

  /* CTA Section */
  .cta {
    padding: 6rem 2rem;
    text-align: center;
  }

  .cta-content h2 {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
  }

  .cta-content p {
    font-size: 1.25rem;
    color: var(--text-muted);
    margin-bottom: 2rem;
  }

  /* Buttons */
  .btn-primary, .btn-secondary, .btn-outline {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.2s ease;
    cursor: pointer;
    border: none;
  }

  .btn-primary {
    background: var(--accent);
    color: var(--bg);
  }

  .btn-primary:hover {
    opacity: 0.9;
    transform: translateY(-1px);
  }

  .btn-secondary {
    background: transparent;
    color: var(--text-primary);
    border: 1px solid var(--border);
  }

  .btn-secondary:hover {
    background: var(--surface);
  }

  .btn-outline {
    background: transparent;
    color: var(--accent);
    border: 1px solid var(--accent);
  }

  .btn-outline:hover {
    background: var(--accent);
    color: var(--bg);
  }

  .btn-large {
    padding: 1rem 2rem;
    font-size: 1.125rem;
  }

  .btn-icon {
    width: 16px;
    height: 16px;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .hero-container {
      grid-template-columns: 1fr;
      gap: 2rem;
    }

    .hero-title {
      font-size: 2.5rem;
    }

    .hero-actions {
      flex-direction: column;
    }

    .nav-container {
      padding: 1rem;
    }

    .nav-actions {
      gap: 0.5rem;
    }

    .features-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
