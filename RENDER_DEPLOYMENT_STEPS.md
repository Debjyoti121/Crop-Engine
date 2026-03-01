# 🚀 Render Deployment Settings
# add build and docker cmd to run automatically
## Use these EXACT settings when deploying on Render:

**Basic Settings:**
- Name: crop-recommender-api
- Environment: Python 3
- Region: Choose closest to your users

**Build & Deploy:**
- Build Command: `pip install -r src/requirements.txt`
- Start Command: `cd src && gunicorn --bind 0.0.0.0:$PORT app_production:app`

**Advanced Settings:**
- Auto-Deploy: Yes (optional)
- Plan: Free (for testing)

## Important Notes:

1. Make sure ALL model files are uploaded to GitHub:
   - lgbm_best_model_22class.joblib
   - crop_label_encoder.pkl  
   - column_scalers.pkl

2. If deployment fails, check the logs in Render dashboard

3. Your API will be available at:
   https://crop-recommender-api-XXXX.onrender.com

## After Deployment:

1. Test the health endpoint:
   GET https://your-url.onrender.com/health

2. Test the prediction endpoint:
   POST https://your-url.onrender.com/predict

3. Update your mobile app with the URL