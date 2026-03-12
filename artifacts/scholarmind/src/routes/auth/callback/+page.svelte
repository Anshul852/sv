<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { supabase } from '$lib/utils/supabase';

  let message = 'Completing sign-in…';

  onMount(async () => {
    try {
      const { data } = await supabase.auth.getSession();
      if (data.session) {
        goto('/dashboard');
        return;
      }

      const { data: listener } = supabase.auth.onAuthStateChange((_event, session) => {
        if (session) {
          goto('/dashboard');
        }
      });

      setTimeout(() => {
        listener.subscription.unsubscribe();
        message = 'Sign-in did not complete. Please go back and try again.';
      }, 8000);
    } catch {
      message = 'Sign-in failed. Please go back and try again.';
    }
  });
</script>

<div class="min-h-screen bg-bg-primary flex items-center justify-center px-4">
  <div class="card max-w-md w-full text-center">
    <div class="w-12 h-12 mx-auto mb-4 rounded-xl bg-gradient-to-br from-accent-primary to-accent-secondary"></div>
    <h1 class="text-xl font-semibold mb-2">Study Vault</h1>
    <p class="text-text-secondary">{message}</p>
  </div>
</div>
