# 📦 Panduan Akses Artifacts

## 🎯 Lokasi Penyimpanan Artifacts

Workflow CI/CD menyimpan artifacts di **2 lokasi**:

### 1. GitHub Actions Artifacts (Temporary - 30 hari)
**Cara Akses:**
1. Buka: https://github.com/afdiansah/Workflow-CI/actions
2. Pilih workflow run yang sudah selesai
3. Scroll ke **"Artifacts"** section
4. Download: `model-*`, `final-comparison`

### 2. Branch `artifacts` (Permanent) ✨
**Cara Akses:**

#### Via Web Browser:
```
https://github.com/afdiansah/Workflow-CI/tree/artifacts
```

#### Via Git Clone:
```bash
# Clone artifacts branch
git clone -b artifacts https://github.com/afdiansah/Workflow-CI.git artifacts

# Atau dari existing repo
git fetch origin artifacts
git checkout artifacts
```

---

## 📊 Struktur Artifacts

```
artifacts branch/
├── README.md                      # Metadata (timestamp, commit, triggered by)
├── final_model_comparison.csv     # Hasil comparison semua model
├── model-Logistic_Regression/
│   ├── mlruns/                   # MLflow tracking data
│   └── model_comparison_results.csv
├── model-Random_Forest/
├── model-Gradient_Boosting/
├── model-Decision_Tree/
├── model-K_Nearest_Neighbors/
└── model-Support_Vector_Machine/
```

---

## 📥 Download Artifacts

### Download Specific File:
```bash
# Download final comparison
curl -O https://raw.githubusercontent.com/afdiansah/Workflow-CI/artifacts/final_model_comparison.csv
```

### Download All Artifacts:
```bash
git clone -b artifacts https://github.com/afdiansah/Workflow-CI.git workflow-artifacts
cd workflow-artifacts
```

### View MLflow UI:
```bash
cd workflow-artifacts/model-Random_Forest
mlflow ui --backend-store-uri file:///$(pwd)/mlruns
# Open: http://localhost:5000
```

---

## 🔄 Auto-Update

Setiap workflow selesai, artifacts **otomatis di-commit** ke branch `artifacts`:

**Commit Message:**
```
🤖 Auto-commit: Training artifacts from run <run_id>
```

**Metadata di README.md:**
- Timestamp
- Commit SHA
- Branch name
- Workflow run ID
- Triggered by

---

## 📈 View Latest Results

```bash
# Fetch latest
git checkout artifacts
git pull origin artifacts

# View results
cat final_model_comparison.csv
```

---

**Artifacts tersimpan permanen dan dapat diakses kapan saja!** 🚀
