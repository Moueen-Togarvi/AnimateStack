<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    
    export let code_content: { html: string; css: string; js: string };
    export let scale: number = 0.75;
    
    let previewUrl = '';
    
    function generatePreview() {
        const { html, css, js } = code_content;
        const blob = new Blob([`
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <script src="https://cdn.tailwindcss.com"><\/script>
                <style>
                    body {
                        margin: 0;
                        padding: 20px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        min-height: 100vh;
                        background: transparent;
                    }
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
    
    onMount(() => {
        if (code_content) {
            generatePreview();
        }
    });
    
    onDestroy(() => {
        if (previewUrl) URL.revokeObjectURL(previewUrl);
    });
    
    $: if (code_content) generatePreview();
</script>

{#if previewUrl}
    <iframe 
        src={previewUrl} 
        title="Component Preview" 
        class="w-full h-full border-0 pointer-events-none origin-center"
        style="transform: scale({scale}); transform-origin: center;"
    />
{:else}
    <div class="w-full h-full flex items-center justify-center text-gray-400 text-sm">
        No Preview Available
    </div>
{/if}
