<script lang="ts">
  import { onMount } from 'svelte';
  import '$lib/../app.css';
  import { 
    BookOpen, Calendar, Zap, BarChart2,
    Scan, CalendarPlus, Brain, HeartHandshake,
    Plus, MessageSquare, Settings, Trash2,
    PanelRight, Menu, User, BookMarked,
    TrendingUp, X, Camera, Paperclip,
    ArrowUp, Copy, ThumbsUp, ThumbsDown,
    ChevronDown, Check, Mic, Share2
  } from 'lucide-svelte';

  // Simple demo without complex store initialization
  type Message = {
    id: string;
    role: 'assistant' | 'user';
    content: string;
    timestamp: number;
    isStreaming: boolean;
    icons?: Record<string, any>;
  };

  let messages: Message[] = [
    {
      id: '1',
      role: 'assistant',
      content: 'Hi! I\'m StudyVault AI, your intelligent study assistant. I can help you with:\n\n**Study Help** - Explain concepts and suggest learning strategies\n**Scheduling** - Create personalized study schedules\n**Motivation** - Keep you motivated and on track\n**Progress Tracking** - Monitor your learning progress\n\nI use advanced AI algorithms (CSP emotion detection, BFS/DFS intent search, Q-learning) to provide personalized help. Feel free to ask me anything!',
      timestamp: Date.now(),
      isStreaming: false,
      icons: {
        'Study Help': BookOpen,
        'Scheduling': Calendar,
        'Motivation': Zap,
        'Progress Tracking': BarChart2
      }
    }
  ];

  let inputText = '';
  let isTyping = false;
  let mobileSidebarOpen = false;
  let contextPanelOpen = true;
  let activeConnector = 'StudyVault AI';
  let connectorDropdownOpen = false;
  let moreOptionsOpen = false;

  const connectors = [
    { id: 'studyvault-ai', name: 'StudyVault AI', color: '#C8FF00', category: 'ai', isConnected: true, isActive: true, icon: 'SV' },
    { id: 'claude', name: 'Claude', color: '#FF6B35', category: 'ai', isConnected: false, isActive: false, icon: '◆' },
    { id: 'chatgpt', name: 'ChatGPT', color: '#10A37F', category: 'ai', isConnected: false, isActive: false, icon: '●' },
    { id: 'gemini', name: 'Gemini', color: '#4285F4', category: 'ai', isConnected: false, isActive: false, icon: '✦' },
    { id: 'perplexity', name: 'Perplexity', color: '#5D6AFF', category: 'ai', isConnected: false, isActive: false, icon: '⚡' },
    { id: 'notebooklm', name: 'NotebookLM', color: '#4285F4', category: 'ai', isConnected: false, isActive: false, icon: '📚' },
    { id: 'obsidian', name: 'Obsidian', color: '#7C3AED', category: 'note', isConnected: false, isActive: false, icon: '💎' },
    { id: 'notion', name: 'Notion', color: '#000000', category: 'note', isConnected: false, isActive: false, icon: '📋' },
    { id: 'evernote', name: 'Evernote', color: '#00A82D', category: 'note', isConnected: false, isActive: false, icon: '🐘' },
    { id: 'onenote', name: 'OneNote', color: '#7719AA', category: 'note', isConnected: false, isActive: false, icon: '📓' },
    { id: 'roam-research', name: 'Roam Research', color: '#C6538C', category: 'note', isConnected: false, isActive: false, icon: '🕸️' },
    { id: 'logseq', name: 'Logseq', color: '#04B182', category: 'note', isConnected: false, isActive: false, icon: '🌿' },
    { id: 'remnote', name: 'RemNote', color: '#FF6B35', category: 'note', isConnected: false, isActive: false, icon: '🧠' },
    { id: 'craft', name: 'Craft', color: '#007AFF', category: 'note', isConnected: false, isActive: false, icon: '🎨' }
  ];

  async function sendMessage() {
    if (!inputText.trim() || isTyping) return;

    const userMessage = {
      id: Date.now().toString(),
      role: 'user' as const,
      content: inputText,
      timestamp: Date.now(),
      isStreaming: false
    };

    messages = [...messages, userMessage];
    inputText = '';
    isTyping = true;

    // Simulate AI response
    setTimeout(() => {
      const aiResponse = {
        id: (Date.now() + 1).toString(),
        role: 'assistant' as const,
        content: generateDemoResponse(userMessage.content),
        timestamp: Date.now(),
        isStreaming: false
      };
      messages = [...messages, aiResponse];
      isTyping = false;
    }, 1500);
  }

  function generateDemoResponse(userInput: string): string {
    const input = userInput.toLowerCase();
    
    if (activeConnector === 'NotebookLM') {
      return `I'm connected to NotebookLM! I can help you:\n\n📚 **Analyze documents** - Upload PDFs, articles, or notes\n🔍 **Answer questions** about your sources\n📝 **Generate summaries** from multiple documents\n🔗 **Connect concepts** across different materials\n\nNotebookLM uses Google's AI to provide source-grounded responses. What would you like to explore with your documents?`;
    }
    
    if (activeConnector === 'Obsidian') {
      return `Connected to Obsidian! I can help you:\n\n🧠 **Link notes** using bidirectional linking\n📊 **Create knowledge graphs** from your vault\n🔍 **Search across all notes** instantly\n📝 **Generate templates** for different note types\n\nObsidian excels at building a personal knowledge base. What aspect of your second brain would you like to work on?`;
    }
    
    if (activeConnector === 'Notion') {
      return `Notion integration active! I can assist with:\n\n📊 **Database management** - organize your data\n📝 **Document creation** with rich formatting\n🔗 **Page linking** and workspace organization\n📋 **Task tracking** and project management\n\nNotion combines notes, tasks, and databases. What would you like to build or organize?`;
    }
    
    if (activeConnector === 'Evernote') {
      return `Evernote connected! I can help you:\n\n📝 **Note organization** with notebooks and tags\n🔍 **Advanced search** across all notes\n📎 **Web clipping** and content saving\n📊 **Document scanning** with OCR\n\nEvernote is great for capturing and organizing information. What would you like to note today?`;
    }
    
    if (activeConnector === 'OneNote') {
      return `Microsoft OneNote integration! I can assist with:\n\n📓 **Free-form note-taking** on infinite canvas\n🗂️ **Notebook organization** with sections and pages\n✏️ **Handwriting recognition** and drawing tools\n🔗 **Integration** with Office 365 apps\n\nOneNote offers flexible note-taking. What would you like to capture or organize?`;
    }
    
    if (activeConnector === 'Roam Research') {
      return `Roam Research connected! I can help you:\n\n🕸️ **Build knowledge networks** with bidirectional links\n📊 **Daily notes** and spaced repetition\n🔍 **Graph database** queries and insights\n💡 **Idea generation** from connected thoughts\n\nRoam excels at connecting ideas. What network of thoughts would you like to explore?`;
    }
    
    if (activeConnector === 'Logseq') {
      return `Logseq integration active! I can assist with:\n\n🧠 **Local-first knowledge management**\n🔗 **Bi-directional linking** and backlinks\n📅 **Daily journaling** and task tracking\n🔒 **Privacy-focused** note-taking\n\nLogseq puts you in control of your data. What knowledge would you like to build?`;
    }
    
    if (activeConnector === 'RemNote') {
      return `RemNote connected! I can help you:\n\n🧠 **Spaced repetition** learning\n📝 **Hierarchical note-taking** with bullets\n🔗 **Reference management** and citations\n💡 **Flashcard creation** from notes\n\nRemNote combines note-taking with learning. What would you like to remember?`;
    }
    
    if (activeConnector === 'Craft') {
      return `Craft integration ready! I can help with:\n\n📝 **Beautiful document creation**\n🎨 **Rich media embedding** and design\n👥 **Collaborative editing** in real-time\n📊 **Data visualization** and tables\n\nCraft focuses on visual, collaborative documents. What would you like to create?`;
    }
    
    if (input.includes('help') || input.includes('explain') || input.includes('understand')) {
      return 'I can definitely help you with that! Based on your visual learning style, I\'d recommend using diagrams and visual examples. What specific concept are you struggling with?';
    }
    
    if (input.includes('schedule') || input.includes('plan') || input.includes('study')) {
      return 'Let me help you create a study schedule! With 21 days until your exam and your current progress in Algorithms, I\'d suggest:\n\n**Today**: Review Algorithms (45min)\n**Tomorrow**: Practice Problems (60min)\n**Day 3**: Start Complexity Analysis (30min)\n\nWould you like me to create a detailed weekly schedule?';
    }
    
    if (input.includes('anxious') || input.includes('worried') || input.includes('nervous')) {
      return 'I understand you\'re feeling anxious - that\'s completely normal! You\'ve been doing great with a 78% retention rate and a 3-day streak. Let\'s break this down into small, manageable steps. You\'ve got this!';
    }
    
    if (input.includes('confused') || input.includes('don\'t understand')) {
      return 'It\'s okay to feel confused! That\'s actually part of the learning process. Let me try explaining this differently. Since you\'re a visual learner, let me use an analogy...';
    }
    
    return `That's a great question! I'm currently connected to ${activeConnector}. Based on your learning profile and current progress, I'd suggest focusing on your weak areas first. You're doing well with Data Structures (mastered!) but could use more practice with Algorithms. How can I help you specifically?`;
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
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
    messages = [];
  }

  function getTimeGreeting() {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 18) return 'Good afternoon';
    return 'Good evening';
  }

  function renderMessageContent(content: string, icons?: Record<string, any>) {
    if (!icons) return content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
    
    let processed = content;
    const parts = content.split('\n');
    
    return parts.map(part => {
      if (part.includes('**Study Help**')) {
        return `<div class="message-line"><BookOpen size={16} style="display: inline-block; margin-right: 8px; vertical-align: middle;" /> <strong>Study Help</strong> - Explain concepts and suggest learning strategies</div>`;
      }
      if (part.includes('**Scheduling**')) {
        return `<div class="message-line"><Calendar size={16} style="display: inline-block; margin-right: 8px; vertical-align: middle;" /> <strong>Scheduling</strong> - Create personalized study schedules</div>`;
      }
      if (part.includes('**Motivation**')) {
        return `<div class="message-line"><Zap size={16} style="display: inline-block; margin-right: 8px; vertical-align: middle;" /> <strong>Motivation</strong> - Keep you motivated and on track</div>`;
      }
      if (part.includes('**Progress Tracking**')) {
        return `<div class="message-line"><BarChart2 size={16} style="display: inline-block; margin-right: 8px; vertical-align: middle;" /> <strong>Progress Tracking</strong> - Monitor your learning progress</div>`;
      }
      return part.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    }).join('<br>');
  }

  function handleSuggestionClick(suggestion: string) {
    inputText = suggestion;
    sendMessage();
  }

  function selectConnector(connectorId: string) {
    // Update all connectors
    connectors.forEach(c => {
      c.isActive = c.id === connectorId;
    });
    
    activeConnector = connectors.find(c => c.id === connectorId)?.name || 'StudyVault AI';
    connectorDropdownOpen = false;
  }

  function closeAllDropdowns() {
    connectorDropdownOpen = false;
    moreOptionsOpen = false;
  }

  function toggleConnectorDropdown() {
    connectorDropdownOpen = !connectorDropdownOpen;
    moreOptionsOpen = false; // Close more options when opening connector dropdown
  }

  function toggleMoreOptions() {
    moreOptionsOpen = !moreOptionsOpen;
    connectorDropdownOpen = false; // Close connector dropdown when opening more options
  }

  function handleMoreOptionClick(action: string) {
    moreOptionsOpen = false;
    
    switch (action) {
      case 'import-file':
        // Handle file import
        console.log('Import file clicked');
        break;
      case 'take-photo':
        // Handle camera
        console.log('Take photo clicked');
        break;
      case 'add-connector':
        // Navigate to settings/connectors
        window.location.href = '/settings/connectors';
        break;
      case 'voice-record':
        // Handle voice recording
        console.log('Voice record clicked');
        break;
      case 'share-context':
        // Handle context sharing
        console.log('Share context clicked');
        break;
    }
  }
