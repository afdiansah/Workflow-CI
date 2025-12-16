# 🔧 Troubleshooting Docker Hub Login Error

**Error:** `Username and password required`

---

## ✅ Solusi Cepat

### Step 1: Verifikasi Secrets di GitHub

1. Buka repository di GitHub
2. Go to: **Settings** → **Secrets and variables** → **Actions**
3. Pastikan ada 2 secrets:
   - ✅ `DOCKER_USERNAME`
   - ✅ `DOCKER_PASSWORD`

**PENTING:** Nama secret harus **PERSIS** seperti di atas (huruf besar semua, ada underscore).

---

### Step 2: Periksa Nama Secret

❌ **SALAH:**
- `docker_username` (huruf kecil)
- `DOCKERHUB_USERNAME` (ada HUB)
- `DOCKER_USER` (tidak ada NAME)
- `Docker_Username` (mixed case)

✅ **BENAR:**
- `DOCKER_USERNAME` ← Copy paste ini
- `DOCKER_PASSWORD` ← Copy paste ini

---

### Step 3: Regenerate Docker Hub Token

Jika sudah yakin nama secret benar tapi masih error:

1. **Login ke Docker Hub:** https://hub.docker.com
2. **Go to:** Account Settings → Security → Access Tokens
3. **Delete** token lama jika ada
4. **Create New Access Token:**
   - Name: `github-actions-ci`
   - Permissions: **Read, Write, Delete** ✅
5. **Copy token** (hanya muncul sekali!)
6. **Update secret di GitHub:**
   - Settings → Secrets → DOCKER_PASSWORD
   - Paste token baru

---

### Step 4: Re-run Workflow

```bash
# Method 1: Via GitHub UI
# Go to Actions → Failed workflow → Re-run all jobs

# Method 2: Via push
git commit --allow-empty -m "chore: trigger workflow"
git push origin main

# Method 3: Manual dispatch
# Actions → ML Training Pipeline → Run workflow
```

---

## 🔍 Debug Checklist

### A. Verify Secret Names
```bash
# SSH ke runner atau check workflow logs
# Secrets harus bernama PERSIS:
DOCKER_USERNAME=your-username
DOCKER_PASSWORD=dckr_pat_xxxxxxxxxxxxx
```

### B. Check Secret Values

**DOCKER_USERNAME:**
- [ ] Huruf kecil semua? (Docker Hub usernames lowercase)
- [ ] Tidak ada spasi
- [ ] Sama dengan username di hub.docker.com

**DOCKER_PASSWORD:**
- [ ] Token dimulai dengan `dckr_pat_`
- [ ] Tidak ada spasi atau newline
- [ ] Token masih valid (tidak expired/deleted)

### C. Test Locally

```bash
# Test login secara manual
echo "YOUR_TOKEN" | docker login -u YOUR_USERNAME --password-stdin

# Jika berhasil, berarti credentials valid
# Jika gagal, regenerate token
```

---

## 📸 Screenshot Cara Setup

### 1. Docker Hub - Generate Token

```
hub.docker.com → Account Settings → Security → Access Tokens

┌─────────────────────────────────────────────┐
│ New Access Token                             │
├─────────────────────────────────────────────┤
│ Description: github-actions-ci               │
│ Access permissions:                          │
│   ☑ Read                                    │
│   ☑ Write                                   │
│   ☑ Delete                                  │
│                                              │
│ [Generate Token]                            │
└─────────────────────────────────────────────┘

Copy token: dckr_pat_aBcDeFgHiJkLmNoPqRsTuVwXyZ
```

### 2. GitHub - Add Secrets

```
Repository → Settings → Secrets and variables → Actions

┌─────────────────────────────────────────────┐
│ Actions secrets                              │
├─────────────────────────────────────────────┤
│ Name: DOCKER_USERNAME                        │
│ Secret: your-dockerhub-username              │
│ [Add secret]                                 │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Actions secrets                              │
├─────────────────────────────────────────────┤
│ Name: DOCKER_PASSWORD                        │
│ Secret: dckr_pat_aBcDeFgHiJkLmNoPqRsTuVwXyZ  │
│ [Add secret]                                 │
└─────────────────────────────────────────────┘
```

