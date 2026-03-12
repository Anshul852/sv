<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import { goto } from "$app/navigation";
  import { user } from "$lib/stores/auth";
  import { chatStore } from "$lib/stores/chatStore";
  import { processMessage } from "$lib/chatbot/cleanChatbot";
  import ChatMessages from "$lib/components/chatbot/ChatMessages.svelte";
  import {
    BookOpen,
    Calendar,
    Zap,
    BarChart2,
    Scan,
    CalendarPlus,
    Brain,
    HeartHandshake,
    Plus,
    MessageSquare,
    Settings,
    Trash2,
    PanelRight,
    Menu,
    BookMarked,
    X,
    Camera,
    Paperclip,
    ArrowUp,
    Check,
    Mic,
    Share2,
    ChevronDown,
    FileText,
    Smartphone,
  } from "lucide-svelte";

  // ── State ──────────────────────────────────────
  let mounted = false;
  let loading = true;
  let inputText = "";
  let isTyping = false;
  let mobileSidebarOpen = false;
  let contextPanelOpen = true;
  let activeConnector = "StudyVault AI";
  let connectorDropdownOpen = false;
  let moreOptionsOpen = false;
  let chatTitle = "Focus Session";

  // Subscribe to chat store
  const { currentChat } = chatStore;
  $: messages = $currentChat?.messages || [];

  const connectors = [
    {
      id: "studyvault",
      name: "StudyVault AI",
      color: "#a3e635",
      category: "ai",
      isConnected: true,
      isActive: true,
      icon: "SV",
    },
    {
      id: "claude",
      name: "Claude",
      color: "#FF6B35",
      category: "ai",
      isConnected: false,
      isActive: false,
      icon: "◆",
    },
    {
      id: "gemini",
      name: "Gemini",
      color: "#4285F4",
      category: "ai",
      isConnected: false,
      isActive: false,
      icon: "✦",
    },
    {
      id: "obsidian",
      name: "Obsidian",
      color: "#7C3AED",
      category: "note",
      isConnected: false,
      isActive: false,
      icon: "💎",
    },
    {
      id: "notion",
      name: "Notion",
      color: "#000000",
      category: "note",
      isConnected: false,
      isActive: false,
      icon: "📋",
    },
  ];

  async function sendMessage() {
    if (!inputText.trim() || isTyping) return;

    const messageText = inputText;
    inputText = "";
    isTyping = true;

    try {
      // processMessage in cleanChatbot.ts handles adding the user message
      await processMessage({
        input: messageText,
        conversationId: "current",
        connectorId: "studyvault",
        profile: null,
        onChunk: () => {},
        onComplete: () => {
          isTyping = false;
        },
        onError: (error: string) => {
          console.error("Chat error:", error);
          isTyping = false;
        },
      });
    } catch (error) {
      console.error("Send error:", error);
      isTyping = false;
    } finally {
      isTyping = false; // Emergency fallback
    }
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  function toggleMobileSidebar() {
    mobileSidebarOpen = !mobileSidebarOpen;
  }
  function toggleContextPanel() {
    contextPanelOpen = !contextPanelOpen;
  }
  function clearChat() {
    chatStore.clearChat();
  }

  function getTimeGreeting() {
    const hour = new Date().getHours();
    if (hour < 12) return "Good morning";
    if (hour < 18) return "Good afternoon";
    return "Good evening";
  }

  function handleSuggestionClick(suggestion: string) {
    inputText = suggestion;
    sendMessage();
  }

  function selectConnector(connectorId: string) {
    connectors.forEach((c) => (c.isActive = c.id === connectorId));
    activeConnector =
      connectors.find((c) => c.id === connectorId)?.name || "StudyVault AI";
    connectorDropdownOpen = false;
  }

  function closeAllDropdowns() {
    connectorDropdownOpen = false;
    moreOptionsOpen = false;
  }

  function handleMoreOptionClick(action: string) {
    moreOptionsOpen = false;
    if (action === "add-connector") goto("/settings/connectors");
    console.log("Action triggered:", action);
  }

  onMount(async () => {
    // Initialize chat store (loads DB and ensures currentChatId)
    await chatStore.initializeWithoutAuth();

    setTimeout(() => {
      loading = false;
      mounted = true;
    }, 800);
  });
</script>

<svelte:head><title>AI Chat — StudyVault</title></svelte:head>
<svelte:window on:click={closeAllDropdowns} />

{#if loading}
  <div class="loading-overlay">
    <div class="background-glow"></div>
    <div class="loading-inner">
      <div class="loading-icon">
        <Zap size={32} fill="#a3e635" />
      </div>
      <p class="loading-text">StudyVault AI</p>
      <div class="loading-status">Synchronizing neural pathways...</div>
      <div class="loading-bar"><div class="loading-fill" /></div>
    </div>
  </div>
{/if}

<div class="page" class:mounted>
  <header class="page-header">
    <div class="header-left">
      <div class="header-icon">
        <MessageSquare size={14} strokeWidth={2} />
      </div>
      <div>
        <h1 class="page-title">AI Chat</h1>
        <p class="page-sub">
          Intelligent study assistant with classical algorithms
        </p>
      </div>
    </div>
    <div class="header-actions">
      <button class="ghost-btn" on:click={toggleContextPanel}>
        <PanelRight size={14} strokeWidth={2} />
        Context
      </button>
      <button class="accent-btn" on:click={() => chatStore.newChat()}>
        <Plus size={14} strokeWidth={2} />
        New Chat
      </button>
    </div>
  </header>

  <div class="divider" />

  <div class="main-layout">
    <div class="sidebar" class:mobile-open={mobileSidebarOpen}>
      <div class="sidebar-top">
        <div class="logo-row">
          <div class="logo-icon">SV</div>
          <span class="logo-text">StudyVault AI</span>
        </div>

        <button class="new-chat-btn" on:click={() => chatStore.newChat()}>
          <Plus size={16} />
          <span>New Chat</span>
        </button>

        <button
          class="connector-chip-sidebar"
          on:click|stopPropagation={() =>
            (connectorDropdownOpen = !connectorDropdownOpen)}
        >
          <div
            class="connector-dot"
            style="background: {connectors.find((c) => c.isActive)?.color}"
          ></div>
          <span class="connector-name"
            >{connectors.find((c) => c.isActive)?.name}</span
          >
          <ChevronDown size={14} />
        </button>

        {#if connectorDropdownOpen}
          <div class="connector-dropdown">
            {#each connectors as connector}
              <button
                class="connector-option"
                class:active={connector.isActive}
                on:click={() => selectConnector(connector.id)}
              >
                <span class="option-icon" style="color: {connector.color}"
                  >{connector.icon}</span
                >
                <span class="option-name">{connector.name}</span>
                {#if connector.isActive}<Check size={14} />{/if}
              </button>
            {/each}
          </div>
        {/if}
      </div>

      <div class="conversation-list">
        <div class="recents-label">RECENTS</div>
        <div class="conversation-item active">
          <MessageSquare size={15} />
          <div class="conversation-content">
            <div class="conversation-title">{chatTitle}</div>
            <div class="conversation-preview">
              {#if messages.length > 0}
                {messages[messages.length - 1].content.slice(0, 30)}...
              {:else}
                No messages yet
              {/if}
            </div>
          </div>
        </div>
      </div>

      <div class="sidebar-bottom">
        <div class="user-avatar">{$user?.email?.[0].toUpperCase() || "U"}</div>
        <div class="user-name">
          {$user?.user_metadata?.full_name ||
            $user?.email?.split("@")[0] ||
            "Student"}
        </div>
        <button class="settings-btn" on:click={() => goto("/settings")}>
          <Settings size={16} />
        </button>
      </div>
    </div>

    <div class="main-chat">
      <div class="chat-header-inner">
        <button class="mobile-menu-btn" on:click={toggleMobileSidebar}
          ><Menu size={20} /></button
        >
        <div class="chat-title-text">{activeConnector}</div>
        <div class="header-right-actions">
          <button class="header-btn" on:click={clearChat}
            ><Trash2 size={18} /></button
          >
        </div>
      </div>

      <div class="messages-area">
        {#if messages.length === 0}
          <div class="empty-state">
            <div class="welcome-badge">SYSTEMS ACTIVE</div>
            <div class="greeting">
              {getTimeGreeting()}, {$user?.user_metadata?.full_name?.split(
                " ",
              )[0] || "Scholar"}
            </div>
            <div class="subtitle">
              I've analyzed your current study trajectory. Ready for a
              breakthrough?
            </div>

            <div class="suggestion-grid">
              <button
                class="suggestion-pill"
                on:click={() =>
                  handleSuggestionClick("Summarize my Algorithms notes")}
              >
                <BookMarked size={14} /> Summarize my Algorithms notes
              </button>
              <button
                class="suggestion-pill"
                on:click={() =>
                  handleSuggestionClick("Build a 7-day crunch plan")}
              >
                <Calendar size={14} /> Build a 7-day crunch plan
              </button>
              <button
                class="suggestion-pill"
                on:click={() =>
                  handleSuggestionClick("Quiz me on Big O notation")}
              >
                <Brain size={14} /> Quiz me on Big O notation
              </button>
              <button
                class="suggestion-pill"
                on:click={() =>
                  handleSuggestionClick("Help me with study anxiety")}
              >
                <HeartHandshake size={14} /> Help me with study anxiety
              </button>
            </div>
          </div>
        {:else}
          <div class="messages-container">
            <ChatMessages {messages} />
            {#if isTyping && !messages.some((m) => m.isStreaming)}
              <div class="typing-indicator-wrapper">
                <div class="typing-bubble">
                  <div class="dot"></div>
                  <div class="dot"></div>
                  <div class="dot"></div>
                </div>
              </div>
            {/if}
          </div>
        {/if}
      </div>

      <div class="input-wrapper">
        <div class="input-container-modern">
          <div class="attachment-container">
            <button
              class="attachment-btn"
              on:click|stopPropagation={() =>
                (moreOptionsOpen = !moreOptionsOpen)}><Plus size={20} /></button
            >

            {#if moreOptionsOpen}
              <div
                class="more-options-dropdown"
                role="menu"
                tabindex="-1"
                on:click|stopPropagation
                on:keydown={(e) => e.stopPropagation()}
              >
                <button
                  class="more-option-btn-v2"
                  on:click={() => handleMoreOptionClick("file")}
                >
                  <FileText size={18} /> <span>Upload Document</span>
                </button>
                <button
                  class="more-option-btn-v2"
                  on:click={() => handleMoreOptionClick("camera")}
                >
                  <Camera size={18} /> <span>Scan with Camera</span>
                </button>
                <button
                  class="more-option-btn-v2"
                  on:click={() => handleMoreOptionClick("connector")}
                >
                  <Zap size={18} /> <span>Add AI Connector</span>
                </button>
                <button
                  class="more-option-btn-v2"
                  on:click={() => handleMoreOptionClick("mobile")}
                >
                  <Smartphone size={18} /> <span>Sync Mobile App</span>
                </button>
              </div>
            {/if}
          </div>

          <textarea
            class="modern-input"
            bind:value={inputText}
            placeholder="Ask StudyVault anything..."
            on:keydown={handleKeydown}
            rows="1"
          ></textarea>
          <div class="input-right">
            <button class="voice-btn"><Mic size={18} /></button>
            <button
              class="send-btn-modern"
              class:active={inputText.trim()}
              on:click={sendMessage}
              disabled={!inputText.trim()}
            >
              <ArrowUp size={20} />
            </button>
          </div>
        </div>
        <div class="input-disclaimer">
          StudyVault AI reasoning uses Discrete Agentic Pipelines. No training
          data used.
        </div>
      </div>
    </div>

    {#if contextPanelOpen}
      <div class="context-panel">
        <div class="context-header-inner">
          <div class="section-title-wrapper">
            <span class="section-dot" />
            <span class="section-title-label">Context</span>
          </div>
          <button class="close-btn" on:click={toggleContextPanel}
            ><X size={16} /></button
          >
        </div>

        <div class="context-scroll">
          <div class="context-section">
            <div class="sec-label">Student Profile</div>
            <div class="context-row">
              <span>Style</span> <span class="val">Visual</span>
            </div>
            <div class="context-row">
              <span>Type</span> <span class="val">Achiever</span>
            </div>
          </div>
          <div class="context-section">
            <div class="sec-label">Performance</div>
            <div class="context-row">
              <span>Retention</span> <span class="val">78%</span>
            </div>
            <div class="context-row">
              <span>Streak</span> <span class="val">3 days</span>
            </div>
          </div>
          <div class="context-section">
            <div class="sec-label">Active Subject</div>
            <div class="active-badge">Computer Science 101</div>
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&display=swap");

  :global(body) {
    background: #0a0a0b;
    color: white;
    margin: 0;
    overflow: hidden;
  }

  .page {
    font-family: "Geist", sans-serif;
    display: flex;
    flex-direction: column;
    padding: 24px 32px;
    height: 100vh;
    box-sizing: border-box;
    opacity: 0;
    transition: opacity 0.5s;
  }
  .page.mounted {
    opacity: 1;
  }

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  .header-left {
    display: flex;
    gap: 12px;
    align-items: center;
  }
  .header-icon {
    width: 32px;
    height: 32px;
    background: rgba(163, 230, 53, 0.1);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #a3e635;
  }
  .page-title {
    font-size: 18px;
    font-weight: 700;
    margin: 0;
  }
  .page-sub {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.3);
    margin: 0;
  }
  .header-actions {
    display: flex;
    gap: 10px;
  }

  .ghost-btn {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.5);
    padding: 6px 14px;
    border-radius: 8px;
    font-size: 12px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .accent-btn {
    background: #a3e635;
    color: black;
    border: none;
    padding: 6px 14px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 12px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .divider {
    height: 1px;
    background: rgba(255, 255, 255, 0.05);
    margin-bottom: 24px;
  }

  .main-layout {
    display: grid;
    grid-template-columns: 260px 1fr 280px;
    gap: 20px;
    flex: 1;
    min-height: 0;
  }

  .sidebar {
    background: #0e0e10;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .sidebar-top {
    padding: 20px;
  }
  .logo-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
  }
  .logo-icon {
    width: 28px;
    height: 28px;
    background: #a3e635;
    border-radius: 6px;
    color: black;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 11px;
  }
  .logo-text {
    font-weight: 600;
    font-size: 14px;
  }
  .new-chat-btn {
    width: 100%;
    padding: 10px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 8px;
    color: white;
    font-size: 13px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 16px;
  }

  .connector-chip-sidebar {
    width: 100%;
    padding: 8px 12px;
    background: rgba(163, 230, 53, 0.05);
    border: 1px solid rgba(163, 230, 53, 0.1);
    border-radius: 8px;
    color: #a3e635;
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    font-size: 13px;
  }
  .connector-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }

  .connector-dropdown {
    margin-top: 8px;
    background: #1a1a1c;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  .connector-option {
    width: 100%;
    padding: 8px 12px;
    display: flex;
    align-items: center;
    gap: 10px;
    background: transparent;
    border: none;
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
    font-size: 12px;
    text-align: left;
  }
  .connector-option.active {
    background: rgba(163, 230, 53, 0.1);
    color: #a3e635;
  }
  .option-icon {
    width: 16px;
    text-align: center;
  }

  .conversation-list {
    flex: 1;
    padding: 20px 8px;
    overflow-y: auto;
  }
  .recents-label {
    font-size: 10px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.2);
    letter-spacing: 0.1em;
    margin-bottom: 12px;
    padding: 0 12px;
  }
  .conversation-item {
    padding: 10px 12px;
    border-radius: 8px;
    display: flex;
    gap: 12px;
    color: rgba(255, 255, 255, 0.4);
    cursor: pointer;
    transition: background 0.2s;
  }
  .conversation-item.active {
    background: rgba(255, 255, 255, 0.03);
    color: white;
  }
  .conversation-title {
    font-size: 13px;
    font-weight: 500;
  }
  .conversation-preview {
    font-size: 11px;
    opacity: 0.5;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .sidebar-bottom {
    padding: 16px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .user-avatar {
    width: 28px;
    height: 28px;
    background: #a3e635;
    border-radius: 50%;
    color: black;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 11px;
  }
  .user-name {
    font-size: 12px;
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .main-chat {
    background: #0e0e10;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    position: relative;
  }
  .chat-header-inner {
    height: 56px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    align-items: center;
    padding: 0 20px;
    justify-content: space-between;
    border-radius: 16px 16px 0 0;
    overflow: hidden;
  }
  .chat-title-text {
    font-size: 14px;
    font-weight: 600;
    color: #a3e635;
  }
  .messages-area {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    scroll-behavior: smooth;
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    max-width: 600px;
    margin: 0 auto;
    text-align: center;
  }
  .welcome-badge {
    font-size: 9px;
    font-weight: 800;
    color: #a3e635;
    border: 1px solid rgba(163, 230, 53, 0.2);
    padding: 3px 8px;
    border-radius: 20px;
    margin-bottom: 20px;
    letter-spacing: 0.1em;
  }
  .greeting {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 12px;
    letter-spacing: -0.02em;
  }
  .subtitle {
    font-size: 15px;
    color: rgba(255, 255, 255, 0.4);
    margin-bottom: 40px;
  }
  .suggestion-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    width: 100%;
  }
  .suggestion-pill {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 12px;
    border-radius: 12px;
    color: white;
    font-size: 13px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
    transition: all 0.2s;
  }
  .suggestion-pill:hover {
    border-color: rgba(163, 230, 53, 0.3);
    background: rgba(163, 230, 53, 0.02);
  }

  .input-wrapper {
    padding: 20px 40px 40px;
  }
  .input-container-modern {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 10px 12px 10px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    position: relative;
  }
  .modern-input {
    flex: 1;
    background: transparent;
    border: none;
    color: white;
    resize: none;
    font-family: inherit;
    font-size: 14px;
    max-height: 150px;
  }
  .modern-input:focus {
    outline: none;
  }
  .send-btn-modern {
    width: 36px;
    height: 36px;
    background: rgba(255, 255, 255, 0.05);
    border: none;
    border-radius: 10px;
    color: rgba(255, 255, 255, 0.2);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .send-btn-modern.active {
    background: #a3e635;
    color: black;
    box-shadow: 0 0 15px rgba(163, 230, 53, 0.3);
  }

  .attachment-container {
    position: relative;
  }
  .more-options-dropdown {
    position: absolute;
    bottom: calc(100% + 12px);
    left: 0;
    background: #1a1a1c;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    width: 200px;
    padding: 8px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    z-index: 100;
  }
  .more-option-btn-v2 {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    background: transparent;
    border: none;
    color: rgba(255, 255, 255, 0.7);
    font-size: 13px;
    cursor: pointer;
    border-radius: 8px;
    transition: all 0.2s;
  }
  .more-option-btn-v2:hover {
    background: rgba(255, 255, 255, 0.05);
    color: white;
  }

  .context-panel {
    background: #0e0e10;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    display: flex;
    flex-direction: column;
  }
  .context-header-inner {
    padding: 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .section-title-wrapper {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .section-dot {
    width: 6px;
    height: 6px;
    background: #a3e635;
    border-radius: 50%;
    box-shadow: 0 0 8px #a3e635;
  }
  .section-title-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.3);
  }
  .context-scroll {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }
  .sec-label {
    font-size: 10px;
    font-weight: 800;
    color: rgba(255, 255, 255, 0.2);
    text-transform: uppercase;
    margin-bottom: 12px;
  }
  .context-row {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.5);
    padding: 4px 0;
  }
  .val {
    color: rgba(255, 255, 255, 0.9);
    font-weight: 600;
  }
  .active-badge {
    background: rgba(163, 230, 53, 0.1);
    border: 1px solid rgba(163, 230, 53, 0.2);
    padding: 8px;
    border-radius: 8px;
    color: #a3e635;
    font-size: 12px;
    font-weight: 600;
    text-align: center;
  }

  .loading-overlay {
    position: fixed;
    inset: 0;
    background: #0a0a0b;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .loading-inner {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    text-align: center;
  }
  .loading-text {
    font-size: 18px;
    font-weight: 700;
    color: white;
    margin: 0;
  }
  .loading-status {
    font-size: 10px;
    color: #a3e635;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }
  .loading-bar {
    width: 150px;
    height: 2px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 2px;
    overflow: hidden;
  }
  .loading-fill {
    height: 100%;
    background: #a3e635;
    width: 0;
    animation: load 0.8s ease-in-out forwards;
  }
  @keyframes load {
    to {
      width: 100%;
    }
  }

  .background-glow {
    position: absolute;
    width: 400px;
    height: 400px;
    background: radial-gradient(
      circle,
      rgba(163, 230, 53, 0.1) 0%,
      transparent 70%
    );
    border-radius: 50%;
    filter: blur(50px);
    pointer-events: none;
  }

  @media (max-width: 1024px) {
    .main-layout {
      grid-template-columns: 1fr;
    }
    .sidebar,
    .context-panel {
      display: none;
    }
  }
</style>
