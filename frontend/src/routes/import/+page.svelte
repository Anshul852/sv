<script lang="ts">
  import { onMount } from 'svelte';
  import { user } from '$lib/stores/auth';
  
  let selectedFile: File | null = null;
  let uploadProgress = 0;
  let isUploading = false;
  let extractedTopics: any[] = [];
  let processingError: string | null = null;
  let showResults = false;
  
  $: currentUser = $user;
  
  // File handling
  function handleFileSelect(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files[0]) {
      selectedFile = target.files[0];
      processingError = null;
      showResults = false;
    }
  }
  
  // Upload and process syllabus
  async function uploadSyllabus() {
    if (!selectedFile || !currentUser) return;
    
    isUploading = true;
    uploadProgress = 0;
    processingError = null;
    
    try {
      const formData = new FormData();
      formData.append('syllabus', selectedFile);
      formData.append('userId', currentUser.user?.id || '');
      
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        uploadProgress = Math.min(uploadProgress + 10, 90);
      }, 200);
      
      const response = await fetch('/api/syllabus/upload', {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${currentUser.session?.access_token || ''}`
        }
      });
      
      clearInterval(progressInterval);
      uploadProgress = 100;
      
      if (response.ok) {
        const result = await response.json();
        extractedTopics = result.topics || [];
        showResults = true;
        
        // Save to IndexedDB
        await saveToIndexedDB(result);
      } else {
        const error = await response.json();
        processingError = error.message || 'Upload failed';
      }
    } catch (error) {
      processingError = 'Network error. Please try again.';
      console.error('Upload error:', error);
    } finally {
      isUploading = false;
    }
  }
  
  // Save to IndexedDB
  async function saveToIndexedDB(data: any) {
    try {
      const db = await openIndexedDB();
      const transaction = db.transaction(['syllabi'], 'readwrite');
      const store = transaction.objectStore('syllabi');
      
      await store.add({
        id: Date.now(),
        filename: selectedFile?.name,
        uploadDate: new Date(),
        topics: data.topics,
        metadata: data.metadata
      });
    } catch (error) {
      console.error('IndexedDB error:', error);
    }
  }
  
  // Open IndexedDB
  function openIndexedDB(): Promise<IDBDatabase> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open('StudyVaultDB', 1);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result);
      
      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        if (!db.objectStoreNames.contains('syllabi')) {
          db.createObjectStore('syllabi', { keyPath: 'id' });
        }
      };
    });
  }
  
  // Generate study plan
  function generateStudyPlan() {
    if (!extractedTopics.length) return;
    
    const planData = {
      topics: extractedTopics,
      examDate: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000), // 2 weeks from now
      subject: 'General'
    };
    
    // Navigate to plan generation
    window.location.href = `/plan?data=${encodeURIComponent(JSON.stringify(planData))}`;
  }
  
  // Format file size
  function formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
  
  // Validate file type
  function isValidFileType(file: File): boolean {
    const validTypes = ['application/pdf', 'text/plain', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    return validTypes.includes(file.type);
  }
</script>

<div class="import-page">
  <div class="import-container">
    <!-- Header -->
    <div class="import-header">
      <h1 class="page-title">Import Syllabus</h1>
      <p class="page-subtitle">Upload your course syllabus to automatically extract topics and generate a study plan</p>
    </div>
    
    <!-- Upload Area -->
    <div class="upload-section">
      <div class="upload-area" class:drag-over={false}>
        <div class="upload-content">
          <div class="upload-icon">📄</div>
          <h3>Drop your syllabus here</h3>
          <p>or</p>
          <label for="file-input" class="upload-button">
            Browse Files
          </label>
          <input 
            id="file-input" 
            type="file" 
            accept=".pdf,.doc,.docx,.txt"
            on:change={handleFileSelect}
          />
        </div>
        
        {#if selectedFile}
          <div class="selected-file">
            <div class="file-info">
              <span class="file-name">{selectedFile.name}</span>
              <span class="file-size">{formatFileSize(selectedFile.size)}</span>
            </div>
            <button 
              class="upload-action-button" 
              on:click={uploadSyllabus}
              disabled={isUploading || !isValidFileType(selectedFile)}
            >
              {#if isUploading}
                <span class="spinner"></span>
                Processing... {uploadProgress}%
              {:else}
                Extract Topics
              {/if}
            </button>
          </div>
        {/if}
      </div>
      
      <!-- Supported Formats -->
      <div class="supported-formats">
        <h4>Supported Formats</h4>
        <div class="format-list">
          <span class="format-badge">PDF</span>
          <span class="format-badge">DOC</span>
          <span class="format-badge">DOCX</span>
          <span class="format-badge">TXT</span>
        </div>
      </div>
    </div>
    
    <!-- Error Display -->
    {#if processingError}
      <div class="error-message">
        <span class="error-icon">⚠️</span>
        <span class="error-text">{processingError}</span>
      </div>
    {/if}
    
    <!-- Results Display -->
    {#if showResults && extractedTopics.length > 0}
      <div class="results-section">
        <h2 class="results-title">Extracted Topics</h2>
        <p class="results-subtitle">Review and edit topics before generating your study plan</p>
        
        <div class="topics-list">
          {#each extractedTopics as topic, index}
            <div class="topic-item">
              <div class="topic-header">
                <span class="topic-number">{index + 1}</span>
                <span class="topic-name">{topic.name}</span>
                <span class="topic-weight">{topic.weight || 5}%</span>
              </div>
              <div class="topic-details">
                <span class="topic-duration">{topic.estimatedHours || 2} hours</span>
                <span class="topic-difficulty">{topic.difficulty || 'Medium'}</span>
              </div>
            </div>
          {/each}
        </div>
        
        <div class="results-actions">
          <button class="action-button secondary" on:click={() => showResults = false}>
            Edit Topics
          </button>
          <button class="action-button primary" on:click={generateStudyPlan}>
            Generate Study Plan
          </button>
        </div>
      </div>
    {/if}
    
    <!-- Instructions -->
    <div class="instructions-section">
      <h3>How it works</h3>
      <div class="instruction-steps">
        <div class="step">
          <div class="step-number">1</div>
          <div class="step-content">
            <h4>Upload Syllabus</h4>
            <p>Upload your course syllabus in PDF, Word, or text format</p>
          </div>
        </div>
        <div class="step">
          <div class="step-number">2</div>
          <div class="step-content">
            <h4>AI Extraction</h4>
            <p>Our Python parser extracts topics, deadlines, and weightings automatically</p>
          </div>
        </div>
        <div class="step">
          <div class="step-number">3</div>
          <div class="step-content">
            <h4>Review & Edit</h4>
            <p>Review extracted topics and make any necessary adjustments</p>
          </div>
        </div>
        <div class="step">
          <div class="step-number">4</div>
          <div class="step-content">
            <h4>Generate Plan</h4>
            <p>Create a personalized study plan based on your exam date and learning style</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .import-page {
    min-height: 100vh;
    background: var(--bg);
    color: var(--text-primary);
    font-family: var(--font-sans);
    padding: 40px 20px;
  }
  
  .import-container {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .import-header {
    text-align: center;
    margin-bottom: 48px;
  }
  
  .page-title {
    font-size: 32px;
    font-weight: 700;
    margin: 0 0 12px 0;
    color: var(--text-primary);
  }
  
  .page-subtitle {
    font-size: 16px;
    color: var(--text-muted);
    margin: 0;
    line-height: 1.5;
  }
  
  .upload-section {
    margin-bottom: 40px;
  }
  
  .upload-area {
    border: 2px dashed var(--border);
    border-radius: var(--radius-card);
    padding: 48px 24px;
    text-align: center;
    transition: all 0.3s ease;
    background: var(--surface);
  }
  
  .upload-area:hover {
    border-color: var(--accent);
    background: rgba(181, 255, 77, 0.05);
  }
  
  .upload-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
  }
  
  .upload-icon {
    font-size: 48px;
    margin-bottom: 8px;
  }
  
  .upload-content h3 {
    font-size: 18px;
    font-weight: 600;
    margin: 0;
    color: var(--text-primary);
  }
  
  .upload-content p {
    color: var(--text-muted);
    margin: 0;
  }
  
  .upload-button {
    background: var(--accent);
    color: #000;
    padding: 12px 24px;
    border-radius: var(--radius-input);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .upload-button:hover {
    filter: brightness(1.1);
  }
  
  #file-input {
    display: none;
  }
  
  .selected-file {
    margin-top: 24px;
    padding: 20px;
    background: rgba(181, 255, 77, 0.1);
    border: 1px solid var(--accent);
    border-radius: var(--radius-input);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .file-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  
  .file-name {
    font-weight: 600;
    color: var(--text-primary);
  }
  
  .file-size {
    font-size: 14px;
    color: var(--text-muted);
  }
  
  .upload-action-button {
    background: var(--accent);
    color: #000;
    border: none;
    padding: 12px 24px;
    border-radius: var(--radius-input);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .upload-action-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .spinner {
    width: 16px;
    height: 16px;
    border: 2px solid #000;
    border-top: 2px solid transparent;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  .supported-formats {
    margin-top: 24px;
    text-align: center;
  }
  
  .supported-formats h4 {
    font-size: 14px;
    font-weight: 600;
    margin: 0 0 12px 0;
    color: var(--text-muted);
  }
  
  .format-list {
    display: flex;
    gap: 8px;
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .format-badge {
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 4px 12px;
    border-radius: 16px;
    font-size: 12px;
    font-weight: 600;
    color: var(--text-muted);
  }
  
  .error-message {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: var(--radius-input);
    padding: 16px;
    margin: 24px 0;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  
  .error-icon {
    font-size: 20px;
  }
  
  .error-text {
    color: #ef4444;
    font-weight: 500;
  }
  
  .results-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 32px;
    margin-bottom: 40px;
  }
  
  .results-title {
    font-size: 24px;
    font-weight: 700;
    margin: 0 0 8px 0;
    color: var(--text-primary);
  }
  
  .results-subtitle {
    color: var(--text-muted);
    margin: 0 0 24px 0;
  }
  
  .topics-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 32px;
  }
  
  .topic-item {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius-input);
    padding: 16px;
  }
  
  .topic-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
  }
  
  .topic-number {
    background: var(--accent);
    color: #000;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 700;
  }
  
  .topic-name {
    flex: 1;
    font-weight: 600;
    color: var(--text-primary);
  }
  
  .topic-weight {
    background: rgba(0, 212, 200, 0.1);
    color: var(--cyan);
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
  }
  
  .topic-details {
    display: flex;
    gap: 16px;
    font-size: 14px;
    color: var(--text-muted);
  }
  
  .results-actions {
    display: flex;
    gap: 12px;
    justify-content: flex-end;
  }
  
  .action-button {
    padding: 12px 24px;
    border-radius: var(--radius-input);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
  }
  
  .action-button.secondary {
    background: transparent;
    color: var(--text-muted);
    border: 1px solid var(--border);
  }
  
  .action-button.primary {
    background: var(--accent);
    color: #000;
  }
  
  .action-button:hover {
    filter: brightness(1.1);
  }
  
  .instructions-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 32px;
  }
  
  .instructions-section h3 {
    font-size: 20px;
    font-weight: 600;
    margin: 0 0 24px 0;
    color: var(--text-primary);
    text-align: center;
  }
  
  .instruction-steps {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 24px;
  }
  
  .step {
    display: flex;
    gap: 16px;
  }
  
  .step-number {
    background: var(--accent);
    color: #000;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    font-weight: 700;
    flex-shrink: 0;
  }
  
  .step-content h4 {
    font-size: 16px;
    font-weight: 600;
    margin: 0 0 8px 0;
    color: var(--text-primary);
  }
  
  .step-content p {
    font-size: 14px;
    color: var(--text-muted);
    margin: 0;
    line-height: 1.5;
  }
  
  @media (max-width: 768px) {
    .import-page {
      padding: 20px 16px;
    }
    
    .instruction-steps {
      grid-template-columns: 1fr;
    }
    
    .results-actions {
      flex-direction: column;
    }
    
    .topic-header {
      flex-wrap: wrap;
    }
  }
</style>
