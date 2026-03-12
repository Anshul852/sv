<script lang="ts">
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { fade } from 'svelte/transition';
  import { supabase } from '$lib/utils/supabase';

  type StudentProfile = {
    id: string;
    user_id: string;
    full_name?: string | null;
    learner_type?: string | null;
    public_key?: string | null;
    created_at?: string | null;
  };

  let loading = true;
  let error = '';
  let demo = false;

  let email: string | null = null;
  let userId: string | null = null;
  let profile: StudentProfile | null = null;

  onMount(async () => {
    demo = $page.url.searchParams.has('demo');

    try {
      const { data } = await supabase.auth.getSession();
      const session = data.session;

      if (!session && !demo) {
        goto('/login');
        return;
      }

      if (demo) {
        email = 'demo@student.dev';
        userId = 'demo-user-id';
        profile = {
          id: 'demo-id',
          user_id: 'demo-user-id',
          full_name: 'Demo Student',
          learner_type: 'Linear',
          public_key: 'placeholder'
        };
        loading = false;
        return;
      }

      email = session?.user?.email ?? null;
      userId = session?.user?.id ?? null;

      if (!userId) {
        goto('/login');
        return;
      }

      const { data: row, error: dbError } = await supabase
        .from('student_profiles')
        .select('*')
        .eq('user_id', userId)
        .maybeSingle();

      if (dbError) {
        error = dbError.message;
        loading = false;
        return;
      }

      profile = (row as StudentProfile | null) ?? null;
      loading = false;
    } catch (e: any) {
      error = e?.message || 'Failed to load profile';
      loading = false;
    }
  });
</script>

<div class="min-h-screen bg-bg-primary mesh-bg" in:fade>
  <header class="fixed top-0 left-0 right-0 z-50 bg-bg-primary/70 backdrop-blur-xl border-b border-border-subtle">
    <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
      <a href="/" class="flex items-center gap-2 lift">
        <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-accent-primary to-accent-secondary flex items-center justify-center">
          <span class="text-white font-bold text-sm">S</span>
        </div>
        <span class="text-xl font-bold text-gradient">Study Vault</span>
      </a>

      <nav class="flex items-center gap-6">
        <a href="/dashboard" class="text-text-secondary hover:text-text-primary transition-colors">Dashboard</a>
        <a href="/profile" class="text-accent-primary font-medium">Profile</a>
        {#if demo}
          <a href="/login" class="btn btn-secondary text-sm">Sign In</a>
        {:else}
          <a href="/settings" class="text-text-secondary hover:text-text-primary transition-colors">Settings</a>
        {/if}
      </nav>
    </div>
  </header>

  <main class="pt-24 pb-12 px-6">
    <div class="max-w-4xl mx-auto">
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8">
        <div>
          <h1 class="text-display font-extrabold mb-2">Student Profile</h1>
          <p class="text-text-secondary text-body">Identity + preferences.</p>
        </div>
        <div class="flex items-center gap-3">
          <a href="/profile?demo=1" class="btn btn-secondary">Demo</a>
          <a href="/dashboard?demo=1" class="btn btn-primary">Dashboard Demo</a>
        </div>
      </div>

      {#if loading}
        <div class="card">
          <div class="skeleton h-6 w-40 rounded-md"></div>
          <div class="mt-4 space-y-3">
            <div class="skeleton h-12 rounded-lg"></div>
            <div class="skeleton h-12 rounded-lg"></div>
            <div class="skeleton h-12 rounded-lg"></div>
          </div>
        </div>
      {:else}
        {#if error}
          <div class="card border border-red-800 bg-red-900/20 text-red-300">{error}</div>
        {/if}

        <div class="grid md:grid-cols-2 gap-6 mt-6">
          <div class="card lift">
            <div class="text-sm text-text-muted">Supabase User</div>
            <div class="mt-4 space-y-3">
              <div class="flex items-center justify-between gap-4">
                <span class="text-text-secondary">Email</span>
                <span class="font-medium truncate max-w-[60%]">{email ?? '—'}</span>
              </div>
              <div class="flex items-center justify-between gap-4">
                <span class="text-text-secondary">User ID</span>
                <span class="font-medium truncate max-w-[60%]">{userId ?? '—'}</span>
              </div>
            </div>
          </div>

          <div class="card-elevated lift">
            <div class="text-sm text-text-muted">student_profiles row</div>
            {#if profile}
              <div class="mt-4 space-y-3">
                <div class="flex items-center justify-between gap-4">
                  <span class="text-text-secondary">Full name</span>
                  <span class="font-medium truncate max-w-[60%]">{profile.full_name ?? '—'}</span>
                </div>
                <div class="flex items-center justify-between gap-4">
                  <span class="text-text-secondary">Learner type</span>
                  <span class="font-medium truncate max-w-[60%]">{profile.learner_type ?? '—'}</span>
                </div>
                <div class="flex items-center justify-between gap-4">
                  <span class="text-text-secondary">Public key</span>
                  <span class="font-medium truncate max-w-[60%]">{profile.public_key ? 'present' : '—'}</span>
                </div>
              </div>
            {:else}
              <div class="mt-4">
                <div class="glass rounded-lg p-4">
                  <div class="font-semibold">No profile row found</div>
                  <p class="text-text-secondary text-sm mt-1">Register once to create it, or insert a row in Supabase for this user_id.</p>
                </div>
              </div>
            {/if}
          </div>
        </div>
      {/if}
    </div>
  </main>
</div>