---

## ⚠️ Common Mistakes

### Mistake 1: Typo di Nama Secret
```yaml
# Di workflow:
username: ${{ secrets.DOCKER_USERNAME }}

# Tapi di GitHub namanya:
DOCKERHUB_USERNAME  ❌ (ada HUB)
```

**Fix:** Pastikan nama secret PERSIS `DOCKER_USERNAME`

### Mistake 2: Password Bukan Token
```bash
# SALAH: Menggunakan password Docker Hub
DOCKER_PASSWORD=mypassword123  ❌

# BENAR: Menggunakan access token
DOCKER_PASSWORD=dckr_pat_xxxxx  ✅
```

**Fix:** Generate access token, jangan pakai password

### Mistake 3: Token Expired
```bash
# Token Docker Hub bisa expire atau dihapus
# Generate token baru dan update secret
```

### Mistake 4: Repository Access
```bash
# Pastikan workflow punya akses ke secrets
# Check: Settings → Actions → General → Workflow permissions
# Harus: Read and write permissions ✅
```

---

## 🧪 Test Secrets

Tambahkan step temporary di workflow untuk debug:

```yaml
- name: Debug Docker Secrets
  run: |
    if [ -z "${{ secrets.DOCKER_USERNAME }}" ]; then
      echo "❌ DOCKER_USERNAME is empty!"
    else
      echo "✅ DOCKER_USERNAME is set"
      # Don't print the actual value!
    fi
    
    if [ -z "${{ secrets.DOCKER_PASSWORD }}" ]; then
      echo "❌ DOCKER_PASSWORD is empty!"
    else
      echo "✅ DOCKER_PASSWORD is set (length: ${#DOCKER_PASSWORD})"
    fi
  env:
    DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
```

**PENTING:** Jangan pernah print secret value! Hanya check apakah empty atau tidak.

---

## 🆘 Masih Error?

### Option 1: Skip Docker Job (Temporary)

Jika ingin training jalan tanpa Docker:

```yaml
# Di workflow main.yml, comment/hapus Docker job
# Atau ubah kondisi if menjadi:
if: false  # Temporary disable
```

### Option 2: Manual Docker Build

Build Docker image secara manual setelah training:

```bash
# Download artifacts dari GitHub
# Build locally:
cd MLProject
mlflow models build-docker -m runs:/RUN_ID/model -n heart-disease-model

# Push manual:
docker tag heart-disease-model:latest your-username/heart-disease-model:latest
docker login
docker push your-username/heart-disease-model:latest
```

### Option 3: Contact Support

1. Check GitHub Actions logs: Actions → Failed run → docker job
2. Copy error message lengkap
3. Check Docker Hub status: https://status.docker.com
4. Verify GitHub Actions status: https://www.githubstatus.com

---

## ✅ Verification

Setelah fix, pastikan:

- [ ] Workflow runs tanpa error
- [ ] Docker job shows "✅ Docker Hub credentials are configured"
- [ ] Docker login successful
- [ ] Image built successfully
- [ ] Image pushed ke Docker Hub
- [ ] Image visible di hub.docker.com

---

## 📞 Quick Commands

```bash
# Check if secrets are set (di GitHub UI)
Settings → Secrets → Check DOCKER_USERNAME dan DOCKER_PASSWORD ada

# Re-run workflow
git commit --allow-empty -m "test: docker credentials"
git push origin main

# Test Docker login locally
docker login -u YOUR_USERNAME
# Enter token when prompted

# Verify image on Docker Hub
docker pull your-username/heart-disease-model:latest
```

---

## 📖 Related Docs

- [DOCKER_SETUP.md](DOCKER_SETUP.md) - Full Docker Hub setup guide
- [README.md](README.md) - Main documentation
- [GitHub Secrets Docs](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Docker Hub Tokens](https://docs.docker.com/docker-hub/access-tokens/)

---

**Paling Sering:** Nama secret typo atau token belum di-generate. Double check nama secret di GitHub!
