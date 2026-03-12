<script lang="ts">
    import { onMount } from "svelte";
    import { user } from "$lib/stores/auth";
    import StatsCards from "$lib/components/dashboard/StatsCards.svelte";
    import CognitiveLoadMeter from "$lib/components/dashboard/CognitiveLoadMeter.svelte";
    import ScheduleTimeline from "$lib/components/dashboard/ScheduleTimeline.svelte";
    import StudyPlanCard from "$lib/components/dashboard/StudyPlanCard.svelte";
    import UpcomingExams from "$lib/components/dashboard/UpcomingExams.svelte";
    import LearnerTypeBadge from "$lib/components/dashboard/LearnerTypeBadge.svelte";
    import PrivacyStatusBar from "$lib/components/dashboard/PrivacyStatusBar.svelte";
    import StudyPatternHeatmap from "$lib/components/dashboard/StudyPatternHeatmap.svelte";
    import ResilienceScoreCard from "$lib/components/dashboard/ResilienceScoreCard.svelte";

    let userProfile = null;
    let loading = true;
    let mounted = false;
    let upcomingExams = [];
    let crisisMode = false;
    let warningMode = false;

    $: currentUser = $user;
    $: displayName =
        userProfile?.display_name ||
        currentUser?.user?.email?.split("@")[0] ||
        currentUser?.email?.split("@")[0] ||
        "Student";
    $: greeting =
        new Date().getHours() < 12
            ? "Good morning"
            : new Date().getHours() < 18
              ? "Good afternoon"
              : "Good evening";
    $: today = new Date().toLocaleDateString("en-US", {
        weekday: "long",
        month: "long",
        day: "numeric",
    });

    // Readiness range - Section 1.3
    $: readinessScore = userProfile?.readiness || 73;
    $: readinessRange = `${Math.max(0, readinessScore - 13)}–${Math.min(100, readinessScore + 13)}% ready`;
    $: readinessColor = readinessScore >= 70 ? 'var(--accent)' : '#f97316';

    onMount(async () => {
        mounted = true;
        try {
            if (!currentUser) return;
            
            // Fetch user profile
            const profileResponse = await fetch(
                `${import.meta.env.VITE_API_URL || "http://localhost:8000"}/api/students/profile`,
                {
                    headers: {
                        Authorization: `Bearer ${currentUser.session?.access_token}`,
                    },
                },
            );
            if (profileResponse.ok) {
                userProfile = await profileResponse.json();
            }
            
            // Fetch upcoming exams for crisis detection - Section 1.4
            const examsResponse = await fetch(
                `${import.meta.env.VITE_API_URL || "http://localhost:8000"}/api/students/exams`,
                {
                    headers: {
                        Authorization: `Bearer ${currentUser.session?.access_token}`,
                    },
                },
            );
            if (examsResponse.ok) {
                upcomingExams = await examsResponse.json();
                checkExamProximity();
            }
        } catch (error) {
            console.error("Failed to fetch data:", error);
        } finally {
            loading = false;
        }
    });
    
    function checkExamProximity() {
        const now = new Date();
        upcomingExams.forEach(exam => {
            const examDate = new Date(exam.date);
            const hoursUntilExam = (examDate.getTime() - now.getTime()) / (1000 * 60 * 60);
            
            if (hoursUntilExam <= 24) {
                crisisMode = true;
            } else if (hoursUntilExam <= 72) {
                warningMode = true;
            }
        });
    }
    
    function goToCrisisMode() {
        const exam = upcomingExams[0];
        window.location.href = `/crisis?subject=${exam.subject}&hours=${Math.floor((new Date(exam.date).getTime() - new Date().getTime()) / (1000 * 60 * 60))}`;
    }
</script>

