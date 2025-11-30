<script lang="ts">
    import { api } from '$lib/api';
    import MonacoEditor from '$lib/components/editor/MonacoEditor.svelte';
    import { auth } from '$lib/stores/auth';

    let prompt = '';
    let generating = false;
    let codeContent = { html: '', css: '', js: '' };
    let activeTab = 'html';
    let previewUrl = '';
    let error = '';

    $: currentCode = codeContent[activeTab as keyof typeof codeContent];

    function updatePreview() {
        const { html, css, js } = codeContent;
        const blob = new Blob([`
            <!DOCTYPE html>
            <html>
            <head>
                <script src="https://cdn.tailwindcss.com"><\/script>
                <style>${css}</style>
            </head>
            <body>
                ${html}
                <script>${js}<\/script>
            </body>
            </html>
        `], { type: 'text/html' });
        
        if (previewUrl) URL.revokeObjectURL(previewUrl);
        previewUrl = URL.createObjectURL(blob);
    }

    async function handleGenerate() {
        if (!prompt.trim()) return;
        
        generating = true;
        error = '';
        codeContent = { html: '', css: '', js: '' };

        try {
            const response = await api.post<any>('/ai/generate/', { prompt });
            console.log('AI Response:', response);
            
            if (!response.code_content) {
                throw new Error('Invalid response from AI: Missing code_content');
            }
            
            codeContent = response.code_content;
            updatePreview();

        } catch (e: any) {
            error = e.message || 'Failed to generate component';
        } finally {
            generating = false;
        }
    }

    let debounceTimer: ReturnType<typeof setTimeout>;

    function handleCodeChange(newCode: string) {
        codeContent = { ...codeContent, [activeTab]: newCode };
        
        // Debounce preview update
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            updatePreview();
        }, 500); // Update after 500ms of inactivity
    }
</script>

<div class="container mx-auto px-4 py-8 h-[calc(100vh-64px)] flex flex-col">
    <div class="mb-8 text-center">
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">AI Component Generator</h1>
        <p class="text-gray-600 dark:text-gray-400">Describe your component and let AI build it for you.</p>
    </div>

    <div class="flex-1 flex gap-6 min-h-0">
        <!-- Input Section -->
        <div class="w-1/3 flex flex-col gap-4">
            <div class="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm flex-1 flex flex-col">
                <label for="prompt" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Prompt
                </label>
                <textarea
                    id="prompt"
                    bind:value={prompt}
                    placeholder="e.g., A modern pricing card with a toggle for monthly/yearly billing..."
                    class="w-full h-40 p-4 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500 resize-none mb-4"
                ></textarea>

                <button
                    on:click={handleGenerate}
                    disabled={generating || !prompt.trim()}
                    class="w-full py-3 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
                >
                    {#if generating}
                        <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Generating...
                    {:else}
                        <span>✨ Generate Component</span>
                    {/if}
                </button>

                {#if error}
                    <div class="mt-4 p-3 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded-lg text-sm">
                        {error}
                    </div>
                {/if}
            </div>
        </div>

        <!-- Output Section -->
        <div class="w-2/3 flex flex-col gap-4">
            {#if codeContent.html || codeContent.css || codeContent.js}
                <div class="flex-1 flex flex-col gap-4 min-h-0">
                    <!-- Preview -->
                    <div class="h-1/2 bg-gray-100 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden relative">
                        <div class="absolute top-2 left-2 px-2 py-1 bg-black/50 text-white text-xs rounded backdrop-blur">Preview</div>
                        <iframe src={previewUrl} title="Generated Preview" class="w-full h-full border-0" />
                    </div>
                    
                    <!-- Code -->
                    <div class="h-1/2 bg-gray-900 rounded-xl border border-gray-700 overflow-hidden relative flex flex-col">
                        <div class="flex items-center bg-gray-800 border-b border-gray-700 px-2">
                            {#each ['html', 'css', 'js'] as tab}
                                <button 
                                    class="px-4 py-2 text-sm font-medium transition-colors {activeTab === tab ? 'text-white border-b-2 border-indigo-500' : 'text-gray-400 hover:text-gray-200'}"
                                    on:click={() => activeTab = tab}
                                >
                                    {tab.toUpperCase()}
                                </button>
                            {/each}
                        </div>
                        <div class="flex-1 relative">
                            <MonacoEditor 
                                value={currentCode} 
                                language={activeTab === 'js' ? 'javascript' : activeTab} 
                                readOnly={false}
                                on:change={(e) => handleCodeChange(e.detail)}
                            />
                        </div>
                    </div>
                </div>
            {:else}
                <div class="flex-1 flex items-center justify-center bg-gray-50 dark:bg-gray-800/50 rounded-xl border-2 border-dashed border-gray-200 dark:border-gray-700 text-gray-400">
                    <div class="text-center">
                        <span class="text-4xl mb-2 block">🤖</span>
                        <p>Generated component will appear here</p>
                    </div>
                </div>
            {/if}
        </div>
    </div>
</div>