</script>

<svelte:head>
  <title>StudyVault AI</title>
</svelte:head>

<svelte:window on:click={closeAllDropdowns} />

<div class="claude-layout" role="application" on:click|stopPropagation on:keydown={handleKeydown}>
  <!-- Left Sidebar -->
  <div class="sidebar" class:mobile-open={mobileSidebarOpen}>
    <div class="sidebar-top">
      <div class="logo-row">
        <div class="logo-icon">SV</div>
        <span class="logo-text">StudyVault AI</span>
      </div>
      
      <button class="new-chat-btn" on:click={clearChat}>
      <Plus size={16} />
      <span>New Chat</span>
    </button>
      
      <button class="connector-chip" on:click={toggleConnectorDropdown} tabindex="0">
        <div class="connector-dot" style="background: {connectors.find(c => c.isActive)?.color || '#C8FF00'}"></div>
        <span class="connector-name">{connectors.find(c => c.isActive)?.name || 'StudyVault AI'}</span>
        <ChevronDown size={14} class="connector-dropdown-arrow" />
      </button>
      
      {#if connectorDropdownOpen}
        <button class="connector-dropdown" role="menu" on:click|stopPropagation on:keydown={handleKeydown}>
          {#each connectors as connector}
            <button 
              class="connector-option" 
              class:active={connector.isActive}
              class:connected={connector.isConnected}
              on:click={() => selectConnector(connector.id)}
              role="menuitem"
              tabindex="0"
            >
              <div class="connector-option-icon" style="color: {connector.color}">
                {connector.icon}
              </div>
              <div class="connector-option-info">
                <span class="connector-option-name">{connector.name}</span>
                {#if !connector.isConnected}
                  <span class="connector-option-status">Connect →</span>
                {:else if connector.category === 'ai'}
                  <span class="connector-option-model">AI Model</span>
                {:else}
                  <span class="connector-option-model">Note App</span>
                {/if}
              </div>
              {#if connector.isActive}
                <Check size={14} />
              {/if}
            </button>
          {/each}
        </button>
      {/if}
    </div>

    <div class="conversation-list">
      <div class="recents-label">RECENTS</div>
      <div class="conversation-item active">
        <MessageSquare size={15} />
        <div class="conversation-content">
          <div class="conversation-title">Demo Conversation</div>
          <div class="conversation-preview">StudyVault AI: Hi! I'm your...</div>
        </div>
      </div>
    </div>

    <div class="sidebar-bottom">
      <div class="user-avatar">U</div>
      <div class="user-name">Demo User</div>
      <button class="settings-btn">
        <Settings size={16} />
      </button>
    </div>
  </div>

  <!-- Mobile Backdrop -->
  {#if mobileSidebarOpen}
    <button class="mobile-backdrop" on:click={toggleMobileSidebar} on:keydown={handleKeydown} aria-label="Close sidebar"></button>
  {/if}

  <!-- Main Chat Area -->
  <div class="main-chat">
    <!-- Header -->
    <div class="chat-header">
      <button class="mobile-menu-btn" on:click={toggleMobileSidebar}>
      <Menu size={20} />
    </button>
      <div class="chat-title">Demo Conversation</div>
      <div class="header-center">
        <div class="connector-chip">
          <div class="connector-dot" style="background: {connectors.find(c => c.isActive)?.color || '#C8FF00'}"></div>
          <span class="connector-name">{connectors.find(c => c.isActive)?.name || 'StudyVault AI'}</span>
        </div>
      </div>
      <div class="header-right">
        <button class="header-btn" on:click={toggleContextPanel}>
          <PanelRight size={18} />
        </button>
        <button class="header-btn" on:click={clearChat}>
          <Trash2 size={18} />
        </button>
      </div>
    </div>

    <!-- Messages Area -->
    <div class="messages-area">
      {#if messages.length === 0}
        <!-- Empty State -->
        <div class="empty-state">
          <div class="greeting">{getTimeGreeting()}</div>
          <div class="subtitle">How can I help you study today?</div>
          <div class="suggestion-cards">
            <button class="suggestion-card" on:click={() => handleSuggestionClick('Scan my syllabus')} on:keydown={handleKeydown}>
              <Scan size={18} />
              <div class="card-title">Scan my syllabus</div>
              <div class="card-description">Point camera at your syllabus</div>
            </button>
            <button class="suggestion-card" on:click={() => handleSuggestionClick('Build a study schedule')} on:keydown={handleKeydown}>
              <CalendarPlus size={18} />
              <div class="card-title">Build a study schedule</div>
              <div class="card-description">Tell me your exam date</div>
            </button>
            <button class="suggestion-card" on:click={() => handleSuggestionClick('Explain a topic')} on:keydown={handleKeydown}>
              <Brain size={18} />
              <div class="card-title">Explain a topic</div>
              <div class="card-description">Help me understand anything</div>
            </button>
            <button class="suggestion-card" on:click={() => handleSuggestionClick('Feeling overwhelmed')} on:keydown={handleKeydown}>
              <HeartHandshake size={18} />
              <div class="card-title">Feeling overwhelmed</div>
              <div class="card-description">Let us make a plan together</div>
            </button>
          </div>
        </div>
      {:else}
        <!-- Messages -->
        <div class="messages-container">
          {#each messages as message (message.id)}
            <div class="message-group" class:user-message={message.role === 'user'}>
              {#if message.role === 'assistant'}
                <div class="message-avatar">SV</div>
                <div class="message-content">
                  <div class="message-text">
                    {#if message.id === '1'}
                      <div class="message-line"><BookOpen size={16} /> <strong>Study Help</strong> - Explain concepts and suggest learning strategies</div>
                      <div class="message-line"><Calendar size={16} /> <strong>Scheduling</strong> - Create personalized study schedules</div>
                      <div class="message-line"><Zap size={16} /> <strong>Motivation</strong> - Keep you motivated and on track</div>
                      <div class="message-line"><BarChart2 size={16} /> <strong>Progress Tracking</strong> - Monitor your learning progress</div>
                      <br>
                      I use advanced AI algorithms (CSP emotion detection, BFS/DFS intent search, Q-learning) to provide personalized help. Feel free to ask me anything!
                    {:else}
                      {@html message.content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>')}
                    {/if}
                  </div>
                  <div class="message-actions">
                    <button class="action-btn">
                      <Copy size={14} />
                    </button>
                    <button class="action-btn">
                      <ThumbsUp size={14} />
                    </button>
                    <button class="action-btn">
                      <ThumbsDown size={14} />
                    </button>
                  </div>
                </div>
              {:else}
                <div class="user-message">
                  <div class="user-bubble">
                    {@html message.content.replace(/\n/g, '<br>')}
                  </div>
                </div>
              {/if}
            </div>
          {/each}

          <!-- Typing Indicator -->
          {#if isTyping}
            <div class="message-group">
              <div class="message-avatar">SV</div>
              <div class="message-content">
                <div class="typing-indicator">
                  <div class="typing-dots">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                  </div>
                  <div class="typing-text">Thinking...</div>
                </div>
              </div>
            </div>
          {/if}
        </div>
      {/if}
    </div>

    <!-- Input Area -->
    <div class="input-area">
      <div class="input-container">
        <div class="input-left">
          <button class="input-btn" on:click={toggleMoreOptions}>
            <Plus size={18} />
          </button>
        </div>
        
        <textarea 
          class="chat-input" 
          bind:value={inputText}
          placeholder="Message {connectors.find(c => c.isActive)?.name || 'StudyVault AI'}..."
          on:keydown={handleKeydown}
          rows="1"
        ></textarea>
        
        <button 
          class="send-button" 
          class:active={inputText.trim()}
          on:click={sendMessage}
          disabled={!inputText.trim()}
        >
          <ArrowUp size={16} />
        </button>
      </div>
      <div class="input-hint">StudyVault AI uses RL algorithms not an LLM</div>
      
      <!-- More Options Dropdown -->
      {#if moreOptionsOpen}
        <button class="more-options-dropdown" role="menu" on:click|stopPropagation on:keydown={handleKeydown}>
          <div class="more-options-header">
            <h4>More Options</h4>
          </div>
          
          <div class="more-options-grid">
            <button class="more-option-btn" on:click={() => handleMoreOptionClick('import-file')} on:keydown={handleKeydown} role="menuitem">
              <div class="option-icon">
                <Paperclip size={20} />
              </div>
              <div class="option-content">
                <span class="option-title">Import File</span>
                <span class="option-description">Upload documents, PDFs, images</span>
              </div>
            </button>
            
            <button class="more-option-btn" on:click={() => handleMoreOptionClick('take-photo')} on:keydown={handleKeydown} role="menuitem">
              <div class="option-icon">
                <Camera size={20} />
              </div>
              <div class="option-content">
                <span class="option-title">Take Photo</span>
                <span class="option-description">Capture images with camera</span>
              </div>
            </button>
            
            <button class="more-option-btn" on:click={() => handleMoreOptionClick('voice-record')} on:keydown={handleKeydown} role="menuitem">
              <div class="option-icon">
                <Mic size={20} />
              </div>
              <div class="option-content">
                <span class="option-title">Voice Record</span>
                <span class="option-description">Record voice message</span>
              </div>
            </button>
            
            <button class="more-option-btn" on:click={() => handleMoreOptionClick('share-context')} on:keydown={handleKeydown} role="menuitem">
              <div class="option-icon">
                <Share2 size={20} />
              </div>
              <div class="option-content">
                <span class="option-title">Share Context</span>
                <span class="option-description">Export study context</span>
              </div>
            </button>
            
            <button class="more-option-btn highlight" on:click={() => handleMoreOptionClick('add-connector')} on:keydown={handleKeydown} role="menuitem">
              <div class="option-icon">
                <Plus size={20} />
              </div>
              <div class="option-content">
                <span class="option-title">Add Connector</span>
                <span class="option-description">Connect AI & note apps</span>
              </div>
            </button>
            
            <button class="more-option-btn" on:click={() => handleMoreOptionClick('settings')} on:keydown={handleKeydown} role="menuitem">
              <div class="option-icon">
                <Settings size={20} />
              </div>
              <div class="option-content">
                <span class="option-title">Settings</span>
                <span class="option-description">Manage preferences</span>
              </div>
            </button>
          </div>
        </button>
      {/if}
    </div>
  </div>

  <!-- Right Context Panel -->
  {#if contextPanelOpen}
    <div class="context-panel">
      <div class="context-header">
        <h4>Context</h4>
        <button class="close-btn" on:click={toggleContextPanel}>
          <X size={16} />
        </button>
      </div>
      
      <div class="context-content">
        <!-- External Connector Context Section -->
        {#if connectors.find(c => c.isActive && c.id !== 'studyvault-ai')}
          <div class="context-section external-connector">
            <div class="section-header">
              <div class="connector-icon" style="color: {connectors.find(c => c.isActive)?.color}">
                {connectors.find(c => c.isActive)?.icon}
              </div>
              SENDING TO {connectors.find(c => c.isActive)?.name?.toUpperCase()}
            </div>
            <div class="context-toggles">
              <div class="context-toggle">
                <label class="toggle-label">
                  <input type="checkbox" checked />
                  <span class="toggle-slider"></span>
                  <span class="toggle-text">Student Profile</span>
                </label>
              </div>
              <div class="context-toggle">
                <label class="toggle-label">
                  <input type="checkbox" checked />
                  <span class="toggle-slider"></span>
                  <span class="toggle-text">Current Subject</span>
                </label>
              </div>
              <div class="context-toggle">
                <label class="toggle-label">
                  <input type="checkbox" checked />
                  <span class="toggle-slider"></span>
                  <span class="toggle-text">Topic Coverage</span>
                </label>
              </div>
              <div class="context-toggle">
                <label class="toggle-label">
                  <input type="checkbox" checked />
                  <span class="toggle-slider"></span>
                  <span class="toggle-text">Today's Schedule</span>
                </label>
              </div>
              <div class="context-toggle">
                <label class="toggle-label">
                  <input type="checkbox" checked />
                  <span class="toggle-slider"></span>
                  <span class="toggle-text">Weak Areas</span>
                </label>
              </div>
              <div class="context-toggle">
                <label class="toggle-label">
                  <input type="checkbox" checked />
                  <span class="toggle-slider"></span>
                  <span class="toggle-text">Performance Data</span>
                </label>
              </div>
              <div class="context-toggle">
                <label class="toggle-label">
                  <input type="checkbox" checked />
                  <span class="toggle-slider"></span>
                  <span class="toggle-text">Response Style</span>
                </label>
              </div>
            </div>
            <div class="context-privacy-note">
              <span class="privacy-icon">🔒</span>
              <span class="privacy-text">Your data is sent directly to {connectors.find(c => c.isActive)?.name}. StudyVault never sees your API key or conversations.</span>
            </div>
          </div>
        {/if}

        <div class="context-section">
          <div class="section-header">
            <User size={13} />
            STUDENT PROFILE
          </div>
          <div class="context-item">
            <span class="context-label">Learning Style</span>
            <span class="context-value">Visual</span>
          </div>
          <div class="context-item">
            <span class="context-label">Personality</span>
            <span class="context-value">Achiever</span>
          </div>
          <div class="context-item">
            <span class="context-label">Exam In</span>
            <span class="context-value">21 days</span>
          </div>
        </div>

        <div class="context-section">
          <div class="section-header">
            <BookMarked size={13} />
            CURRENT SUBJECT
          </div>
          <div class="context-item">
            <span class="context-value">Computer Science 101</span>
          </div>
        </div>

        <div class="context-section">
          <div class="section-header">
            <TrendingUp size={13} />
            PERFORMANCE
          </div>
          <div class="context-item">
            <span class="context-label">Retention</span>
            <span class="context-value">78%</span>
          </div>
          <div class="context-item">
            <span class="context-label">Streak</span>
            <span class="context-value">3 days</span>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  /* Claude.ai Layout - Full Viewport */
  .claude-layout {
    display: grid;
    grid-template-columns: 240px 1fr 280px;
    height: 100vh;
    background: #0A0A0B;
    font-family: 'Inter', system-ui, sans-serif;
  }

  /* Global Icon Styling */
  :global(svg) {
    color: inherit;
    stroke-width: 1.75;
    fill: none;
    vertical-align: middle;
    flex-shrink: 0;
  }

  /* Left Sidebar */
  .sidebar {
    background: #111114;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .sidebar-top {
    padding: 16px;
    position: relative;
  }

  .logo-row {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .logo-icon {
    width: 28px;
    height: 28px;
    background: #C8FF00;
    color: #0A0A0B;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 11px;
  }

  .logo-text {
    font-size: 14px;
    font-weight: 600;
    color: white;
  }

  .new-chat-btn {
    width: 100%;
    height: 40px;
    margin-top: 16px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0 12px;
    color: rgba(255, 255, 255, 0.7);
    font-size: 14px;
    cursor: pointer;
    transition: all 150ms;
  }

  .new-chat-btn:hover {
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.9);
  }

  .connector-chip {
    height: 32px;
    border-radius: 6px;
    background: rgba(200, 255, 0, 0.08);
    border: 1px solid rgba(200, 255, 0, 0.2);
    padding: 0 10px;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 12px;
    cursor: pointer;
    transition: all 150ms;
    position: relative;
    width: 100%;
    justify-content: space-between;
    font-size: 13px;
  }

  .connector-chip:hover {
    background: rgba(200, 255, 0, 0.12);
    border-color: rgba(200, 255, 0, 0.3);
    transform: translateY(-1px);
  }

  .connector-dropdown-arrow {
    margin-left: auto;
    transition: transform 150ms;
  }

  .connector-dropdown {
    position: absolute;
    top: 100%;
    left: 16px;
    right: 16px;
    margin-top: 4px;
    background: #1a1a1c;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    overflow: hidden;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    max-height: 300px;
    overflow-y: auto;
  }

  .connector-option {
    width: 100%;
    padding: 8px 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    background: none;
    border: none;
    color: rgba(255, 255, 255, 0.7);
    cursor: pointer;
    transition: background 150ms;
    font-size: 13px;
  }

  .connector-option:hover {
    background: rgba(255, 255, 255, 0.05);
    color: white;
  }

  .connector-option.active {
    background: rgba(200, 255, 0, 0.1);
    color: #C8FF00;
  }

  .connector-option.connected {
    color: rgba(255, 255, 255, 0.9);
  }

  .connector-option-icon {
    font-size: 16px;
    width: 20px;
    text-align: center;
    flex-shrink: 0;
  }

  .connector-option-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  .connector-option-name {
    font-weight: 500;
    color: inherit;
  }

  .connector-option-status {
    font-size: 11px;
    color: rgba(200, 255, 0, 0.7);
    font-weight: 500;
  }

  .connector-option-model {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.5);
  }

  .connector-option-name {
    flex: 1;
    text-align: left;
  }

  .connector-dot {
    width: 8px;
    height: 8px;
    background: #C8FF00;
    border-radius: 50%;
  }

  .connector-name {
    font-size: 13px;
    color: #C8FF00;
  }

  .conversation-list {
    flex: 1;
    overflow-y: auto;
    padding: 8px;
  }

  .recents-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: rgba(255, 255, 255, 0.3);
    padding: 8px 8px 4px;
  }

  .conversation-item {
    padding: 8px 10px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    transition: background 150ms;
  }

  .conversation-item:hover {
    background: rgba(255, 255, 255, 0.04);
  }

  .conversation-item.active {
    background: rgba(255, 255, 255, 0.06);
  }

  .conversation-item.active .conversation-title {
    color: white;
  }

  .conversation-content {
    flex: 1;
    min-width: 0;
  }

  .conversation-title {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.7);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .conversation-preview {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.3);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-top: 2px;
  }

  .sidebar-bottom {
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .user-avatar {
    width: 32px;
    height: 32px;
    background: rgba(200, 255, 0, 0.15);
    border: 1px solid rgba(200, 255, 0, 0.3);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #C8FF00;
    font-size: 13px;
    font-weight: 600;
  }

  .user-name {
    flex: 1;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.7);
  }

  .settings-btn {
    background: none;
    border: none;
    color: rgba(255, 255, 255, 0.3);
    cursor: pointer;
    padding: 6px;
    border-radius: 6px;
    transition: all 150ms;
  }

  .settings-btn:hover {
    color: white;
    background: rgba(255, 255, 255, 0.06);
  }

  /* Main Chat Area */
  .main-chat {
    background: #0A0A0B;
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
  }

  .chat-header {
    height: 56px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    display: flex;
    align-items: center;
    padding: 0 20px;
  }

  .mobile-menu-btn {
    display: none;
    background: none;
    border: none;
    color: rgba(255, 255, 255, 0.4);
    cursor: pointer;
    padding: 6px;
    border-radius: 6px;
    margin-right: 12px;
  }

  .chat-title {
    font-size: 15px;
    font-weight: 500;
    color: white;
    flex: 1;
  }

  .header-center {
    display: flex;
    justify-content: center;
  }

  .header-right {
    display: flex;
    gap: 8px;
  }

  .header-btn {
    background: none;
    border: none;
    color: rgba(255, 255, 255, 0.4);
    cursor: pointer;
    padding: 6px;
    border-radius: 6px;
    transition: all 150ms;
  }

  .header-btn:hover {
    color: white;
    background: rgba(255, 255, 255, 0.06);
  }

  /* Messages Area */
  .messages-area {
    flex: 1;
    overflow-y: auto;
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 40px;
  }

  .greeting {
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: white;
  }

  .subtitle {
    font-size: 16px;
    color: rgba(255, 255, 255, 0.4);
    margin-top: 4px;
  }

  .suggestion-cards {
    margin-top: 32px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    max-width: 480px;
  }

  .suggestion-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 16px;
    cursor: pointer;
    text-align: left;
    transition: all 150ms;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .suggestion-card:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(200, 255, 0, 0.2);
    transform: translateY(-1px);
  }

  .card-title {
    font-size: 14px;
    font-weight: 600;
    color: white;
  }

  .card-description {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.4);
    margin-top: 4px;
  }

  .messages-container {
    max-width: 720px;
    margin: 0 auto;
    padding: 24px 24px 0;
  }

  .message-group {
    margin-bottom: 24px;
    display: flex;
    gap: 12px;
    align-items: flex-start;
  }

  .message-group.user-message {
    justify-content: flex-end;
  }

  .message-avatar {
    width: 28px;
    height: 28px;
    border-radius: 6px;
    background: rgba(200, 255, 0, 0.12);
    border: 1px solid rgba(200, 255, 0, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 11px;
    color: #C8FF00;
    flex-shrink: 0;
  }

  .message-content {
    flex: 1;
  }

  .message-text {
    font-size: 15px;
    line-height: 1.75;
    color: rgba(255, 255, 255, 0.87);
  }

  .message-text strong {
    font-weight: 600;
  }

  .message-line {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
  }

  .message-line :global(svg) {
    color: #C8FF00;
    flex-shrink: 0;
  }

  .message-actions {
    opacity: 0;
    transition: opacity 150ms;
    display: flex;
    gap: 4px;
    margin-top: 8px;
  }

  .message-group:hover .message-actions {
    opacity: 1;
  }

  .action-btn {
    height: 28px;
    padding: 0 8px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.06);
    color: rgba(255, 255, 255, 0.4);
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 4px;
    cursor: pointer;
    transition: all 150ms;
  }

  .action-btn:hover {
    background: rgba(255, 255, 255, 0.08);
    color: white;
  }

  .user-message {
    display: flex;
    justify-content: flex-end;
  }

  .user-bubble {
    max-width: 80%;
    background: rgba(30, 27, 75, 0.8);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 18px 18px 4px 18px;
    padding: 12px 16px;
    font-size: 15px;
    line-height: 1.6;
    color: rgba(255, 255, 255, 0.9);
  }

  .typing-indicator {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .typing-dots {
    display: flex;
    gap: 4px;
  }

  .dot {
    width: 8px;
    height: 8px;
    background: #C8FF00;
    border-radius: 50%;
    animation: bounce 1.4s infinite ease-in-out both;
  }

  .dot:nth-child(1) { animation-delay: -0.32s; }
  .dot:nth-child(2) { animation-delay: -0.16s; }
  .dot:nth-child(3) { animation-delay: 0; }

  @keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-4px); }
  }

  .typing-text {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.3);
  }

  /* Input Area */
  .input-area {
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    background: #0A0A0B;
    padding: 16px 24px 20px;
  }

  .input-container {
    max-width: 720px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 12px 16px;
    display: flex;
    align-items: flex-end;
    gap: 10px;
    transition: border-color 150ms, box-shadow 150ms;
  }

  .input-container:focus-within {
    border-color: rgba(200, 255, 0, 0.3);
    box-shadow: 0 0 0 3px rgba(200, 255, 0, 0.06);
  }

  .input-left {
    display: flex;
    gap: 6px;
    align-items: center;
  }

  .input-btn {
    background: none;
    border: none;
    color: rgba(255, 255, 255, 0.3);
    cursor: pointer;
    padding: 4px;
    border-radius: 6px;
    transition: all 150ms;
  }

  .input-btn:hover {
    color: rgba(255, 255, 255, 0.7);
  }

  .chat-input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: white;
    font-size: 15px;
    line-height: 1.6;
    resize: none;
    min-height: 24px;
    max-height: 160px;
    overflow-y: auto;
    font-family: 'Inter', sans-serif;
  }

  .chat-input::placeholder {
    color: rgba(255, 255, 255, 0.25);
  }

  .send-button {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: transparent;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    color: rgba(255, 255, 255, 0.2);
    cursor: default;
    transition: all 150ms;
  }

  .send-button.active {
    background: #C8FF00;
    color: #0A0A0B;
    cursor: pointer;
  }

  .send-button.active:hover {
    filter: brightness(0.9);
  }

  .input-hint {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.2);
    text-align: center;
    margin-top: 8px;
  }

  /* Context Panel */
  .context-panel {
    background: #111114;
    border-left: 1px solid rgba(255, 255, 255, 0.06);
    height: 100vh;
    overflow-y: auto;
    padding: 20px;
  }

  .context-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
  }

  .context-section.external-connector {
    background: rgba(200, 255, 0, 0.05);
    border: 1px solid rgba(200, 255, 0, 0.1);
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 16px;
  }

  .connector-icon {
    font-size: 14px;
    margin-right: 6px;
  }

  .context-toggles {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin: 12px 0;
  }

  .context-toggle {
    display: flex;
    align-items: center;
  }

  .toggle-label {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    width: 100%;
    font-size: 12px;
  }

  .toggle-label input[type="checkbox"] {
    display: none;
  }

  .toggle-slider {
    width: 32px;
    height: 16px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    position: relative;
    transition: background 150ms;
  }

  .toggle-slider::before {
    content: '';
    position: absolute;
    top: 2px;
    left: 2px;
    width: 12px;
    height: 12px;
    background: white;
    border-radius: 50%;
    transition: transform 150ms;
  }

  .toggle-label input:checked + .toggle-slider {
    background: #C8FF00;
  }

  .toggle-label input:checked + .toggle-slider::before {
    transform: translateX(16px);
  }

  .toggle-text {
    color: rgba(255, 255, 255, 0.7);
    font-size: 12px;
  }

  .context-privacy-note {
    display: flex;
    align-items: flex-start;
    gap: 6px;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    font-size: 11px;
    color: rgba(255, 255, 255, 0.5);
  }

  .privacy-icon {
    flex-shrink: 0;
    margin-top: 1px;
    color: rgba(255, 255, 255, 0.5);
  }

  /* More Options Dropdown */
  .more-options-dropdown {
    position: absolute;
    bottom: 80px;
    left: 20px;
    background: rgba(20, 20, 20, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 16px;
    min-width: 320px;
    max-width: 400px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    z-index: 1000;
  }

  .more-options-header h4 {
    font-size: 14px;
    font-weight: 600;
    color: white;
    margin: 0 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .more-options-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .more-option-btn {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: white;
    cursor: pointer;
    transition: all 150ms;
    text-align: left;
  }

  .more-option-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-1px);
  }

  .more-option-btn.highlight {
    background: rgba(200, 255, 0, 0.1);
    border-color: rgba(200, 255, 0, 0.3);
  }

  .more-option-btn.highlight:hover {
    background: rgba(200, 255, 0, 0.15);
  }

  .option-icon {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    flex-shrink: 0;
  }

  .more-option-btn.highlight .option-icon {
    background: rgba(200, 255, 0, 0.2);
    color: #C8FF00;
  }

  .option-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .option-title {
    font-size: 14px;
    font-weight: 500;
    color: white;
  }

  .option-description {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
    line-height: 1.3;
  }

  .context-header h4 {
    font-size: 14px;
    font-weight: 600;
    color: white;
  }

  .close-btn {
    background: none;
    border: none;
    color: rgba(255, 255, 255, 0.4);
    cursor: pointer;
    padding: 6px;
    border-radius: 6px;
    transition: all 150ms;
  }

  .close-btn:hover {
    color: white;
  }

  .section-header {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: rgba(255, 255, 255, 0.3);
    margin-top: 20px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .context-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  }

  .context-label {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.4);
  }

  .context-value {
    font-size: 13px;
    color: white;
    font-weight: 500;
  }

  /* Mobile Responsive */
  @media (max-width: 768px) {
    .claude-layout {
      grid-template-columns: 1fr;
    }

    .sidebar {
      position: fixed;
      left: 0;
      top: 0;
      width: 280px;
      z-index: 1000;
      transform: translateX(-100%);
      transition: transform 250ms ease-out;
    }

    .sidebar.mobile-open {
      transform: translateX(0);
    }

    .mobile-backdrop {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      z-index: 999;
    }

    .mobile-menu-btn {
      display: block;
    }

    .context-panel {
      display: none;
    }

    .suggestion-cards {
      grid-template-columns: 1fr;
    }
  }
</style>
