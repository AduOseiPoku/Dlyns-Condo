# 🚀 Deploying Dlyns Condo on Dokploy

This project is pre-configured with a production-ready `Dockerfile`, `WhiteNoise` asset compression, reverse-proxy headers for Traefik, PostgreSQL support, and an automated startup sequence (`entrypoint.sh`).

---

## 📋 Step-by-Step Dokploy Setup

### 1. Push Your Code to Git
Make sure your project repository is pushed to your Git provider (**GitHub**, **GitLab**, or **Gitea**).

---

### 2. (Optional but Recommended) Create a PostgreSQL Database
1. In your **Dokploy** dashboard, click **Databases** → **Create Database**.
2. Select **PostgreSQL**.
3. Once running, copy the internal connection string:
   ```text
   postgres://username:password@postgres-service:5432/database_name
   ```

---

### 3. Create the Web Application in Dokploy
1. In your project, click **Applications** → **Create Application**.
2. **Name**: `dlyns-condo`
3. **Source**: Select your Git repository and branch (`main` or `master`).
4. **Build Type**: Select **Dockerfile**.
5. **Port**: Set to `8000`.

---

### 4. Configure Environment Variables
In the **Environment** tab of your Dokploy application, paste the following:

```ini
SECRET_KEY=generate-a-strong-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,*.dokploy.host
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://*.dokploy.host

# Database (if using PostgreSQL created in Step 2):
DATABASE_URL=postgres://username:password@postgres-service:5432/database_name

# Automatic Admin User on First Launch:
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=YourSecurePassword123!
DJANGO_SUPERUSER_EMAIL=reservations@dlynscondo.com
```

---

### 5. Attach Persistent Volume for Media Uploads (Optional)
If you plan to upload photos directly through the `/admin/` panel:
* Go to the **Volumes** / **Storage** tab.
* Mount a volume:
  * **Host Path**: `dlyns-condo-media`
  * **Mount Path in Container**: `/app/media`
*(Static files like CSS, JS, and default imagery are compiled into the image and do not need a volume).*

---

### 6. Add Custom Domain & SSL (HTTPS)
1. Go to the **Domains** tab in Dokploy.
2. Enter your domain (e.g. `dlynscondo.com`).
3. Set **Certificate**: **Let's Encrypt** (automatic free SSL).
4. Point your DNS `A` record at your server's IP address.

---

### 7. Click "Deploy" 🎉
Dokploy will:
1. Build the Docker container.
2. Run `collectstatic` to compress static assets.
3. Automatically run migrations (`python manage.py migrate`).
4. Auto-seed initial Koforidua-Apenkwa suites and settings if the database is fresh.
5. Create your admin superuser credentials if provided.
6. Start Gunicorn with live healthchecks at `/health/`.

---

## 🛠️ Accessing the App After Deployment
* **Public Website:** `https://yourdomain.com`
* **Host Admin Desk:** `https://yourdomain.com/admin/`
* **Health Check:** `https://yourdomain.com/health/`
