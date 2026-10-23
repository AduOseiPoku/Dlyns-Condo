# Dlyns Condo — Luxury Serviced Residence & Hotel Website

A high-converting dynamic hotel/condo web application built with **Django 5**, **Tailwind CSS**, and **Alpine.js**, structured around the **"Call-to-Book" & WhatsApp Inquiry** hospitality model (no online payment gateway headaches).

---

## 🌟 Key Highlights & Architecture

- **High-Converting Booking Channels:**
  1. **Direct Click-to-Call (`tel:`)**: Integrated header and mobile sticky action bar.
  2. **1-Click WhatsApp Booking**: Dynamic pre-filled reservation messages.
  3. **"Request a Stay" Inquiry Engine**: Validated booking forms logged directly into the database.
- **Manager Control Panel (`/admin`):**
  - Instant lead tracking with status badges (`🟡 New Lead`, `🔵 Called`, `🟢 Confirmed`, `⚪ Cancelled`).
  - Clickable 📞 **Direct Call** and 💬 **WhatsApp** buttons next to each guest lead.
  - Zero-code content editing for prices, descriptions, photos, and amenities.
- **Production & Dokploy Ready:**
  - Includes `Dockerfile`, `.dockerignore`, and `WhiteNoise` for static asset compression.
  - One-click deployable to Dokploy, Railway, Render, or any VPS with Docker.

---

## 🚀 Running Locally on Your Computer

### 1. Start the Server
Open your terminal in this directory (`d:\Dlyns Condo`) and run:

```bash
python manage.py runserver
```

### 2. View the Website
- **Public Guest Website:** Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Host Admin Panel:** Open [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

### 3. Default Host Admin Login
- **Username:** `admin`
- **Password:** `admin12345`
*(You can change this password anytime in the Django admin under Users).*

---

## 🛠️ Management Commands

- **Seed Demo Suites & Amenities:**
  ```bash
  python manage.py seed_data
  ```
- **Create a New Admin User:**
  ```bash
  python manage.py createsuperuser
  ```
- **Make Database Migrations:**
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

---

## 🚢 Deploying to Dokploy

1. Push this folder to your Git repository (GitHub / GitLab).
2. In your **Dokploy** dashboard:
   - Click **Create Application** → Select your Git repository.
   - Choose **Build Type**: `Dockerfile`.
   - Set **Port** to `8000`.
3. Add your **Environment Variables** in Dokploy:
   ```ini
   SECRET_KEY=generate-a-strong-random-key
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,*.dokploy.host
   CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
   # If using Dokploy's 1-click PostgreSQL database:
   DATABASE_URL=postgres://user:password@postgres-service:5432/dlyns_condo_db
   ```
4. In the **Domains** tab, add your domain name (`dlynscondo.com`). Dokploy will automatically generate a free **Let's Encrypt SSL (HTTPS)** certificate.
5. Click **Deploy**!
