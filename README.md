A FastAPI application for using vaiours LLMs .


## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with necessary credentials and configurations.

3. Run the application:
```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload
```

## API Documentation

Once the application is running, you can access:
- API documentation: http://localhost:8000/docs
- Alternative documentation: http://localhost:8000/redoc
