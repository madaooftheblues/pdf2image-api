# PDF2Image API

A lightweight API endpoint for converting PDF files to images using Python's pdf2image library with FastAPI. Supports high DPI conversion and automatic ZIP packaging for multi-page PDFs.

## Features

- 🚀 **FastAPI-based** - Modern, fast web framework
- 📄 **PDF to Image Conversion** - Convert PDFs to PNG, JPEG, WEBP formats
- 🎯 **High DPI Support** - Configurable DPI up to 600
- 📦 **Auto ZIP** - Multi-page PDFs are automatically zipped
- 🔐 **API Key Authentication** - Secure your endpoint with API keys
- 🐳 **Docker Ready** - Easy deployment with Docker
- ☁️ **Serverless Support** - AWS Lambda compatible
- 🔒 **Input Validation** - File type, size, and parameter validation
- 📊 **Health Checks** - Built-in health monitoring

## Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your API key:**
   ```bash
   # Option 1: Environment variable
   export API_KEY="your-secret-api-key-here"
   
   # Option 2: Create .env file (copy from env.example)
   cp env.example .env
   # Edit .env with your API key
   ```

3. **Run the server:**
   ```bash
   python main.py
   ```

4. **Access the API:**
   - API: http://localhost:8473
   - Docs: http://localhost:8473/docs
   - Health: http://localhost:8473/health

### Docker Deployment

1. **Build the image:**
   ```bash
   docker build -t pdf2image-api .
   ```

2. **Run with Docker:**
   ```bash
   docker run -p 8473:8473 pdf2image-api
   ```

3. **Or use Docker Compose:**
   ```bash
   docker-compose up
   ```

## API Usage

### Convert PDF to Images

**Endpoint:** `POST /convert`

**Parameters:**
- `file` (required): PDF file to convert
- `format` (optional): Output format (PNG, JPEG, JPG, WEBP) - Default: PNG
- `dpi` (optional): DPI for conversion (72-600) - Default: 300
- `quality` (optional): JPEG quality (1-100) - Only for JPEG format

**Response:**
- Single page PDF → Returns image file directly
- Multi-page PDF → Returns ZIP file with all pages

**Example using curl:**
```bash
# Convert to PNG with default settings
curl -X POST "http://localhost:8473/convert" \
  -H "Authorization: Bearer your-secret-api-key-here" \
  -F "file=@document.pdf"

# Convert to JPEG with custom DPI and quality
curl -X POST "http://localhost:8473/convert" \
  -H "Authorization: Bearer your-secret-api-key-here" \
  -F "file=@document.pdf" \
  -F "format=JPEG" \
  -F "dpi=600" \
  -F "quality=95"
```

**Authentication:**
All requests to `/convert` require an API key in the Authorization header:
```
Authorization: Bearer your-secret-api-key-here
```

## Deployment Options

### 1. Coolify Deployment (Recommended)

1. **Push to Git repository**
2. **In Coolify:**
   - Create new project
   - Connect your Git repository
   - Select Docker deployment
   - **Set environment variables:**
     - `API_KEY` = Your secure API key (generate a strong random key)
   - Deploy!

### 2. AWS Lambda (Serverless)

1. **Install Serverless Framework:**
   ```bash
   npm install -g serverless
   npm install serverless-python-requirements
   ```

2. **Deploy:**
   ```bash
   serverless deploy
   ```

### 3. Traditional VPS/Cloud

1. **Install system dependencies:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install poppler-utils
   
   # CentOS/RHEL
   sudo yum install poppler-utils
   ```

2. **Deploy with Docker:**
   ```bash
   docker run -d -p 8473:8473 --name pdf2image-api pdf2image-api
   ```

## Configuration

### Environment Variables

- `API_KEY` - **Required** - Your secure API key for authentication
- `PYTHONUNBUFFERED=1` - Enable Python output buffering
- `MAX_FILE_SIZE` - Maximum file size (default: 50MB)

### Docker Configuration

The Dockerfile includes:
- Python 3.11 slim base image
- Poppler utilities for PDF processing
- Non-root user for security
- Health checks
- Optimized layer caching

## API Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8473/docs
- **ReDoc:** http://localhost:8473/redoc

## Limitations

- Maximum file size: 50MB
- DPI range: 72-600
- Supported formats: PNG, JPEG, JPG, WEBP
- Memory usage scales with PDF size and DPI

## Development

### Project Structure

```
pdf2image-api/
├── main.py                 # Main FastAPI application
├── serverless_main.py     # AWS Lambda version
├── requirements.txt       # Python dependencies
├── requirements-serverless.txt  # Serverless dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── serverless.yml        # Serverless Framework config
└── README.md             # This file
```

### Testing

```bash
# Test with a sample PDF
curl -X POST "http://localhost:8473/convert" \
  -H "Authorization: Bearer your-secret-api-key-here" \
  -F "file=@sample.pdf" \
  -F "format=PNG" \
  -F "dpi=300"
```

## License

MIT License - see LICENSE file for details.