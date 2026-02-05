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
    let showPrompt = true;

    $: currentCode = codeContent[activeTab as keyof typeof codeContent];

    function updatePreview() {
        const { html, css, js } = codeContent;
        const blob = new Blob([`
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <script src="https://cdn.tailwindcss.com"><\/script>
                <style>
                    body { margin: 0; padding: 20px; min-height: 100vh; display: flex; align-items: center; justify-content: center; background: transparent; }
                    ${css}
                </style>
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
        // Don't clear codeContent immediately to keep context, or clear if new generation
        // codeContent = { html: '', css: '', js: '' }; 

        try {
            const response = await api.post<any>('/ai/generate/', { prompt });
            
            if (!response.code_content) {
                throw new Error('Invalid response from AI: Missing code_content');
            }
            
            codeContent = response.code_content;
            updatePreview();
            showPrompt = false; // Auto-hide prompt on success to show full view

        } catch (e: any) {
            error = e.message || 'Failed to generate component';
        } finally {
            generating = false;
        }
    }

    let debounceTimer: ReturnType<typeof setTimeout>;

    function handleCodeChange(newCode: string) {
        codeContent = { ...codeContent, [activeTab]: newCode };
        
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            updatePreview();
        }, 500);
    }
</script>

<div class="pt-20 h-screen flex flex-col box-border overflow-hidden bg-[#1e1e1e]">
    <!-- Main Workspace -->
    <div class="flex-1 flex min-h-0">
        
        <!-- Left: Preview Area (Browser Viewport) -->
        <div class="flex-1 relative bg-gray-900 flex flex-col min-w-0">
            <!-- Browser Toolbar Mockup -->
            <div class="h-10 bg-[#2d2d2d] flex items-center px-4 gap-4 border-b border-black">
                <div class="flex gap-2">
                    <div class="w-3 h-3 rounded-full bg-red-500"></div>
                    <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
                    <div class="w-3 h-3 rounded-full bg-green-500"></div>
                </div>
                <div class="flex-1 bg-[#1e1e1e] h-6 rounded-md flex items-center px-3 text-xs text-gray-400 font-mono">
                    localhost:3000/preview
                </div>
            </div>

            <!-- Iframe Container -->
            <div class="flex-1 relative bg-[url('/grid.svg')] bg-center overflow-hidden">
                {#if previewUrl}
                    <iframe src={previewUrl} title="Preview" class="w-full h-full border-0" />
                {:else}
                    <div class="absolute inset-0 flex items-center justify-center text-gray-600">
                        <div class="text-center">
                            <p class="text-xl">No Preview</p>
                            <p class="text-sm">Generate a component to see it here</p>
                        </div>
                    </div>
                {/if}
            </div>

            <!-- Floating Prompt Bar -->
            <div class="absolute bottom-8 left-1/2 -translate-x-1/2 w-full max-w-2xl px-4 z-20">
                <div class="bg-black/80 backdrop-blur-xl border border-white/10 rounded-2xl p-2 shadow-2xl flex flex-col gap-2 transition-all duration-300 {showPrompt ? 'translate-y-0 opacity-100' : 'translate-y-[120%] opacity-0 pointer-events-none'}">
                    <div class="relative flex items-center">
                        <textarea
                            bind:value={prompt}
                            placeholder="Describe your component..."
                            class="w-full pl-4 pr-12 py-3 bg-transparent text-white placeholder-gray-500 focus:outline-none resize-none h-12 max-h-32"
                            on:keydown={(e) => { if(e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleGenerate(); } }}
                        ></textarea>
                        <button
                            on:click={handleGenerate}
                            disabled={generating || !prompt.trim()}
                            class="absolute right-2 p-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg disabled:opacity-50 transition-colors"
                        >
                            {#if generating}
                                <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                            {:else}
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                            {/if}
                        </button>
                    </div>
                    {#if error}
                        <div class="px-4 pb-2 text-xs text-red-400">{error}</div>
                    {/if}
                </div>
                <!-- Toggle Button -->
                <button 
                    class="absolute bottom-0 right-4 translate-y-full mt-2 p-2 bg-black/50 hover:bg-black/80 text-white rounded-full backdrop-blur border border-white/10 transition-all"
                    on:click={() => showPrompt = !showPrompt}
                    title="Toggle Prompt"
                >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path></svg>
                </button>
            </div>
        </div>

        <!-- Right: Editor Area (DevTools Style) -->
        <div class="w-[500px] bg-[#202124] border-l border-[#3e3e3e] flex flex-col shadow-xl z-10">
            <!-- DevTools Tabs -->
            <div class="flex items-center bg-[#2d2d2d] border-b border-[#1e1e1e]">
                {#each ['html', 'css', 'js'] as tab}
                    <button 
                        class="px-4 py-2 text-xs font-medium border-b-2 transition-colors {activeTab === tab ? 'text-[#a8c7fa] border-[#a8c7fa] bg-[#202124]' : 'text-[#9aa0a6] border-transparent hover:bg-[#35363a] hover:text-[#e8eaed]'}"
                        on:click={() => activeTab = tab}
                    >
                        {tab.toUpperCase()}
                    </button>
                {/each}
                <div class="flex-1"></div>
                <button 
                    on:click={() => {
                        localStorage.setItem('draft_component', JSON.stringify({
                            title: prompt.slice(0, 50) || 'AI Generated Component',
                            description: `Generated from prompt: ${prompt}`,
                            code_content: codeContent
                        }));
                        window.location.href = '/upload?draft=true';
                    }}
                    class="mx-2 px-3 py-1 text-xs font-bold bg-[#35363a] hover:bg-[#45464a] text-[#8ab4f8] rounded border border-[#5f6368] transition-colors"
                >
                    Publish
                </button>
            </div>

            <!-- Editor Content -->
            <div class="flex-1 relative">
                <MonacoEditor 
                    value={currentCode} 
                    language={activeTab === 'js' ? 'javascript' : activeTab} 
                    readOnly={false}
                    on:change={(e) => handleCodeChange(e.detail)}
                />
            </div>
            
            <!-- DevTools Status Bar -->
            <div class="h-6 bg-[#2d2d2d] border-t border-[#1e1e1e] flex items-center px-2 text-[10px] text-[#9aa0a6]">
                <span>Console</span>
                <span class="mx-2">|</span>
                <span>What's New</span>
                <div class="flex-1"></div>
                <span>Ln 1, Col 1</span>
            </div>
        </div>
    </div>
</div>
