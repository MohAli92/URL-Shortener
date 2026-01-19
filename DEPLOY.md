# Deployment Guide

This repository includes a `deploy` job in `.github/workflows/ci.yml` that copies the project to a remote server and runs Docker to build and start the app.

## Required GitHub Secrets
Set the following Secrets in your repository (Settings → Secrets → Actions):

- `SSH_HOST`: Remote server hostname or IP
- `SSH_USER`: SSH username
- `SSH_KEY`: SSH private key (PEM format) for `SSH_USER` — add without a passphrase or configure agent forwarding
- `SSH_PORT` (optional): SSH port (default: 22)
- `DEPLOY_PATH`: Absolute path on the remote host where files will be uploaded (e.g. `/home/ubuntu/url-shortener`)

## Prepare the Remote Server (minimal)

1. Create a deploy user and enable SSH key authentication:

```bash
sudo adduser deploy
sudo usermod -aG docker deploy
mkdir -p /home/deploy/.ssh
chmod 700 /home/deploy/.ssh
# paste the public key into /home/deploy/.ssh/authorized_keys
chmod 600 /home/deploy/.ssh/authorized_keys
chown -R deploy:deploy /home/deploy/.ssh
```

2. Install Docker (Ubuntu example):

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable --now docker
```

3. Add the repository Secrets listed above in GitHub.

4. Push to `main` (or open a PR) to run the CI pipeline. The `deploy` job will:
- SCP the repository to `DEPLOY_PATH`
- SSH into the host, run `docker build` and `docker run` to start the container on port 80 forwarding to Flask's port

## Notes
- The workflow uses `appleboy/scp-action` and `appleboy/ssh-action` to transfer files and run remote commands.
- For safer deploys, consider using a registry + `docker pull`, `docker-compose`, or orchestrator for zero-downtime updates.
