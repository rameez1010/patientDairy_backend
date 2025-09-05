# Bio Krystal API

A FastAPI-based backend for managing blood biomarkers, patient data, and integrations such as Fullscript.

## Environment Configuration

This project uses environment variables for configuration, loaded from `.env` files. There are separate files for each environment:

- `.env.development` → for local development
- `.env.staging` → for staging/testing
- `.env.production` → for production

You **do not need to manually copy** these files. The project will automatically load the correct file based on the `ENV` environment variable.

### Example `.env.development`

```env
GOOGLE_API_KEY=Google Cloud API Key
GCP_PROJECT_ID=Google Cloud Project ID
GCP_LOCATION=Google Cloud Region (e.g., us-central1)
JWT_KEY=JWT signing secret key
ALGORITHM=JWT algorithm (e.g., HS256)
ACCESS_KEY_EXPIRE_DAYS=Number of days before access token expires
CLOUD_STORAGE_BUCKET_NAME=Google Cloud Storage bucket name
SENDGRID_API_KEY=SendGrid API Key for sending emails
ENVIRONMENT=App environment (development/staging/production)
FULLSCRIPT_CLIENT_ID=Fullscript OAuth Client ID
FULLSCRIPT_CLIENT_SECRET=Fullscript OAuth Client Secret
FULLSCRIPT_REDIRECT_URI=Fullscript OAuth Redirect URI
FULLSCRIPT_API_URL=Fullscript API base URL
FRONTEND_PATIENT_SET_PASSWORD_URL=Frontend URL for patient to set password

# ...other variables
```

---

## Running the Project

### Development

```sh
python uvicorn_config.py
```

- Loads `.env.development` by default.

### Staging

```sh
ENV=staging python uvicorn_config.py
```

- Loads `.env.staging` automatically.

### Production

```sh
ENV=production python uvicorn_config.py
```

- Loads `.env.production` automatically.

---

## Managing Environment Variables

- All environment variables are defined in the respective `.env.*` files.
- To add new variables, add them to each `.env.*` file as needed.
- The `ENVIRONMENT` variable inside each `.env.*` file should match the environment (e.g., `ENVIRONMENT=staging` in `.env.staging`).
