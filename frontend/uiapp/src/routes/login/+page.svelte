<script lang="ts">
    import { api } from '$lib/api';
    import { auth } from '$lib/stores/auth';
    import { goto } from '$app/navigation';

    let email = '';
    let password = '';
    let error = '';
    let loading = false;

    async function handleLogin() {
        loading = true;
        error = '';
        
        try {
            // 1. Get Token
            const tokenRes = await api.post<any>('/auth/login/', { email, password });
            const accessToken = tokenRes.access;
            
            // 2. Get User Profile
            // We need to manually set the token in localStorage first for the api client to pick it up
            // or pass it in headers. The api wrapper might need adjustment or we just use fetch here for the second call
            // But let's try to use the auth store's login method which sets localStorage
            
            // Temporary mock user until we fetch real one, or we fetch it immediately
            // Ideally, the login response should return user data too, but simplejwt doesn't by default.
            // So we fetch /auth/me/
            
            // Manually set token for the next request
            localStorage.setItem('token', accessToken);
            
            const user = await api.get<any>('/auth/me/', { token: accessToken });
            
            auth.login(user, accessToken);
            goto('/dashboard');
            
        } catch (e: any) {
            console.error(e);
            error = 'Invalid credentials';
            localStorage.removeItem('token'); // Clean up if failed
        } finally {
            loading = false;
        }
    }
</script>

<div class="min-h-[calc(100vh-64px)] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700">
        <div>
            <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900 dark:text-white">
                Sign in to your account
            </h2>
            <p class="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
                Or <a href="/register" class="font-medium text-indigo-600 hover:text-indigo-500">create a new account</a>
            </p>
        </div>
        <form class="mt-8 space-y-6" on:submit|preventDefault={handleLogin}>
            <div class="rounded-md shadow-sm -space-y-px">
                <div>
                    <label for="email-address" class="sr-only">Email address</label>
                    <input id="email-address" name="email" type="email" autocomplete="email" required bind:value={email} class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm dark:bg-gray-700" placeholder="Email address">
                </div>
                <div>
                    <label for="password" class="sr-only">Password</label>
                    <input id="password" name="password" type="password" autocomplete="current-password" required bind:value={password} class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm dark:bg-gray-700" placeholder="Password">
                </div>
            </div>

            {#if error}
                <div class="text-red-500 text-sm text-center">{error}</div>
            {/if}

            <div>
                <button type="submit" disabled={loading} class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50">
                    {loading ? 'Signing in...' : 'Sign in'}
                </button>
            </div>
        </form>
    </div>
</div>