<div class="page" class:mounted>
    <!-- Crisis Mode Banner - Section 1.4 -->
    {#if crisisMode && upcomingExams.length > 0}
        <div class="crisis-banner">
            <div class="crisis-content">
                <span class="crisis-text">
                    Your {upcomingExams[0].subject} exam is in {Math.floor((new Date(upcomingExams[0].date).getTime() - new Date().getTime()) / (1000 * 60 * 60))} hours.
                </span>
                <div class="crisis-actions">
                    <button class="crisis-btn" on:click={goToCrisisMode}>
                        Open Crisis Mode
                    </button>
                    <button class="dismiss-btn" on:click={() => crisisMode = false}>
                        Dismiss
                    </button>
                </div>
            </div>
        </div>
    {:else if warningMode && upcomingExams.length > 0}
        <div class="warning-banner">
            <div class="warning-content">
                <span class="warning-text">
                    {upcomingExams[0].subject} in {Math.floor((new Date(upcomingExams[0].date).getTime() - new Date().getTime()) / (1000 * 60 * 60))} days. Your plan has been tightened.
                </span>
            </div>
        </div>
    {/if}

    <!-- ── Header ── -->
    <header class="page-header">
        <div class="header-left">
            <p class="greeting-label">{today}</p>
            <h1 class="greeting-heading">
                {greeting}, <span class="accent">{displayName}</span>
            </h1>
            <!-- Readiness Range - Section 1.3 -->
            <div class="readiness-display">
                <span class="readiness-text" style="color: {readinessColor}">
                    Estimated {readinessRange}
                </span>
                <span class="readiness-caveat">
                    based on what I can see — your judgment matters more than this estimate
                </span>
            </div>
        </div>
        <div class="header-right">
            <PrivacyStatusBar />
        </div>
    </header>

    <div class="divider" />

    <!-- ── Stats ── -->
    <StatsCards {userProfile} />

    <div class="divider" />

    <!-- ── Main Grid ── -->
    <div class="main-grid">
        <!-- Left column -->
        <div class="col-main">
            <div class="card-section">
                <div class="section-header">
                    <span class="section-dot" />
                    <h2 class="section-title">Today's Schedule</h2>
                </div>
                <ScheduleTimeline {userProfile} />
            </div>

            <div class="card-section">
                <div class="section-header">
                    <span class="section-dot" />
                    <h2 class="section-title">Weekly Study Plan</h2>
                </div>
                <StudyPlanCard {userProfile} />
            </div>
        </div>

        <!-- Right column -->
        <div class="col-side">
            <div class="card-section">
                <ResilienceScoreCard score={userProfile?.resilience || 78} />
            </div>

            <div class="card-section">
                <div class="section-header">
                    <span class="section-dot" />
                    <h2 class="section-title">Cognitive Load</h2>
                </div>
                <CognitiveLoadMeter
                    level={userProfile?.cognitive_load || 0}
                    {userProfile}
                />
            </div>

            <div class="card-section">
                <div class="section-header">
                    <span class="section-dot" />
                    <h2 class="section-title">Upcoming Exams</h2>
                </div>
                <UpcomingExams {userProfile} />
            </div>

            <div class="card-section">
                <div class="section-header">
                    <span class="section-dot" />
                    <h2 class="section-title">Study Pattern</h2>
                </div>
                <StudyPatternHeatmap />
            </div>

            <div class="card-section">
                <div class="section-header">
                    <span class="section-dot" />
                    <h2 class="section-title">Learner Profile</h2>
                </div>
                <LearnerTypeBadge
                    type={userProfile?.learner_type || "omni"}
                    vak={userProfile?.vak_style || "visual"}
                    {userProfile}
                />
            </div>
        </div>
    </div>
</div>

<style>
    @import url("https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&display=swap");

    .page {
        font-family: "Geist", system-ui, sans-serif;
        display: flex;
        flex-direction: column;
        gap: 20px;
        padding: 28px 32px 48px;
        max-width: 1280px;
        width: 100%;
        opacity: 0;
        transform: translateY(6px);
        transition:
            opacity 300ms ease,
            transform 300ms ease;
    }

    .page.mounted {
        opacity: 1;
        transform: translateY(0);
    }

    /* ── Header ── */
    .page-header {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 16px;
        flex-wrap: wrap;
    }

    .header-left {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .readiness-display {
        display: flex;
        flex-direction: column;
        gap: 2px;
        margin-top: 4px;
    }

    .readiness-text {
        font-size: 14px;
        font-weight: 600;
        margin: 0;
    }

    .readiness-caveat {
        font-size: 11px;
        color: rgba(255, 255, 255, 0.4);
        font-style: italic;
        margin: 0;
    }

    /* Crisis Banners - Section 1.4 */
    .crisis-banner {
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: var(--radius-card);
        padding: 16px;
        margin-bottom: 20px;
    }

    .crisis-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        flex-wrap: wrap;
    }

    .crisis-text {
        color: #ef4444;
        font-size: 14px;
        font-weight: 600;
    }

    .crisis-actions {
        display: flex;
        gap: 8px;
    }

    .crisis-btn {
        background: #ef4444;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: var(--radius-input);
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
    }

    .dismiss-btn {
        background: transparent;
        color: rgba(255, 255, 255, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 8px 16px;
        border-radius: var(--radius-input);
        font-size: 12px;
        cursor: pointer;
    }

    .warning-banner {
        background: rgba(251, 146, 60, 0.08);
        border: 1px solid rgba(251, 146, 60, 0.3);
        border-radius: var(--radius-card);
        padding: 12px;
        margin-bottom: 20px;
    }

    .warning-content {
        text-align: center;
    }

    .warning-text {
        color: #fb923c;
        font-size: 13px;
        font-weight: 500;
    }

    .greeting-label {
        font-size: 11px;
        font-weight: 500;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.3);
        margin: 0;
    }

    .greeting-heading {
        font-size: 24px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.92);
        letter-spacing: -0.5px;
        margin: 0;
        line-height: 1.2;
    }

    .accent {
        color: #a3e635;
    }

    .header-right {
        display: flex;
        align-items: center;
        padding-bottom: 2px;
    }

    /* ── Divider ── */
    .divider {
        height: 1px;
        background: rgba(255, 255, 255, 0.05);
        flex-shrink: 0;
    }

    /* ── Section labels ── */
    .card-section {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .section-header {
        display: flex;
        align-items: center;
        gap: 7px;
    }

    .section-dot {
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: #a3e635;
        flex-shrink: 0;
    }

    .section-title {
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.28);
        margin: 0;
    }

    /* ── Main Grid ── */
    .main-grid {
        display: grid;
        grid-template-columns: 1fr 300px;
        gap: 20px;
        align-items: start;
    }

    .col-main {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .col-side {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    @media (max-width: 960px) {
        .page {
            padding: 20px 16px 40px;
        }
        .main-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
