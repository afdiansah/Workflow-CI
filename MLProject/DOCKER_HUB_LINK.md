# 🐳 Docker Hub Repository

## Heart Disease Classification Model

**Docker Hub Repository:** 
- Repository Name: `your-dockerhub-username/heart-disease-model`
- Link: https://hub.docker.com/r/your-dockerhub-username/heart-disease-model

---

## Available Tags

### Latest Version
```bash
docker pull your-dockerhub-username/heart-disease-model:latest
```

### Model-Specific Tags
- `logistic-regression` - Logistic Regression model
- `random-forest` - Random Forest model
- `gradient-boosting` - Gradient Boosting model
- `decision-tree` - Decision Tree model
- `k-nearest-neighbors` - KNN model
- `support-vector-machine` - SVM model

### Date-Based Tags
Format: `{model-name}-YYYYMMDD`

Example:
```bash
docker pull your-dockerhub-username/heart-disease-model:random-forest-20241217
```

---

## How to Use

### 1. Pull the Image
```bash
docker pull your-dockerhub-username/heart-disease-model:latest
```

### 2. Run the Container
```bash
docker run -p 8080:8080 your-dockerhub-username/heart-disease-model:latest
```

### 3. Make Predictions
```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{
    "dataframe_split": {
      "columns": ["feature1", "feature2", "..."],
      "data": [[value1, value2, ...]]
    }
  }'
```

---

## Docker Hub Setup Instructions

### For Repository Maintainers

1. **Create Docker Hub Account**
   - Sign up at https://hub.docker.com

2. **Create Access Token**
   - Go to: Account Settings → Security → Access Tokens
   - Create new token with Read, Write, Delete permissions

3. **Add GitHub Secrets**
   - Repository → Settings → Secrets and variables → Actions
   - Add `DOCKERHUB_USERNAME` (your Docker Hub username)
   - Add `DOCKER_PASSWORD` (your access token)

4. **Push Changes**
   - The CI/CD pipeline will automatically build and push images
   - Images are tagged with model name and date

---

## Image Details

**Base Image:** MLflow serving image (automatically generated)

**Exposed Port:** 8080

**Environment Variables:**
- `MLFLOW_TRACKING_URI` - MLflow tracking server URI (optional)

**Model Format:** MLflow model format with sklearn flavor

---

## Automated Builds

Images are automatically built and pushed by GitHub Actions when:
- Code is pushed to `main` or `develop` branches
- Pull requests are merged
- Workflow is manually triggered

The best performing model is automatically selected and containerized.

---

## Version History

Check the Docker Hub repository for complete version history and tags:
https://hub.docker.com/r/your-dockerhub-username/heart-disease-model/tags

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/your-username/your-repo/issues
- Email: your-email@example.com

---

**Last Updated:** December 2024
**Maintained by:** Your Name
