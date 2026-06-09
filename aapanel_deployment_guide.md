# Odoo Deployment Guide for AWS aaPanel

Deploying Odoo on aaPanel can be done in two ways. **Method 1 (Docker)** is highly recommended because Odoo has complex system dependencies (like `wkhtmltopdf`, specific PostgreSQL versions, and Python C-extensions) that are tedious to set up manually on aaPanel. 

Before proceeding with either method, you must **update your `odoo.conf` file** on your server, as it currently contains a Windows file path (`C:\odoo\custom_addons`) which will cause errors on your Linux-based aaPanel server.

Change your `addons_path` in `odoo.conf` on the server to look like this:
```ini
[options]
admin_passwd = your_secure_admin_password
db_host = postgres
db_port = 5432
db_user = odoo
db_password = your_secure_db_password
addons_path = /mnt/extra-addons
http_port = 8069
```

---

## Method 1: Using Docker (Highly Recommended)

aaPanel has a great Docker module that makes running Odoo trivial and isolates it from the rest of your server.

### 1. Install Docker in aaPanel
1. Go to your aaPanel **App Store**.
2. Search for **Docker** (or Docker Manager) and click **Install**.

### 2. Create a `docker-compose.yml` file
In the root directory of your cloned Odoo repo on the server (e.g., `/www/wwwroot/your_odoo_domain`), create a file named `docker-compose.yml` and add the following:

```yaml
version: '3.1'
services:
  web:
    image: odoo:16.0 # Change this to your Odoo version (e.g. 15.0, 17.0)
    depends_on:
      - postgres
    ports:
      - "8069:8069"
    volumes:
      - ./addons:/mnt/extra-addons
      - ./custom_addons:/mnt/extra-addons2
      - ./odoo.conf:/etc/odoo/odoo.conf
      - odoo-web-data:/var/lib/odoo
    environment:
      - HOST=postgres
      - USER=odoo
      - PASSWORD=my_secure_password

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=my_secure_password
      - POSTGRES_USER=odoo
    volumes:
      - odoo-db-data:/var/lib/postgresql/data

volumes:
  odoo-web-data:
  odoo-db-data:
```
*Note: Make sure the `PASSWORD` matches in both services and in your `odoo.conf`.*

### 3. Start the Application
Connect to your AWS server via SSH (or use the aaPanel Terminal), navigate to your repository, and start Docker:
```bash
cd /www/wwwroot/your_odoo_repo_folder
docker compose up -d
```
Odoo will now be running on port `8069`. You can use aaPanel's **Website** > **Add site** feature to set up a reverse proxy pointing your domain to `http://127.0.0.1:8069`.

---

## Method 2: Manual Setup via Python Manager

If you absolutely must run it natively using aaPanel's Python Manager:

### 1. Install Required Services in aaPanel
- **PostgreSQL**: Install PostgreSQL Manager from the aaPanel App Store. Create a new database user `odoo` and a database.
- **Python Manager**: Install Python Manager from the App Store.

### 2. Install System Dependencies
Odoo requires several system packages. Open the aaPanel terminal and run:
```bash
sudo apt update
sudo apt install python3-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev \
    libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev libfreetype6-dev \
    liblcms2-dev libwebp-dev libharfbuzz-dev libfribidi-dev libxcb1-dev libpq-dev
```

### 3. Install Wkhtmltopdf
Odoo needs this specific tool to generate PDF reports:
```bash
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
sudo apt install ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb
```

### 4. Setup Python Environment via aaPanel
1. Open **Python Manager** in aaPanel.
2. Click **Add Project**.
3. **Project Path**: Select your cloned repository folder.
4. **Startup File**: Select `odoo-bin`.
5. **Port**: 8069
6. **Requirements**: Select `requirements.txt` from the repo.
7. Click **Confirm**. aaPanel will create a virtual environment and install the dependencies.

### 5. Configure `odoo.conf`
Ensure your `odoo.conf` looks like this:
```ini
[options]
admin_passwd = admin
db_host = 127.0.0.1
db_port = 5432
db_user = odoo
db_password = your_postgres_password
addons_path = /www/wwwroot/your_repo/addons,/www/wwwroot/your_repo/custom_addons
http_port = 8069
```

### 6. Run Odoo
You can start the project from within the Python Manager. If it fails, check the project logs in the Python Manager to identify missing Python dependencies and install them manually via the terminal in the venv (e.g. `/www/wwwroot/your_repo/venv/bin/pip install ...`).
