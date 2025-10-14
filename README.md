# secure_voting_app
secure_voting_app_basic

## Running PostgreSQL in GitHub Codespaces

GitHub Codespaces does not support running Docker containers directly inside the codespace. Instead, use the built-in PostgreSQL service provided by Codespaces, or connect to a remote/local PostgreSQL instance.

### Option 1: Use Codespaces PostgreSQL Dev Service

1. Open the Codespaces configuration (gear icon > "Add Dev Service").
2. Add the PostgreSQL service and configure:
	- Username: `postgres`
	- Password: `password`
	- Database: `voting_db`
	- Port: `5432`
3. Update your `.env` file if needed:
	```env
	DATABASE_URL=postgresql://postgres:password@localhost:5432/voting_db
	```

### Option 2: Connect to a Remote or Local PostgreSQL

If you have PostgreSQL running on your local machine or a remote server, update your `.env` file with the correct host and credentials.

### Option 3: Use a Managed PostgreSQL Service

You can use cloud providers like AWS RDS, Azure Database, or Google Cloud SQL. Update your `.env` file with the connection string provided by your service.

---

## Docker Installation (Debian-based Linux)

To install Docker, run the following commands:

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
	"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
	$(lsb_release -cs) stable" | \
	sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

After installation, verify Docker is installed:

```bash
docker --version
```
