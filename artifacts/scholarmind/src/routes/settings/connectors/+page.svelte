<script lang="ts">
  import { onMount } from 'svelte';
  import { ChevronDown, ChevronUp, Check, X, Key, Shield, Globe, Book, Settings } from 'lucide-svelte';

  interface Connector {
    id: string;
    name: string;
    color: string;
    category: 'ai' | 'note';
    isConnected: boolean;
    isActive: boolean;
    icon: string;
    description: string;
    apiKeyRequired: boolean;
    website?: string;
    model?: string;
  }

  let connectors: Connector[] = [
    {
      id: 'claude',
      name: 'Claude',
      color: '#FF6B35',
      category: 'ai',
      isConnected: false,
      isActive: false,
      icon: '◆',
      description: 'Anthropic\'s AI assistant with advanced reasoning',
      apiKeyRequired: true,
      website: 'https://claude.ai',
      model: 'claude-sonnet-4-6'
    },
    {
      id: 'gemini',
      name: 'Gemini',
      color: '#4285F4',
      category: 'ai',
      isConnected: false,
      isActive: false,
      icon: '✦',
      description: 'Google\'s multimodal AI assistant',
      apiKeyRequired: true,
      website: 'https://gemini.google.com',
      model: 'gemini-1.5-pro'
    },
    {
      id: 'chatgpt',
      name: 'ChatGPT',
      color: '#10A37F',
      category: 'ai',
      isConnected: false,
      isActive: false,
      icon: '●',
      description: 'OpenAI\'s conversational AI',
      apiKeyRequired: true,
      website: 'https://chat.openai.com',
      model: 'gpt-4o'
    },
    {
      id: 'notebooklm',
      name: 'NotebookLM',
      color: '#4285F4',
      category: 'ai',
      isConnected: false,
      isActive: false,
      icon: '📚',
      description: 'Google\'s AI research assistant',
      apiKeyRequired: true,
      website: 'https://notebooklm.google.com',
      model: 'gemini-1.5-pro'
    },
    {
      id: 'perplexity',
      name: 'Perplexity',
      color: '#5D6AFF',
      category: 'ai',
      isConnected: false,
      isActive: false,
      icon: '⚡',
      description: 'AI with real-time web search',
      apiKeyRequired: true,
      website: 'https://perplexity.ai',
      model: 'llama-3.1-sonar-small-128k-online'
    },
    {
      id: 'obsidian',
      name: 'Obsidian',
      color: '#7C3AED',
      category: 'note',
      isConnected: false,
      isActive: false,
      icon: '💎',
      description: 'Personal knowledge base and note management',
      apiKeyRequired: true,
      website: 'https://obsidian.md'
    },
    {
      id: 'notion',
      name: 'Notion',
      color: '#000000',
      category: 'note',
      isConnected: false,
      isActive: false,
      icon: '📋',
      description: 'All-in-one workspace for notes and tasks',
      apiKeyRequired: true,
      website: 'https://notion.so'
    }
  ];

  let expandedConnector: string | null = null;
  let apiKeyInputs: Record<string, string> = {};
  let connectionStatus: Record<string, 'idle' | 'connecting' | 'connected' | 'error'> = {};
  let errorMessages: Record<string, string> = {};

  function toggleExpanded(connectorId: string) {
    expandedConnector = expandedConnector === connectorId ? null : connectorId;
  }

  async function connectConnector(connectorId: string) {
    const apiKey = apiKeyInputs[connectorId];
    if (!apiKey || apiKey.trim().length < 10) {
      errorMessages[connectorId] = 'Please enter a valid API key';
      return;
    }

    connectionStatus[connectorId] = 'connecting';
    errorMessages[connectorId] = '';

    try {
      // Simulate API key validation
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Simulate validation result (90% success rate)
      if (Math.random() > 0.1) {
        connectionStatus[connectorId] = 'connected';
        const connector = connectors.find(c => c.id === connectorId);
        if (connector) {
          connector.isConnected = true;
        }
        apiKeyInputs[connectorId] = '';
      } else {
        throw new Error('Invalid API key');
      }
    } catch (error) {
      connectionStatus[connectorId] = 'error';
      errorMessages[connectorId] = 'Invalid API key. Please check your key and try again.';
    }
  }

  async function disconnectConnector(connectorId: string) {
    const connector = connectors.find(c => c.id === connectorId);
    if (connector) {
      connector.isConnected = false;
      connector.isActive = false;
    }
    connectionStatus[connectorId] = 'idle';
    errorMessages[connectorId] = '';
  }

  function getConnectorIcon(connector: Connector) {
    return connector.icon;
  }

  function getStatusIcon(status: string) {
    switch (status) {
      case 'connecting':
        return '⏳';
      case 'connected':
        return '✅';
      case 'error':
        return '❌';
      default:
        return '';
    }
  }

  $: aiConnectors = connectors.filter(c => c.category === 'ai');
  $: noteConnectors = connectors.filter(c => c.category === 'note');
