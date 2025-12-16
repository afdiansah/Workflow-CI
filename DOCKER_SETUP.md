# 🐳 Docker Hub Setup Guide

**Author:** Raifal Bagus Afdiansah  
**Project:** Heart Disease ML Model - CI/CD Pipeline

---

## 📋 Overview

Workflow ini secara otomatis:
1. ✅ Melatih 6 model ML secara paralel
2. ✅ Mengevaluasi dan memilih model terbaik
3. ✅ Build Docker image menggunakan `mlflow build-docker`
4. ✅ Push image ke Docker Hub dengan multiple tags

---

## 🚀 Setup Docker Hub

### Step 1: Buat Docker Hub Account
1. Kunjungi: https://hub.docker.com
2. Sign up atau login
3. Catat **username** Anda

### Step 2: Create Access Token
1. Login ke Docker Hub
2. Go to: **Account Settings** → **Security** → **Access Tokens**
3. Click: **New Access Token**
4. Name: `github-actions-ci`
5. Permissions: **Read, Write, Delete**
6. Click: **Generate**
7. **Copy token** (hanya tampil sekali!)

### Step 3: Add Secrets to GitHub
1. Go to repository: https://github.com/afdiansah/Workflow-CI
2. Navigate: **Settings** → **Secrets and variables** → **Actions**
3. Click: **New repository secret**

**Add 2 secrets:**

**Secret 1:**
- Name: `DOCKER_USERNAME`
- Value: `your-dockerhub-username`

**Secret 2:**
- Name: `DOCKER_PASSWORD`
- Value: `your-access-token` (dari Step 2)

---

## 🔧 Workflow Configuration

### Docker Job Details

```yaml
docker:
  name: Build and Push Docker Image
  needs: evaluate
  runs-on: ubuntu-latest
```

### What It Does:

1. **Find Best Model**
   - Reads evaluation results
   - Selects model with highest accuracy
   - Extracts model name and metrics

2. **Build Docker Image**
   - Uses `mlflow models build-docker`
   - Builds from best model run
   - Creates production-ready image

3. **Tag Images**
   - `latest` - Latest build
   - `{model-name}` - Model specific (e.g., `random-forest`)
   - `{model-name}-{date}` - Versioned (e.g., `random-forest-20241216`)

4. **Push to Docker Hub**
   - Pushes all 3 tags
   - Available publicly or privately

---

## 🐳 Docker Image Usage

### Pull Image
```bash
# Latest version
docker pull your-username/heart-disease-model:latest

# Specific model
docker pull your-username/heart-disease-model:random-forest

# Specific date version
docker pull your-username/heart-disease-model:random-forest-20241216
```

### Run Container
```bash
# Run with port mapping
docker run -p 8080:8080 your-username/heart-disease-model:latest

# Run in background
docker run -d -p 8080:8080 --name heart-disease-api your-username/heart-disease-model:latest

# Run with environment variables
docker run -p 8080:8080 \
  -e MLFLOW_TRACKING_URI=your-tracking-uri \
  your-username/heart-disease-model:latest
```

### Test API
```bash
# Health check
curl http://localhost:8080/health

# Predict
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{
    "columns": ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"],
    "data": [[63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1]]
  }'
```

---

## 📊 Workflow Output

### GitHub Actions Summary

Setelah workflow selesai, Anda akan melihat:

```
## 🐳 Docker Image Published

**Model:** Random_Forest
**Accuracy:** 0.9508

### Docker Images:
```
docker pull your-username/heart-disease-model:latest
docker pull your-username/heart-disease-model:random-forest-20241216
```

### Run Container:
```bash
docker run -p 8080:8080 your-username/heart-disease-model:latest
```
```

---

## 🔍 Verify Docker Hub

### Check on Docker Hub
1. Login to https://hub.docker.com
2. Go to **Repositories**
3. Find: `heart-disease-model`
4. Check tags:
   - ✅ latest
   - ✅ random-forest
   - ✅ random-forest-20241216

### Check Locally
```bash
# List images
docker images | grep heart-disease-model

# Inspect image
docker inspect your-username/heart-disease-model:latest

# Check image size
docker images your-username/heart-disease-model --format "{{.Repository}}:{{.Tag}} - {{.Size}}"
```

---

## 🛠️ Troubleshooting

### Error: Invalid credentials
**Solution:** Check `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets

### Error: Permission denied
**Solution:** Regenerate Docker Hub access token with correct permissions

### Error: Image push failed
**Solution:** 
- Check Docker Hub storage quota
- Verify repository exists or set to auto-create

### Error: mlflow build-docker failed
**Solution:**
- Check MLflow version (2.19.0)
- Verify model artifacts are available
- Check Python dependencies in requirements.txt

---

## 📦 Docker Image Contents

### Base Image
- Python 3.12.7
- MLflow 2.19.0
- Model dependencies (scikit-learn, pandas, numpy)

### Included Files
- ✅ Trained model artifacts
- ✅ Model metadata
- ✅ MLflow serving code
- ✅ Dependencies (requirements.txt)

### Exposed Ports
- **8080** - MLflow model serving API

### Environment Variables
- `MLFLOW_TRACKING_URI` - Optional tracking URI
- `MLFLOW_MODEL_URI` - Model location (auto-set)

---

## 🎯 Use Cases

### 1. Development Testing
```bash
docker run -p 8080:8080 your-username/heart-disease-model:latest
```

### 2. Production Deployment
```bash
docker run -d \
  --name heart-disease-prod \
  -p 80:8080 \
  --restart=always \
  your-username/heart-disease-model:random-forest-20241216
```

### 3. Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: heart-disease-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: heart-disease-api
  template:
    metadata:
      labels:
        app: heart-disease-api
    spec:
      containers:
      - name: api
        image: your-username/heart-disease-model:latest
        ports:
        - containerPort: 8080
```

### 4. Docker Compose
```yaml
version: '3.8'
services:
  api:
    image: your-username/heart-disease-model:latest
    ports:
      - "8080:8080"
    environment:
      - MLFLOW_TRACKING_URI=http://mlflow:5000
    restart: always
```

---

## 📈 Benefits

1. **Reproducibility** - Same environment everywhere
2. **Portability** - Run anywhere Docker runs
3. **Version Control** - Tagged versions for rollback
4. **CI/CD Integration** - Automated builds
5. **Easy Deployment** - One command to run
6. **Scalability** - Easy to scale with orchestrators

---

## 🔗 Related Files

- **Workflow:** `.github/workflows/main.yml`
- **Model Training:** `MLProject/modelling.py`
- **Requirements:** `MLProject/requirements.txt`
- **Artifacts Guide:** `ARTIFACTS_GUIDE.md`

---

## 📝 Notes

- Docker images auto-build setiap kali workflow berjalan
- Hanya model terbaik yang di-build jadi Docker image
- Image size sekitar 1-2 GB (tergantung model)
- Free Docker Hub: unlimited public repos, 1 private repo
- Images otomatis di-overwrite tag `latest`

---

## ✅ Checklist

- [ ] Docker Hub account created
- [ ] Access token generated
- [ ] GitHub secrets configured (`DOCKER_USERNAME`, `DOCKER_PASSWORD`)
- [ ] Workflow triggered dan berhasil
- [ ] Docker image tersedia di Docker Hub
- [ ] Image tested locally
- [ ] Documentation updated

---

## 👤 Author

**Raifal Bagus Afdiansah**  
Semester 7 - ASAH  
CI/CD Pipeline with Docker Integration
