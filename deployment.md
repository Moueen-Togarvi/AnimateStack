# Deployment Guide

## Frontend (SvelteKit) -> Vercel

1. **Install Vercel Adapter**
   ```bash
   npm install -D @sveltejs/adapter-vercel
   ```

2. **Update `svelte.config.js`**
   ```javascript
   import adapter from '@sveltejs/adapter-vercel';
   
   export default {
       kit: {
           adapter: adapter()
       }
   };
   ```

3. **Deploy**
   - Push code to GitHub.
   - Import project in Vercel.
   - Set Environment Variables:
     - `VITE_API_URL`: Your backend URL (e.g., https://api.animatestack.com)

## Backend (Django) -> Fly.io / Railway

1. **Prepare for Production**
   - Install `gunicorn` and `psycopg2-binary`.
   - Create `Procfile`:
     ```
     web: gunicorn core.wsgi:application
     ```

2. **Environment Variables**
   - `DEBUG`: False
   - `SECRET_KEY`: <secure-random-key>
   - `DATABASE_URL`: postgres://user:pass@host:port/db
   - `ALLOWED_HOSTS`: .animatestack.com
   - `CORS_ALLOWED_ORIGINS`: https://animatestack.com
   - `OPENAI_API_KEY`: <your-key>

3. **Database (PostgreSQL)**
   - Use a managed Postgres service (Neon, Supabase, or Railway).
   - Update `settings.py` to use `dj-database-url`.

4. **Static Files**
   - Use WhiteNoise for serving static files, or configure S3 storage.

## Docker (Optional)

Use the provided `docker-compose.yml` for a full local stack or containerized deployment.
