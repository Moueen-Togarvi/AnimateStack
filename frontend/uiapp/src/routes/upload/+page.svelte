<script lang="ts">
    import { onMount } from 'svelte';
    import { api } from '$lib/api';
    import MonacoEditor from '$lib/components/editor/MonacoEditor.svelte';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';

    let title = '';
    let description = '';
    let price = 0;
    let activeTab = 'html';
    let codeContent = { html: '', css: '', js: '' };
    let previewUrl = '';
    let submitting = false;
    let error = '';

    onMount(() => {
        const isDraft = $page.url.searchParams.get('draft');
        if (isDraft) {
            const draft = localStorage.getItem('draft_component');
            if (draft) {
                const data = JSON.parse(draft);
                title = data.title;
                description = data.description;
                codeContent = data.code_content;
                updatePreview();
                localStorage.removeItem('draft_component');
            }
        }
    });

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

    function handleCodeChange(newCode: string) {
        codeContent = { ...codeContent, [activeTab]: newCode };
        // Debounce could be added here
        updatePreview();
    }

    async function handleSubmit() {
        if (!title || !description) {
            error = 'Title and description are required';
            return;
        }

        submitting = true;
        error = '';

        try {
            await api.post('/components/', {
                title,
                description,
                price,
                code_content: codeContent,
                is_public: true
            });
            goto('/dashboard');
        } catch (e: any) {
            error = e.message || 'Failed to upload component';
        } finally {
            submitting = false;
        }
    }
</script>

<div class="container mx-auto px-4 py-8 flex flex-col h-[calc(100vh-64px)]">
    <div class="flex items-center justify-between mb-6">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Upload Component</h1>
        <button 
            on:click={handleSubmit}
            disabled={submitting}
            class="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50"
        >
            {submitting ? 'Uploading...' : 'Submit for Approval'}
        </button>
    </div>

    {#if error}
        <div class="mb-4 p-4 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded-lg">
            {error}
        </div>
    {/if}

    <div class="flex-1 flex gap-6 min-h-0">
        <!-- Form Section -->
        <div class="w-1/3 flex flex-col gap-4 overflow-y-auto pr-2">
            <div class="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
                <div class="mb-4">
                    <label for="title" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Title</label>
                    <input 
                        type="text" 
                        id="title" 
                        bind:value={title}
                        class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500"
                        placeholder="e.g., Glassmorphism Card"
                    />
                </div>

                <div class="mb-4">
                    <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Description</label>
                    <textarea 
                        id="description" 
                        bind:value={description}
                        rows="4"
                        class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500 resize-none"
                        placeholder="Describe your component..."
                    ></textarea>
                </div>

                <div class="mb-4">
                    <label for="price" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Price ($)</label>
                    <input 
                        type="number" 
                        id="price" 
                        bind:value={price}
                        min="0"
                        step="0.01"
                        class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500"
                    />
                    <p class="text-xs text-gray-500 mt-1">Leave as 0 for free components</p>
                </div>
            </div>
        </div>

        <!-- Editor & Preview -->
        <div class="w-2/3 flex flex-col gap-4">
            <div class="flex-1 flex flex-col gap-4 min-h-0">
                <!-- Preview -->
                <div class="h-1/2 bg-gray-100 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden relative flex items-center justify-center">
                    <div class="absolute top-2 left-2 px-2 py-1 bg-black/50 text-white text-xs rounded backdrop-blur z-10">Preview</div>
                    <iframe src={previewUrl} title="Preview" class="w-full h-full border-0" />
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
        </div>
    </div>
</div>
