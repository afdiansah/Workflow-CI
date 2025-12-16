# ✅ Setup Checklist - CI/CD dengan Docker Hub

**Project:** Heart Disease ML Pipeline  
**Author:** Raifal Bagus Afdiansah

---

## 📋 Pre-requisites

- [ ] Repository GitHub sudah dibuat
- [ ] Dataset `Heart_Disease_preprocessing.csv` tersedia
- [ ] File `modelling.py` dan `requirements.txt` siap
- [ ] Git installed dan configured

---

## 🔧 1. Repository Setup

- [ ] Clone repository atau init git
  ```bash
  git clone <your-repo-url>
  cd Workflow-CI
  ```

- [ ] Struktur folder sudah benar:
  ```
  ├── .github/workflows/main.yml
  ├── MLProject/
  │   ├── Heart_Disease_preprocessing.csv
  │   ├── modelling.py
  │   └── requirements.txt
  ```

- [ ] Push ke GitHub
  ```bash
  git add .
  git commit -m "Initial commit"
  git push -u origin main
  ```

---

## 🔐 2. GitHub Secrets Setup

### Option A: MLflow Tracking (Optional)

Jika ingin tracking ke DagsHub/MLflow server:

- [ ] Buat account di DagsHub atau setup MLflow server
- [ ] Add secrets di GitHub:
  - [ ] `MLFLOW_TRACKING_URI`
  - [ ] `MLFLOW_TRACKING_USERNAME`
  - [ ] `MLFLOW_TRACKING_PASSWORD`

**Path:** Repository → Settings → Secrets and variables → Actions

### Option B: Docker Hub (Required untuk Docker deployment)

- [ ] **Buat Docker Hub account**
  - URL: https://hub.docker.com
  - [ ] Register/Login
  - [ ] Catat username

- [ ] **Generate Access Token**
  - [ ] Go to: Account Settings → Security
  - [ ] Click: New Access Token
  - [ ] Name: `github-actions-ci`
  - [ ] Permissions: **Read, Write, Delete**
  - [ ] **Copy token** (save di notepad, hanya muncul sekali!)

- [ ] **Add secrets di GitHub**
  - [ ] Repository → Settings → Secrets and variables → Actions
  - [ ] Click: New repository secret
  - [ ] Secret 1:
    - Name: `DOCKER_USERNAME`
    - Value: `your-dockerhub-username`
  - [ ] Secret 2:
    - Name: `DOCKER_PASSWORD`
    - Value: `your-access-token` (dari step sebelumnya)
  - [ ] Save both secrets

---

## 🚀 3. Workflow Trigger

### Test Manual Trigger

- [ ] Go to repository → Actions tab
- [ ] Select "ML Training Pipeline"
- [ ] Click "Run workflow"
- [ ] Select branch: `main`
- [ ] Click green "Run workflow" button

### Monitor Workflow

- [ ] Wait for workflow to start (~30 seconds)
- [ ] Check jobs:
  - [ ] ✅ Setup Environment
  - [ ] ✅ Train ML Models (6 parallel jobs)
  - [ ] ✅ Evaluate and Compare Models
  - [ ] ✅ Build and Push Docker Image
  - [ ] ✅ Notification

### Expected Duration
- Training: ~5-8 minutes
- Docker build & push: ~2-5 minutes
- **Total: 10-15 minutes**

---

## 📦 4. Verify Artifacts

### GitHub Actions Artifacts (Temporary)

- [ ] Scroll to bottom of workflow run
- [ ] Check section "Artifacts"
- [ ] Download artifacts:
  - [ ] `model-Random_Forest`
  - [ ] `model-Gradient_Boosting`
  - [ ] `model-Logistic_Regression`
  - [ ] `final-comparison`
  - [ ] logs (if failed)

### GitHub Branch Artifacts (Permanent)

- [ ] Go to repository
- [ ] Switch branch to: `artifacts`
- [ ] Check files:
  - [ ] `final_model_comparison.csv`
  - [ ] `README.md` (with run metadata)
  - [ ] Model artifacts dari semua models

---

## 🐳 5. Verify Docker Hub

### Check Docker Hub Website

- [ ] Login to https://hub.docker.com
- [ ] Go to: Repositories
- [ ] Find repository: `heart-disease-model`
- [ ] Check tags:
  - [ ] `latest`
  - [ ] Model-specific (e.g., `random-forest`)
  - [ ] Date-versioned (e.g., `random-forest-20241216`)

### Pull Image Locally

```bash
# Pull image
docker pull your-username/heart-disease-model:latest

# Verify image
docker images | grep heart-disease-model

# Check image size (expected: 1-2 GB)
docker images your-username/heart-disease-model --format "{{.Repository}}:{{.Tag}} - {{.Size}}"
```

- [ ] Image pulled successfully
- [ ] Image size reasonable (1-2 GB)
- [ ] Tags visible

---

