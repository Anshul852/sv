<script lang="ts">
    import "../app.css";
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import { authStore } from "$lib/stores/auth";
    import { themeStore, applyTheme } from "$lib/stores/themeStore";
    import {
        getDeepWorkSessionsCount,
        getStudySessionsCount,
        initDB,
    } from "$lib/db/indexeddb";
    import {
        fetchAndDecryptBlobs,
        processSyncQueue,
        registerSyncListeners,
    } from "$lib/utils/sync";
    import { supabase } from "$lib/utils/supabase";
    import AppSidebar from "$lib/components/AppSidebar.svelte";

    let sidebarCollapsed = false;
    let appReady = false;

    onMount(() => {
        let cleanup: (() => void) | undefined;

        themeStore.subscribe((theme) => {
            applyTheme(theme);
        });

        (async () => {
            await initDB();
            await authStore.initializeAuth();

            const {
                data: { session },
            } = await supabase.auth.getSession();
            if (session) {
                const [studyCount, deepWorkCount] = await Promise.all([
                    getStudySessionsCount(),
                    getDeepWorkSessionsCount(),
                ]);
                if (studyCount === 0 && deepWorkCount === 0) {
                    await fetchAndDecryptBlobs(session.user.id);
                }
            }

            await processSyncQueue();
            cleanup = registerSyncListeners(() => processSyncQueue());
        })();

        requestAnimationFrame(() => {
            appReady = true;
        });

        return () => {
            cleanup?.();
        };
    });

    $: isGuestRoute = ['/', '/login', '/register'].includes($page?.url?.pathname ?? "");

    $: routeLabel = (() => {
        const p = $page?.url?.pathname ?? "";
        if (p.startsWith("/chat")) return "AI Chat";
        if (p.startsWith("/schedule")) return "Schedule";
        if (p.startsWith("/dashboard")) return "Dashboard";
        if (p.startsWith("/settings")) return "Settings";
        if (p.startsWith("/profile")) return "Profile";
        return "StudyVault";
    })();
</script>

<svelte:head>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link
        href="https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;600;700;800&display=swap"
        rel="stylesheet"
    />
</svelte:head>

