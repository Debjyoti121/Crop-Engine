# Crop Recommender Engine - Deployment Guide

## Quick Start

### Local Development
```bash
cd src
pip install -r requirements.txt
python app.py
```

### Docker Deployment (Recommended)

#### Option 1: Simple Docker Run
```bash
# Build the image
docker build -t crop-recommender .

# Run the container
docker run -p 5000:5000 crop-recommender
```

#### Option 2: Docker Compose (With Health Checks)
```bash
# Start the service
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

#### Option 3: With Nginx Reverse Proxy
```bash
# Start with nginx
docker-compose --profile with-nginx up -d
```

## API Endpoints

### Health Check
```
GET /health
```
Response:
```json
{
  "status": "healthy",
  "message": "Crop Recommender API is running",
  "model_loaded": true,
  "encoder_loaded": true,
  "number_of_crops": 22
}
```

### Crop Prediction
```
POST /predict
Content-Type: application/json
```

Request Body:
```json
{
  "N": 276.50,        // Nitrogen content
  "P": 35,            // Phosphorus content
  "K": 40,            // Potassium content
  "pH": 6.70,         // Soil pH (0-14)
  "temperature": 37,   // Temperature in °C
  "humidity": 67.50,   // Humidity percentage (0-100)
  "moisture": 79,      // Soil moisture (0-100)
  "rainfall": 150      // Rainfall in mm
}
```

Response:
```json
{
  "best_crop": "rice",
  "probability": 0.8542,
  "input_received": { ... }
}
```

### API Information
```
GET /
```

## Testing the API

### Using curl
```bash
# Health check
curl http://localhost:5000/health

# Prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "N": 276.50,
    "P": 35,
    "K": 40,
    "pH": 6.70,
    "temperature": 37,
    "humidity": 67.50,
    "moisture": 79,
    "rainfall": 150
  }'
```

### Using the provided test script
```bash
cd src
python test.py
```

## Production Deployment

### Environment Variables
- `FLASK_ENV=production`
- `WORKERS=2` (for gunicorn)

### Required Files
Ensure these files are present in the src/ directory:
- `lgbm_best_model_22class.joblib` (ML model)
- `crop_label_encoder.pkl` (label encoder)
- `column_scalers.pkl` (feature scalers)

### Cloud Deployment Options

#### 1. Heroku
```bash
# Install Heroku CLI, then:
heroku create your-crop-recommender
git push heroku main
```

#### 2. AWS ECS/Fargate
- Push Docker image to ECR
- Create ECS service with the image
- Configure load balancer

#### 3. Google Cloud Run
```bash
gcloud run deploy crop-recommender \
  --image gcr.io/PROJECT-ID/crop-recommender \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### 4. Azure Container Instances
```bash
az container create \
  --resource-group myResourceGroup \
  --name crop-recommender \
  --image crop-recommender:latest \
  --ports 5000
```

## Security Considerations

1. **Rate Limiting**: Nginx config includes basic rate limiting
2. **Input Validation**: All inputs are validated before processing
3. **Error Handling**: Sensitive information is not exposed in error messages
4. **CORS**: Configured for cross-origin requests

## Monitoring

### Health Checks
The `/health` endpoint provides service status and can be used with:
- Docker health checks
- Kubernetes liveness/readiness probes
- Load balancer health checks

### Logging
- Application logs are written to stdout
- Use `docker-compose logs` to view logs
- Consider log aggregation for production (ELK stack, Splunk, etc.)

## Troubleshooting

### Common Issues

1. **Model files not found**
   - Ensure all `.pkl` and `.joblib` files are in the src/ directory
   - Check file permissions

2. **Import errors**
   - Verify all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Port conflicts**
   - Change port in docker-compose.yml if 5000 is in use
   - Use `docker-compose port crop-recommender 5000` to check assigned port

4. **Memory issues**
   - Increase Docker memory limits
   - Reduce gunicorn workers if needed

### Performance Tips

1. **Model Loading**: Models are cached after first load
2. **Concurrent Requests**: Gunicorn handles multiple workers
3. **Resource Limits**: Set appropriate Docker memory/CPU limits
4. **Caching**: Consider Redis for caching predictions if needed