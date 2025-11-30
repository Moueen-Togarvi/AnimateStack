<script lang="ts">
    import { api } from '$lib/api';
    import { goto } from '$app/navigation';

    let file: File | null = null;
    let assetType = '3d';
    let uploading = false;

    async function handleUpload() {
        if (!file) return;
        
        uploading = true;
        const formData = new FormData();
        formData.append('file', file);
        formData.append('asset_type', assetType);

        try {
            // We need a custom fetch here because our api wrapper assumes JSON
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:8000/api/assets/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            if (response.ok) {
                goto('/assets');
            } else {
                alert('Upload failed');
            }
        } catch (e) {
            console.error(e);
            alert('Upload error');
        } finally {
            uploading = false;
        }
    }
</script>

<div class="container mx-auto px-4 py-8 max-w-xl">
    <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-8">Upload Asset</h1>

    <div class="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700">
        <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Asset Type</label>
            <select bind:value={assetType} class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white">
                <option value="3d">3D Model (GLTF/GLB)</option>
                <option value="image">Image</option>
                <option value="lottie">Lottie Animation</option>
            </select>
        </div>

        <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">File</label>
            <input 
                type="file" 
                accept=".glb,.gltf,.png,.jpg,.json"
                on:change={(e) => file = e.currentTarget.files?.[0] || null}
                class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white"
            />
        </div>

        <button 
            on:click={handleUpload} 
            disabled={!file || uploading}
            class="w-full py-3 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white rounded-lg font-medium transition-colors"
        >
            {uploading ? 'Uploading...' : 'Upload Asset'}
        </button>
    </div>
</div>