<div class="shell" class:ready={appReady}>
    <!-- App-wide grid texture -->
    <div class="grid-bg" aria-hidden="true"></div>

    {#if !isGuestRoute}
        <!-- Sidebar — fully controlled by AppSidebar component -->
        <AppSidebar bind:collapsed={sidebarCollapsed} />
    {/if}

    <!-- Main column -->
    <div class="body" class:collapsed={sidebarCollapsed} class:full={isGuestRoute}>
        {#if !isGuestRoute}
            <!-- Topbar -->
            <header class="topbar">
                <button
                    class="tog-btn"
                    on:click={() => (sidebarCollapsed = !sidebarCollapsed)}
                    aria-label={sidebarCollapsed
                        ? "Expand sidebar"
                        : "Collapse sidebar"}
                >
                    <svg
                        width="14"
                        height="14"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        {#if sidebarCollapsed}
                            <line x1="3" y1="6" x2="21" y2="6" />
                            <line x1="3" y1="12" x2="21" y2="12" />
                            <line x1="3" y1="18" x2="21" y2="18" />
                        {:else}
                            <line x1="3" y1="6" x2="15" y2="6" />
                            <line x1="3" y1="12" x2="21" y2="12" />
                            <line x1="3" y1="18" x2="15" y2="18" />
                        {/if}
                    </svg>
                </button>

                <div class="breadcrumb">
                    <span class="bc-app">StudyVault</span>
                    <span class="bc-sep">/</span>
                    <span class="bc-page">{routeLabel}</span>
                </div>

                <div class="topbar-right">
                    <div class="priv-pill">
                        <span class="pill-dot lime-dot"></span>
                        <svg
                            width="9"
                            height="9"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2.5"
                        >
                            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                        </svg>
                        <span>Privacy Protected</span>
                    </div>
                    <div class="sync-pill">
                        <span class="pill-dot cyan-dot"></span>
                        <span>Synced</span>
                    </div>
                </div>
            </header>
        {/if}

        <!-- Slot -->
        <main class="main sv-scroll">
            <slot />
        </main>
    </div>
</div>

<style>
    /* ── Global reset & tokens ──────────────────────────────────────────────── */
    :global(html, body) {
        margin: 0;
        padding: 0;
        height: 100%;
        background: #060608;
        color: #e0e0e0;
        font-family: "Syne", sans-serif;
        -webkit-font-smoothing: antialiased;
        overflow: hidden;
    }
    :global(*, *::before, *::after) {
        box-sizing: border-box;
    }
    :global(button) {
        font-family: inherit;
        cursor: pointer;
    }
    :global(a) {
        color: inherit;
        text-decoration: none;
    }

    :global(:root) {
        --bg: #060608;
        --panel: #0c0c10;
        --border: rgba(255, 255, 255, 0.07);
        --lime: #b5ff4d;
        --cyan: #00d4c8;
        --orange: #ff9500;
        --purple: #c084fc;
        --red: #ff5555;
        --dim: rgba(255, 255, 255, 0.38);
        --mono: "Space Mono", monospace;
        --radius: 14px;
        --topbar-h: 46px;
        --sb-w: 220px;
        --sb-col-w: 56px;
        --ease: 260ms cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ── Shell ──────────────────────────────────────────────────────────────── */
    .shell {
        display: flex;
        height: 100vh;
        width: 100vw;
        background: var(--bg);
        position: relative;
        overflow: hidden;
        opacity: 0;
        transition: opacity 280ms ease;
    }
    .shell.ready {
        opacity: 1;
    }

    /* Grid overlay */
    .grid-bg {
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        background-image:
            linear-gradient(rgba(181, 255, 77, 0.025) 1px, transparent 1px),
            linear-gradient(
                90deg,
                rgba(181, 255, 77, 0.025) 1px,
                transparent 1px
            );
        background-size: 52px 52px;
        mask-image: radial-gradient(
            ellipse 100% 80% at 50% 0%,
            black 30%,
            transparent 100%
        );
    }

    /* ── Body (right of sidebar) ────────────────────────────────────────────── */
    .body {
        display: flex;
        flex-direction: column;
        flex: 1;
        min-width: 0;
        height: 100vh;
        margin-left: var(--sb-w);
        transition: margin-left var(--ease);
        position: relative;
        z-index: 1;
    }
    .body.collapsed {
        margin-left: var(--sb-col-w);
    }
    .body.full {
        margin-left: 0;
    }

    /* ── Topbar ─────────────────────────────────────────────────────────────── */
    .topbar {
        height: var(--topbar-h);
        flex-shrink: 0;
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0 20px 0 14px;
        border-bottom: 1px solid var(--border);
        background: rgba(6, 6, 8, 0.88);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        position: sticky;
        top: 0;
        z-index: 50;
    }

    .tog-btn {
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid var(--border);
        border-radius: 8px;
        color: var(--dim);
        flex-shrink: 0;
        transition:
            background 140ms,
            color 140ms,
            border-color 140ms;
    }
    .tog-btn:hover {
        background: rgba(255, 255, 255, 0.08);
        color: #fff;
        border-color: rgba(255, 255, 255, 0.14);
    }

    .breadcrumb {
        display: flex;
        align-items: center;
        gap: 7px;
        flex: 1;
        min-width: 0;
    }
    .bc-app {
        font-family: var(--mono);
        font-size: 10px;
        font-weight: 700;
        color: var(--dim);
        letter-spacing: 0.08em;
        white-space: nowrap;
    }
    .bc-sep {
        color: rgba(255, 255, 255, 0.15);
        font-size: 13px;
    }
    .bc-page {
        font-family: var(--mono);
        font-size: 10px;
        font-weight: 700;
        color: var(--lime);
        letter-spacing: 0.08em;
        white-space: nowrap;
    }

    .topbar-right {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-shrink: 0;
    }

    .priv-pill,
    .sync-pill {
        display: flex;
        align-items: center;
        gap: 5px;
        padding: 4px 11px;
        border-radius: 20px;
        font-family: var(--mono);
        font-size: 9px;
        letter-spacing: 0.06em;
        white-space: nowrap;
    }
    .priv-pill {
        background: rgba(181, 255, 77, 0.07);
        border: 1px solid rgba(181, 255, 77, 0.18);
        color: var(--lime);
    }
    .sync-pill {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid var(--border);
        color: var(--dim);
    }

    .pill-dot {
        width: 5px;
        height: 5px;
        border-radius: 50%;
        flex-shrink: 0;
        animation: pulse 2s ease-in-out infinite;
    }
    .lime-dot {
        background: var(--lime);
    }
    .cyan-dot {
        background: var(--cyan);
        animation-delay: 1s;
    }

    /* ── Main / slot ────────────────────────────────────────────────────────── */
    .main {
        flex: 1;
        overflow-y: auto;
        overflow-x: hidden;
        display: flex;
        flex-direction: column;
    }

    /* ── Shared global utilities exposed to all child pages ─────────────────── */

    /* Scrollbar */
    :global(.sv-scroll) {
        scrollbar-width: thin;
        scrollbar-color: rgba(255, 255, 255, 0.08) transparent;
    }
    :global(.sv-scroll::-webkit-scrollbar) {
        width: 5px;
    }
    :global(.sv-scroll::-webkit-scrollbar-thumb) {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 3px;
    }
    :global(.sv-scroll::-webkit-scrollbar-thumb:hover) {
        background: rgba(255, 255, 255, 0.14);
    }

    /* Panel card */
    :global(.sv-panel) {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: var(--radius);
    }

    /* Section label */
    :global(.sv-label) {
        display: flex;
        align-items: center;
        gap: 7px;
        font-family: var(--mono);
        font-size: 9px;
        font-weight: 700;
        letter-spacing: 0.14em;
        color: var(--dim);
        text-transform: uppercase;
    }

    /* Accent + ghost buttons */
    :global(.sv-btn-accent) {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 8px 16px;
        background: var(--lime);
        border: none;
        border-radius: 9px;
        font-family: "Syne", sans-serif;
        font-size: 12px;
        font-weight: 700;
        color: #000;
        cursor: pointer;
        transition: filter 140ms;
    }
    :global(.sv-btn-accent:hover) {
        filter: brightness(1.08);
    }

    :global(.sv-btn-ghost) {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 7px 14px;
        background: transparent;
        border: 1px solid var(--border);
        border-radius: 9px;
        font-family: "Syne", sans-serif;
        font-size: 12px;
        font-weight: 600;
        color: var(--dim);
        cursor: pointer;
        transition:
            border-color 140ms,
            color 140ms;
    }
    :global(.sv-btn-ghost:hover) {
        border-color: rgba(255, 255, 255, 0.18);
        color: rgba(255, 255, 255, 0.8);
    }

    /* Page wrapper for child routes */
    :global(.page-wrap) {
        padding: 22px 26px 48px;
        max-width: 1440px;
        width: 100%;
    }

    /* ── Keyframes ──────────────────────────────────────────────────────────── */
    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
        }
        50% {
            opacity: 0.3;
        }
    }

    /* ── Responsive ─────────────────────────────────────────────────────────── */
    @media (max-width: 900px) {
        :global(:root) {
            --sb-w: 200px;
        }
    }
    @media (max-width: 700px) {
        .body {
            margin-left: 0 !important;
        }
        .topbar {
            padding: 0 14px;
        }
        .priv-pill span:last-child,
        .sync-pill span:last-child {
            display: none;
        }
    }
</style>
