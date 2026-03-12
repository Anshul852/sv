<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  // Direct access - no authentication required
  let loading = true;

  onMount(async () => {
    // Redirect to chat immediately
    await goto('/chat');
  });
</script>

<svelte:head>
  <title>StudyVault AI - Direct Access</title>
  <meta name="description" content="Direct access to StudyVault AI chatbot" />
</svelte:head>

<div class="direct-access">
  {#if loading}
    <div class="loading-container">
      <div class="loading-spinner"></div>
      <h2>StudyVault AI</h2>
      <p>Initializing your intelligent study assistant...</p>
    </div>
  {/if}
</div>

<style>
  .direct-access {
    height: 100vh;
    width: 100vw;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }

  .loading-container {
    text-align: center;
    max-width: 400px;
    padding: 2rem;
  }

  .loading-spinner {
    width: 60px;
    height: 60px;
    border: 4px solid rgba(255, 255, 255, 0.3);
    border-top: 4px solid #ffffff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 2rem;
  }

  h2 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    background: linear-gradient(45deg, #fff, #f0f0f0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  p {
    font-size: 1.1rem;
    opacity: 0.9;
    margin: 0;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  :global(body) {
    margin: 0;
    padding: 0;
    overflow: hidden;
  }
</style>
