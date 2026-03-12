<script lang="ts">
  import { onMount, onDestroy, tick } from "svelte";
  import { goto } from "$app/navigation";
  import { chatStore } from "$lib/stores/chatStore";
  import { processMessage } from "$lib/chatbot/cleanChatbot";
  import {
    Plus, MessageSquare, Trash2, Send, Zap, Bot,
    User, Copy, ThumbsUp, ThumbsDown, RefreshCw,
    BookOpen, Calendar, Brain, BarChart2, Check,
    Loader2, ChevronDown, X, Menu, Sparkles,
    GraduationCap
  } from "lucide-svelte";

  // ── State ──────────────────────────────────────
  let mounted = false;
  let loading = true;
  let inputText = "";
  let isTyping = false;
  let messagesEl: HTMLElement;
  let inputEl: HTMLTextAreaElement;
  let sidebarOpen = false;
  let copiedId = "";

  const { currentChat } = chatStore;
  $: messages = $currentChat?.messages || [];
  $: conversations = $chatStore?.conversations || [];
  $: currentChatId = $chatStore?.currentChatId;

  const suggestions = [
    { icon: BookOpen, text: "Create a study plan for my exam next week" },
    { icon: Brain,    text: "Explain machine learning with simple examples" },
    { icon: Calendar, text: "Schedule my study sessions for today" },
    { icon: BarChart2,text: "Analyze my weak areas and suggest resources" },
  ];

  async function sendMessage() {
    if (!inputText.trim() || isTyping) return;
    const text = inputText.trim();
    inputText = "";
    await tick();
    resizeTextarea();
    isTyping = true;
    scrollToBottom();

    try {
      await processMessage({
        input: text,
        conversationId: "current",
        connectorId: "studyvault",
        profile: null,
        onChunk: () => scrollToBottom(),
        onComplete: () => { isTyping = false; scrollToBottom(); },
        onError: () => { isTyping = false; },
      });
    } catch {
      isTyping = false;
    }
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  function resizeTextarea() {
    if (!inputEl) return;
    inputEl.style.height = "auto";
    inputEl.style.height = Math.min(inputEl.scrollHeight, 160) + "px";
  }

  async function scrollToBottom() {
    await tick();
    if (messagesEl) {
      messagesEl.scrollTop = messagesEl.scrollHeight;
    }
  }

  function copyMessage(content: string, id: string) {
    navigator.clipboard.writeText(content);
    copiedId = id;
    setTimeout(() => (copiedId = ""), 2000);
  }

  function useSuggestion(text: string) {
    inputText = text;
    sendMessage();
  }

  function formatTime(ts: number) {
    return new Date(ts).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  function renderContent(content: string): string {
    return content
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.*?)\*/g, "<em>$1</em>")
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/\n/g, "<br>");
  }

  function truncateTitle(title: string) {
    return title.length > 28 ? title.slice(0, 28) + "…" : title;
  }

  $: if (messages.length) scrollToBottom();

  onMount(async () => {
    await chatStore.initializeWithoutAuth();
    setTimeout(() => { loading = false; mounted = true; }, 600);
  });
</script>

<svelte:head><title>AI Chat — StudyVault</title></svelte:head>