</script>

<div class="connectors-page">
  <div class="page-header">
    <div class="header-content">
      <h1>Connectors</h1>
      <p>Manage your AI and note-taking app integrations</p>
    </div>
    <div class="header-actions">
      <button class="help-btn">
        <Settings size={16} />
        Help
      </button>
    </div>
  </div>

  <div class="privacy-notice">
    <div class="privacy-icon">
      <Shield size={20} />
    </div>
    <div class="privacy-content">
      <h3>Privacy First</h3>
      <p>Your API keys and conversations are stored locally and sent directly to the services. StudyVault never has access to your data.</p>
    </div>
  </div>

  <!-- AI Connectors Section -->
  <div class="connector-section">
    <div class="section-header">
      <div class="section-icon">
        <Globe size={18} />
      </div>
      <div class="section-info">
        <h2>AI Assistants</h2>
        <p>Connect external AI models for enhanced study assistance</p>
      </div>
    </div>

    <div class="connectors-grid">
      {#each aiConnectors as connector}
        <div class="connector-card" class:connected={connector.isConnected}>
          <div class="card-header" on:click={() => toggleExpanded(connector.id)}>
            <div class="connector-info">
              <div class="connector-icon" style="color: {connector.color}">
                {getConnectorIcon(connector)}
              </div>
              <div class="connector-details">
                <h3>{connector.name}</h3>
                <p>{connector.description}</p>
              </div>
            </div>
            <div class="card-actions">
              {#if connector.isConnected}
                <div class="connection-badge connected">
                  <Check size={12} />
                  Connected
                </div>
              {:else}
                <div class="connection-badge">
                  Connect
                </div>
              {/if}
              {#if expandedConnector === connector.id}
                <ChevronUp size={16} />
              {:else}
                <ChevronDown size={16} />
              {/if}
            </div>
          </div>

          {#if expandedConnector === connector.id}
            <div class="card-content">
              <div class="connector-details-expanded">
                <div class="detail-row">
                  <span class="detail-label">Model:</span>
                  <span class="detail-value">{connector.model || 'N/A'}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Website:</span>
                  <a href={connector.website} target="_blank" class="detail-link">
                    {connector.website}
                  </a>
                </div>
              </div>

              {#if !connector.isConnected}
                <div class="connection-form">
                  <div class="input-group">
                    <label for="api-key-{connector.id}">
                      <Key size={14} />
                      API Key
                    </label>
                    <input
                      id="api-key-{connector.id}"
                      type="password"
                      placeholder="Enter your {connector.name} API key"
                      bind:value={apiKeyInputs[connector.id]}
                      class:error={errorMessages[connector.id]}
                    />
                    {#if errorMessages[connector.id]}
                      <div class="error-message">
                        <X size={12} />
                        {errorMessages[connector.id]}
                      </div>
                    {/if}
                  </div>

                  <div class="form-actions">
                    <button
                      class="connect-btn"
                      on:click={() => connectConnector(connector.id)}
                      disabled={connectionStatus[connector.id] === 'connecting'}
                    >
                      {#if connectionStatus[connector.id] === 'connecting'}
                        {getStatusIcon('connecting')} Connecting...
                      {:else}
                        <Key size={14} />
                        Connect
                      {/if}
                    </button>
                  </div>
                </div>
              {:else}
                <div class="connected-info">
                  <div class="success-message">
                    <Check size={16} />
                    Successfully connected to {connector.name}
                  </div>
                  <button
                    class="disconnect-btn"
                    on:click={() => disconnectConnector(connector.id)}
                  >
                    <X size={14} />
                    Disconnect
                  </button>
                </div>
              {/if}
            </div>
          {/if}
        </div>
      {/each}
    </div>
  </div>

  <!-- Note-Taking Connectors Section -->
  <div class="connector-section">
    <div class="section-header">
      <div class="section-icon">
        <Book size={18} />
      </div>
      <div class="section-info">
        <h2>Note-Taking Apps</h2>
        <p>Integrate with your favorite note-taking and knowledge management tools</p>
      </div>
    </div>

    <div class="connectors-grid">
      {#each noteConnectors as connector}
        <div class="connector-card" class:connected={connector.isConnected}>
          <div class="card-header" on:click={() => toggleExpanded(connector.id)}>
            <div class="connector-info">
              <div class="connector-icon" style="color: {connector.color}">
                {getConnectorIcon(connector)}
              </div>
              <div class="connector-details">
                <h3>{connector.name}</h3>
                <p>{connector.description}</p>
              </div>
            </div>
            <div class="card-actions">
              {#if connector.isConnected}
                <div class="connection-badge connected">
                  <Check size={12} />
                  Connected
                </div>
              {:else}
                <div class="connection-badge">
                  Connect
                </div>
              {/if}
              {#if expandedConnector === connector.id}
                <ChevronUp size={16} />
              {:else}
                <ChevronDown size={16} />
              {/if}
            </div>
          </div>

          {#if expandedConnector === connector.id}
            <div class="card-content">
              <div class="connector-details-expanded">
                <div class="detail-row">
                  <span class="detail-label">Website:</span>
                  <a href={connector.website} target="_blank" class="detail-link">
                    {connector.website}
                  </a>
                </div>
              </div>

              {#if !connector.isConnected}
                <div class="connection-form">
                  <div class="input-group">
                    <label for="api-key-{connector.id}">
                      <Key size={14} />
                      API Key / Token
                    </label>
                    <input
                      id="api-key-{connector.id}"
                      type="password"
                      placeholder="Enter your {connector.name} API key"
                      bind:value={apiKeyInputs[connector.id]}
                      class:error={errorMessages[connector.id]}
                    />
                    {#if errorMessages[connector.id]}
                      <div class="error-message">
                        <X size={12} />
                        {errorMessages[connector.id]}
                      </div>
                    {/if}
                  </div>

                  <div class="form-actions">
                    <button
                      class="connect-btn"
                      on:click={() => connectConnector(connector.id)}
                      disabled={connectionStatus[connector.id] === 'connecting'}
                    >
                      {#if connectionStatus[connector.id] === 'connecting'}
                        {getStatusIcon('connecting')} Connecting...
                      {:else}
                        <Key size={14} />
                        Connect
                      {/if}
                    </button>
                  </div>
                </div>
              {:else}
                <div class="connected-info">
                  <div class="success-message">
                    <Check size={16} />
                    Successfully connected to {connector.name}
                  </div>
                  <button
                    class="disconnect-btn"
                    on:click={() => disconnectConnector(connector.id)}
                  >
                    <X size={14} />
                    Disconnect
                  </button>
                </div>
              {/if}
            </div>
          {/if}
        </div>
      {/each}
    </div>
  </div>
</div>

<style>
  .connectors-page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 24px;
    color: white;
  }

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 32px;
  }

  .header-content h1 {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 8px;
    color: white;
  }

  .header-content p {
    font-size: 16px;
    color: rgba(255, 255, 255, 0.7);
  }

  .help-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    color: white;
    font-size: 14px;
    cursor: pointer;
    transition: all 150ms;
  }

  .help-btn:hover {
    background: rgba(255, 255, 255, 0.15);
  }

  .privacy-notice {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 20px;
    background: rgba(200, 255, 0, 0.05);
    border: 1px solid rgba(200, 255, 0, 0.1);
    border-radius: 12px;
    margin-bottom: 32px;
  }

  .privacy-icon {
    padding: 8px;
    background: rgba(200, 255, 0, 0.1);
    border-radius: 8px;
    color: #C8FF00;
    flex-shrink: 0;
  }

  .privacy-content h3 {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 4px;
    color: #C8FF00;
  }

  .privacy-content p {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.7);
    line-height: 1.5;
  }

  .connector-section {
    margin-bottom: 48px;
  }

  .section-header {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 24px;
  }

  .section-icon {
    padding: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: white;
    flex-shrink: 0;
  }

  .section-info h2 {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 4px;
    color: white;
  }

  .section-info p {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.7);
  }

  .connectors-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 20px;
  }

  .connector-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    overflow: hidden;
    transition: all 150ms;
  }

  .connector-card.connected {
    border-color: #C8FF00;
    background: rgba(200, 255, 0, 0.05);
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px;
    cursor: pointer;
    transition: background 150ms;
  }

  .card-header:hover {
    background: rgba(255, 255, 255, 0.05);
  }

  .connector-info {
    display: flex;
    align-items: center;
    gap: 12px;
    flex: 1;
  }

  .connector-icon {
    font-size: 24px;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    flex-shrink: 0;
  }

  .connector-details h3 {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 4px;
    color: white;
  }

  .connector-details p {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
    line-height: 1.4;
  }

  .card-actions {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .connection-badge {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 4px 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    font-size: 11px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.7);
  }

  .connection-badge.connected {
    background: rgba(200, 255, 0, 0.2);
    color: #C8FF00;
  }

  .card-content {
    padding: 0 20px 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }

  .connector-details-expanded {
    padding: 16px 0;
  }

  .detail-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }

  .detail-label {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
  }

  .detail-value {
    font-size: 13px;
    color: white;
    font-weight: 500;
  }

  .detail-link {
    font-size: 13px;
    color: #C8FF00;
    text-decoration: none;
  }

  .detail-link:hover {
    text-decoration: underline;
  }

  .connection-form {
    padding: 16px 0;
  }

  .input-group {
    margin-bottom: 16px;
  }

  .input-group label {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    font-weight: 500;
    color: white;
    margin-bottom: 8px;
  }

  .input-group input {
    width: 100%;
    padding: 12px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    color: white;
    font-size: 14px;
    transition: all 150ms;
  }

  .input-group input:focus {
    outline: none;
    border-color: #C8FF00;
    background: rgba(255, 255, 255, 0.08);
  }

  .input-group input.error {
    border-color: #ff4444;
  }

  .error-message {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 8px;
    font-size: 12px;
    color: #ff4444;
  }

  .form-actions {
    display: flex;
    gap: 8px;
  }

  .connect-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    background: #C8FF00;
    border: none;
    border-radius: 8px;
    color: black;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 150ms;
  }

  .connect-btn:hover:not(:disabled) {
    background: #B8E600;
    transform: translateY(-1px);
  }

  .connect-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .connected-info {
    padding: 16px 0;
  }

  .success-message {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 16px;
    font-size: 14px;
    color: #C8FF00;
  }

  .disconnect-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    background: rgba(255, 68, 68, 0.1);
    border: 1px solid rgba(255, 68, 68, 0.3);
    border-radius: 6px;
    color: #ff4444;
    font-size: 12px;
    cursor: pointer;
    transition: all 150ms;
  }

  .disconnect-btn:hover {
    background: rgba(255, 68, 68, 0.2);
  }

  @media (max-width: 768px) {
    .connectors-page {
      padding: 16px;
    }

    .page-header {
      flex-direction: column;
      gap: 16px;
    }

    .connectors-grid {
      grid-template-columns: 1fr;
    }

    .card-header {
      padding: 16px;
    }

    .connector-details h3 {
      font-size: 15px;
    }

    .connector-details p {
      font-size: 12px;
    }
  }
</style>