## 🧪 6. Test Docker Container

### Run Container

```bash
# Run container
docker run -d -p 8080:8080 --name test-api \
  your-username/heart-disease-model:latest

# Wait ~30 seconds for startup
sleep 30
```

- [ ] Container started successfully
- [ ] No errors in logs: `docker logs test-api`

### Test API

```bash
# Health check
curl http://localhost:8080/health

# Test prediction
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{
    "columns": ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"],
    "data": [[63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1]]
  }'
```

- [ ] Health endpoint responds
- [ ] Prediction endpoint works
- [ ] Returns valid JSON response

### Cleanup

```bash
# Stop and remove container
docker stop test-api
docker rm test-api
```

- [ ] Container stopped and removed

---

## 📊 7. View Results

### GitHub Actions Summary

- [ ] Click on workflow run
- [ ] Scroll to summary section
- [ ] Check:
  - [ ] ✅ "ML Training Pipeline Results"
  - [ ] ✅ "Docker Image Published"
  - [ ] Model comparison table
  - [ ] Docker pull commands

### Model Comparison

- [ ] Download `final_model_comparison.csv`
- [ ] Open in Excel/spreadsheet
- [ ] Verify columns:
  - [ ] model
  - [ ] test_accuracy
  - [ ] test_precision
  - [ ] test_recall
  - [ ] test_f1_score
- [ ] Check best model highlighted

---

## 🔄 8. Continuous Integration Test

### Test Auto-trigger on Push

```bash
# Make a small change
cd MLProject
echo "# Test commit" >> modelling.py

# Commit and push
git add .
git commit -m "test: verify auto-trigger"
git push origin main
```

- [ ] Workflow triggered automatically
- [ ] All jobs completed successfully
- [ ] New Docker image pushed
- [ ] New tag created (with new date)

### Test on Pull Request

```bash
# Create feature branch
git checkout -b feature/test-pr

# Make change
echo "# PR test" >> modelling.py

# Push and create PR
git add .
git commit -m "test: PR trigger"
git push origin feature/test-pr
```

- [ ] Create PR on GitHub
- [ ] Workflow triggered on PR
- [ ] Checks pass on PR

---

## 📚 9. Documentation Review

- [ ] Read [README.md](README.md) - Main documentation
- [ ] Read [TRIGGER_GUIDE.md](TRIGGER_GUIDE.md) - Trigger methods
- [ ] Read [ARTIFACTS_GUIDE.md](ARTIFACTS_GUIDE.md) - Artifacts access
- [ ] Read [DOCKER_SETUP.md](DOCKER_SETUP.md) - Docker Hub setup

---

## ✅ Final Checklist

### Required for Basic CI/CD
- [ ] Repository setup complete
- [ ] Workflow file exists and valid
- [ ] Dataset uploaded
- [ ] Workflow runs successfully
- [ ] Artifacts generated and accessible

### Required for Docker Deployment
- [ ] Docker Hub account created
- [ ] GitHub secrets configured (`DOCKER_USERNAME`, `DOCKER_PASSWORD`)
- [ ] Docker job runs successfully
- [ ] Docker image pushed to Docker Hub
- [ ] Image tested and working

### Optional Enhancements
- [ ] MLflow tracking to DagsHub/server
- [ ] Branch protection rules
- [ ] Code review requirements
- [ ] Slack/Discord notifications
- [ ] Automated deployments

---

## 🎯 Success Criteria

✅ **Workflow berjalan otomatis** saat push ke main/develop  
✅ **6 models trained** secara paralel dalam ~5-8 menit  
✅ **Best model identified** berdasarkan accuracy  
✅ **Docker image built** menggunakan mlflow build-docker  
✅ **Image pushed** ke Docker Hub dengan 3 tags  
✅ **Container runs** dan API responds correctly  
✅ **Artifacts stored** both temporarily dan permanently  

---

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Workflow not triggered | Check path filter di workflow.yml |
| Dataset not found | Ensure dataset in MLProject/ folder |
| Docker login failed | Verify DOCKER_USERNAME & DOCKER_PASSWORD secrets |
| Docker build failed | Check MLflow version and model artifacts |
| Image push failed | Check Docker Hub storage quota |
| Container won't start | Check logs: `docker logs <container-name>` |

---

## 📞 Support

Jika ada masalah:
1. Check logs di GitHub Actions
2. Review error messages
3. Consult documentation files
4. Check Docker Hub repository settings
5. Verify all secrets are set correctly

---

## 🎓 Learning Resources

- **GitHub Actions:** https://docs.github.com/actions
- **MLflow:** https://mlflow.org/docs/latest/
- **Docker:** https://docs.docker.com/
- **MLflow Docker:** https://mlflow.org/docs/latest/models.html#deploy-mlflow-models

---

**Status:** Ready for Production ✅  
**Last Updated:** December 16, 2025  
**Author:** Raifal Bagus Afdiansah