{#if loading}
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-[#0A0A0B]">
    <div class="flex flex-col items-center gap-4">
      <div class="w-14 h-14 rounded-2xl bg-[#a3e635]/10 border border-[#a3e635]/20 flex items-center justify-center animate-pulse">
        <Zap size={28} fill="#a3e635" color="#a3e635" />
      </div>
      <p class="text-[#a3e635] font-semibold tracking-wide text-sm">StudyVault AI</p>
      <div class="w-40 h-0.5 bg-[#1e1e22] rounded-full overflow-hidden">
        <div class="h-full bg-[#a3e635] rounded-full animate-[loading-bar_1.2s_ease-in-out_infinite]" style="width:60%"></div>
      </div>
    </div>
  </div>
{/if}

<div class="flex h-[calc(100vh-0px)] bg-[#0A0A0B] overflow-hidden" class:opacity-0={!mounted} style="transition: opacity 0.4s ease">

  <!-- ── Sidebar ── -->
  <div
    class="flex flex-col border-r border-white/[0.06] transition-all duration-300 bg-[#0d0d10]"
    class:w-64={sidebarOpen}
    class:w-14={!sidebarOpen}
  >
    <!-- Sidebar toggle -->
    <div class="flex items-center gap-2 p-3 border-b border-white/[0.06]">
      <button
        class="w-8 h-8 flex items-center justify-center rounded-lg text-white/40 hover:text-white/80 hover:bg-white/[0.06] transition-colors"
        on:click={() => sidebarOpen = !sidebarOpen}
      >
        <Menu size={16} />
      </button>
      {#if sidebarOpen}
        <div class="flex items-center gap-2 overflow-hidden">
          <div class="w-5 h-5 rounded bg-[#a3e635] flex items-center justify-center flex-shrink-0">
            <GraduationCap size={11} color="#0A0A0B" />
          </div>
          <span class="text-sm font-semibold text-white/90 whitespace-nowrap">StudyVault AI</span>
        </div>
      {/if}
    </div>

    <!-- New Chat -->
    <div class="p-2">
      <button
        class="flex items-center gap-2 w-full rounded-lg px-2 py-2 text-white/60 hover:text-white/90 hover:bg-white/[0.06] transition-colors text-sm"
        on:click={() => chatStore.newChat()}
        title="New Chat"
      >
        <Plus size={16} class="flex-shrink-0" />
        {#if sidebarOpen}<span>New Chat</span>{/if}
      </button>
    </div>

    <!-- Conversations list -->
    {#if sidebarOpen}
      <div class="flex-1 overflow-y-auto px-2 py-1 flex flex-col gap-0.5">
        {#if conversations.length === 0}
          <p class="text-white/25 text-xs px-2 py-2">No conversations yet</p>
        {:else}
          {#each conversations as conv}
            <button
              class="w-full text-left px-2 py-2 rounded-lg text-xs transition-colors group flex items-center gap-2 {conv.id === currentChatId ? 'bg-white/10 text-white/90' : 'text-white/50 hover:bg-white/5'}"
              on:click={() => chatStore.setCurrentChat(conv.id)}
            >
              <MessageSquare size={12} class="flex-shrink-0 opacity-60" />
              <span class="truncate flex-1">{truncateTitle(conv.title)}</span>
            </button>
          {/each}
        {/if}
      </div>
    {:else}
      <div class="flex-1 overflow-y-auto flex flex-col items-center gap-1 py-2">
        {#each conversations.slice(0, 6) as conv}
          <button
            class="w-8 h-8 flex items-center justify-center rounded-lg transition-colors {conv.id === currentChatId ? 'bg-white/10 text-lime-400' : 'text-white/30 hover:bg-white/5'}"
            on:click={() => chatStore.setCurrentChat(conv.id)}
            title={conv.title}
          >
            <MessageSquare size={13} />
          </button>
        {/each}
      </div>
    {/if}
  </div>

  <!-- ── Main Chat Area ── -->
  <div class="flex-1 flex flex-col min-w-0">

    <!-- Top bar -->
    <div class="flex items-center justify-between px-5 py-3 border-b border-white/[0.06]">
      <div class="flex items-center gap-3">
        <div class="flex items-center gap-2">
          <div class="w-7 h-7 rounded-lg bg-[#a3e635]/10 border border-[#a3e635]/20 flex items-center justify-center">
            <Sparkles size={13} color="#a3e635" />
          </div>
          <div>
            <p class="text-sm font-semibold text-white/90 leading-none">StudyVault AI</p>
            <p class="text-[10px] text-[#a3e635] mt-0.5">Online · Classical AI Pipeline</p>
          </div>
        </div>
      </div>
      <button
        class="text-xs text-white/30 hover:text-white/60 flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg hover:bg-white/[0.05] transition-colors"
        on:click={() => chatStore.clearChat()}
      >
        <Trash2 size={12} />
        Clear
      </button>
    </div>

    <!-- Messages area -->
    <div class="flex-1 overflow-y-auto" bind:this={messagesEl}>
      {#if messages.length === 0}
        <!-- Empty state -->
        <div class="flex flex-col items-center justify-center h-full px-6 py-12">
          <div class="w-16 h-16 rounded-2xl bg-[#a3e635]/8 border border-[#a3e635]/15 flex items-center justify-center mb-5">
            <Bot size={30} color="#a3e635" opacity="0.8" />
          </div>
          <h2 class="text-xl font-bold text-white/90 mb-1.5">How can I help you study?</h2>
          <p class="text-sm text-white/40 text-center max-w-sm mb-8">
            I use classical AI algorithms — fuzzy logic, Dempster-Shafer, HTN planning — to give you personalized academic support.
          </p>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 w-full max-w-xl">
            {#each suggestions as s}
              <button
                class="flex items-center gap-3 px-4 py-3 rounded-xl border border-white/[0.07] bg-white/[0.02] hover:bg-white/[0.05] hover:border-white/[0.12] transition-all text-left group"
                on:click={() => useSuggestion(s.text)}
              >
                <div class="w-7 h-7 rounded-lg bg-[#a3e635]/10 flex items-center justify-center flex-shrink-0 group-hover:bg-[#a3e635]/20 transition-colors">
                  <svelte:component this={s.icon} size={14} color="#a3e635" />
                </div>
                <span class="text-xs text-white/60 group-hover:text-white/80 transition-colors leading-relaxed">{s.text}</span>
              </button>
            {/each}
          </div>
        </div>
      {:else}
        <div class="max-w-3xl mx-auto px-4 py-6 flex flex-col gap-6">
          {#each messages as msg (msg.id)}
            {#if msg.role === 'user'}
              <!-- User message -->
              <div class="flex justify-end">
                <div class="flex items-end gap-2.5 max-w-[75%]">
                  <div class="flex flex-col items-end gap-1">
                    <div class="bg-[#a3e635]/12 border border-[#a3e635]/20 rounded-2xl rounded-br-md px-4 py-3 text-sm text-white/90 leading-relaxed">
                      {msg.content}
                    </div>
                    <span class="text-[10px] text-white/20">{formatTime(msg.timestamp)}</span>
                  </div>
                  <div class="w-7 h-7 rounded-full bg-white/10 border border-white/10 flex items-center justify-center flex-shrink-0 mb-5">
                    <User size={13} color="rgba(255,255,255,0.6)" />
                  </div>
                </div>
              </div>
            {:else if msg.role === 'assistant'}
              <!-- Assistant message -->
              <div class="flex gap-2.5">
                <div class="w-7 h-7 rounded-full bg-[#a3e635]/15 border border-[#a3e635]/25 flex items-center justify-center flex-shrink-0 mt-1">
                  <Zap size={13} fill="#a3e635" color="#a3e635" />
                </div>
                <div class="flex-1 min-w-0">
                  <div class="rounded-2xl rounded-tl-md px-4 py-3 bg-[#111114] border border-white/[0.06] text-sm text-white/85 leading-relaxed">
                    {#if msg.isStreaming && !msg.content}
                      <div class="flex items-center gap-1.5 py-1">
                        <span class="w-1.5 h-1.5 rounded-full bg-[#a3e635]/70 animate-bounce" style="animation-delay:0ms"></span>
                        <span class="w-1.5 h-1.5 rounded-full bg-[#a3e635]/70 animate-bounce" style="animation-delay:150ms"></span>
                        <span class="w-1.5 h-1.5 rounded-full bg-[#a3e635]/70 animate-bounce" style="animation-delay:300ms"></span>
                      </div>
                    {:else}
                      {@html renderContent(msg.content)}
                      {#if msg.isStreaming}
                        <span class="inline-block w-0.5 h-4 bg-[#a3e635] ml-0.5 animate-pulse align-middle"></span>
                      {/if}
                    {/if}
                  </div>
                  {#if !msg.isStreaming}
                    <div class="flex items-center gap-1 mt-1.5 ml-1">
                      <span class="text-[10px] text-white/20 mr-1">{formatTime(msg.timestamp)}</span>
                      <button
                        class="w-6 h-6 flex items-center justify-center rounded-md text-white/25 hover:text-white/60 hover:bg-white/[0.06] transition-colors"
                        on:click={() => copyMessage(msg.content, msg.id)}
                        title="Copy"
                      >
                        {#if copiedId === msg.id}
                          <Check size={11} color="#a3e635" />
                        {:else}
                          <Copy size={11} />
                        {/if}
                      </button>
                      <button class="w-6 h-6 flex items-center justify-center rounded-md text-white/25 hover:text-white/60 hover:bg-white/[0.06] transition-colors" title="Good response">
                        <ThumbsUp size={11} />
                      </button>
                      <button class="w-6 h-6 flex items-center justify-center rounded-md text-white/25 hover:text-white/60 hover:bg-white/[0.06] transition-colors" title="Bad response">
                        <ThumbsDown size={11} />
                      </button>
                    </div>
                  {/if}
                </div>
              </div>
            {/if}
          {/each}

          {#if isTyping && messages[messages.length-1]?.role !== 'assistant'}
            <div class="flex gap-2.5">
              <div class="w-7 h-7 rounded-full bg-[#a3e635]/15 border border-[#a3e635]/25 flex items-center justify-center flex-shrink-0">
                <Zap size={13} fill="#a3e635" color="#a3e635" />
              </div>
              <div class="bg-[#111114] border border-white/[0.06] rounded-2xl rounded-tl-md px-4 py-3">
                <div class="flex items-center gap-1.5">
                  <span class="w-1.5 h-1.5 rounded-full bg-[#a3e635]/70 animate-bounce" style="animation-delay:0ms"></span>
                  <span class="w-1.5 h-1.5 rounded-full bg-[#a3e635]/70 animate-bounce" style="animation-delay:150ms"></span>
                  <span class="w-1.5 h-1.5 rounded-full bg-[#a3e635]/70 animate-bounce" style="animation-delay:300ms"></span>
                </div>
              </div>
            </div>
          {/if}
        </div>
      {/if}
    </div>

    <!-- Input area -->
    <div class="border-t border-white/[0.06] px-4 py-3">
      <div class="max-w-3xl mx-auto">
        <div class="flex items-end gap-2.5 bg-[#111114] border border-white/[0.08] rounded-2xl px-4 py-3 focus-within:border-[#a3e635]/30 transition-colors">
          <textarea
            bind:this={inputEl}
            bind:value={inputText}
            on:keydown={handleKeydown}
            on:input={resizeTextarea}
            placeholder="Ask anything about your studies…"
            rows="1"
            disabled={isTyping}
            class="flex-1 bg-transparent text-sm text-white/90 placeholder-white/25 resize-none outline-none leading-relaxed max-h-40 disabled:opacity-50"
            style="scrollbar-width:none"
          ></textarea>
          <button
            on:click={sendMessage}
            disabled={!inputText.trim() || isTyping}
            class="w-8 h-8 flex items-center justify-center rounded-xl transition-all flex-shrink-0 mb-0.5 {inputText.trim() && !isTyping ? 'send-active' : 'opacity-30 bg-white/10'}"
          >
            {#if isTyping}
              <Loader2 size={15} color={inputText.trim() ? "#0A0A0B" : "rgba(255,255,255,0.4)"} class="animate-spin" />
            {:else}
              <Send size={15} color={inputText.trim() ? "#0A0A0B" : "rgba(255,255,255,0.4)"} />
            {/if}
          </button>
        </div>
        <p class="text-center text-[10px] text-white/15 mt-2">Powered by classical AI — fuzzy logic · Dempster-Shafer · HTN planning</p>
      </div>
    </div>
  </div>
</div>

<style>
  :global(.send-active) {
    background-color: #a3e635;
  }
  :global(code) {
    background: rgba(163,230,53,0.1);
    color: #a3e635;
    padding: 1px 5px;
    border-radius: 4px;
    font-size: 0.8em;
    font-family: 'JetBrains Mono', monospace;
  }
  textarea::-webkit-scrollbar { display: none; }

  @keyframes loading-bar {
    0%   { transform: translateX(-100%); }
    100% { transform: translateX(200%); }
  }
</style>
