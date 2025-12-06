# Vision Studio API Documentation

**Version:** 1.0.0  
**Base URL:** `http://localhost:8000`  
**API Prefix:** `/api/v1`

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Authentication](#authentication)
4. [Endpoints](#endpoints)
5. [Request Examples](#request-examples)
6. [Response Format](#response-format)
7. [Error Handling](#error-handling)
8. [Rate Limits](#rate-limits)
9. [Best Practices](#best-practices)

---

## Overview

Vision Studio is an AI-powered document data extraction API that uses Google Gemini vision models to extract structured data from PDFs and images.

### Supported File Types
- PDF (`.pdf`)
- PNG (`.png`)
- JPEG (`.jpg`, `.jpeg`)

### Key Features
- 📄 Multi-format support (PDF, images)
- 🤖 Powered by Google Gemini AI
- 🎯 Two extraction modes: Reference-based and Instruction-based
- 📚 Multi-page PDF processing
- ⚡ Fast processing (~3-5 seconds per document)
- 🆓 Free tier (1,500 requests/day)

---

## Quick Start

### 1. Start the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 2. Make Your First Request

```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@invoice.pdf" \
  -F 'reference_values={"invoice_number": "Invoice", "total": "Total"}'
```

### 3. View Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Authentication

Currently, the API does not require authentication for local development.

**For Production:**
- Configure API keys in `.env` file
- Implement authentication middleware as needed
- Consider rate limiting per API key

---

## Endpoints

### 1. Extract Data from Document

Extract structured data from uploaded files using AI vision.

**Endpoint:** `POST /api/v1/extract`

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File | ✅ Yes | PDF or image file (max 100MB) |
| `reference_values` | JSON String | ⚠️ One required* | Key-value pairs for extraction |
| `instructions` | String | ⚠️ One required* | Free-text extraction instructions |
| `ai_model` | String | ❌ No | AI model (default: `gemini`) |

*Either `reference_values` OR `instructions` must be provided.

#### Response

```json
{
  "status": "success",
  "extracted_data": {
    "invoice_number": "INV-2024-001",
    "total": "$9,765"
  },
  "confidence_scores": null,
  "processing_time": 3.58,
  "model_used": "gemini",
  "pages_processed": 1,
  "error_message": null
}
```

---

### 2. Get Available Models

Get list of supported AI models.

**Endpoint:** `GET /api/v1/models`

#### Response

```json
[
  {
    "name": "gemini",
    "provider": "Google",
    "description": "Google Gemini 2.5 Flash - Fast and efficient vision model",
    "supports_vision": true
  }
]
```

---

### 3. Health Check

Check API health status.

**Endpoint:** `GET /api/v1/health`

#### Response

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "models_available": {
    "gemini": true,
    "claude": false
  }
}
```

---

## Request Examples

### Reference-Based Extraction

Extract specific fields using key-value pairs.

#### cURL

```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@invoice.pdf" \
  -F 'reference_values={"invoice_number": "Invoice #", "date": "Date", "total": "Total Amount"}'
```

#### Python

```python
import requests

url = "http://localhost:8000/api/v1/extract"

with open("invoice.pdf", "rb") as f:
    response = requests.post(
        url,
        files={"file": f},
        data={
            "reference_values": '{"invoice_number": "Invoice #", "total": "Total"}'
        }
    )

result = response.json()
print(result["extracted_data"])
```

#### JavaScript (Node.js)

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('file', fs.createReadStream('invoice.pdf'));
form.append('reference_values', JSON.stringify({
  invoice_number: "Invoice #",
  total: "Total"
}));

axios.post('http://localhost:8000/api/v1/extract', form, {
  headers: form.getHeaders()
})
.then(response => console.log(response.data))
.catch(error => console.error(error));
```

---

### Instruction-Based Extraction

Extract data using natural language instructions.

#### cURL

```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@receipt.jpg" \
  -F "instructions=Extract all purchased items with their prices and the total amount"
```

#### Python

```python
import requests

url = "http://localhost:8000/api/v1/extract"

with open("receipt.jpg", "rb") as f:
    response = requests.post(
        url,
        files={"file": f},
        data={
            "instructions": "Extract all items, prices, and total amount"
        }
    )

result = response.json()
print(result["extracted_data"])
```

---

### Common Use Cases

#### 1. Invoice Processing

```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@invoice.pdf" \
  -F 'reference_values={
    "invoice_number": "Invoice Number",
    "date": "Date",
    "due_date": "Due Date",
    "bill_to": "Bill To",
    "subtotal": "Subtotal",
    "tax": "Tax",
    "total": "Total"
  }'
```

#### 2. Receipt Scanning

```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@receipt.jpg" \
  -F "instructions=Extract the store name, all purchased items with prices, subtotal, tax, and total amount"
```

#### 3. Business Card Extraction

```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@business_card.png" \
  -F 'reference_values={
    "name": "Name",
    "title": "Title",
    "company": "Company",
    "email": "Email",
    "phone": "Phone",
    "address": "Address"
  }'
```

#### 4. Form Data Extraction

```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@form.pdf" \
  -F "instructions=Extract all filled form fields including name, email, phone, address, and any checkbox selections"
```

---

## Response Format

### Success Response

```json
{
  "status": "success",
  "extracted_data": {
    "field1": "value1",
    "field2": "value2"
  },
  "confidence_scores": null,
  "processing_time": 3.58,
  "model_used": "gemini",
  "pages_processed": 1,
  "error_message": null
}
```

### Error Response

```json
{
  "status": "error",
  "extracted_data": {},
  "confidence_scores": null,
  "processing_time": 0.25,
  "model_used": "gemini",
  "pages_processed": 0,
  "error_message": "File too large. Maximum size is 100MB"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | `"success"` or `"error"` |
| `extracted_data` | Object | Extracted key-value pairs |
| `confidence_scores` | Object | Confidence scores (0.0-1.0) for each field |
| `processing_time` | Float | Processing time in seconds |
| `model_used` | String | AI model used (`"gemini"`) |
| `pages_processed` | Integer | Number of pages/images processed |
| `error_message` | String | Error description (null if success) |

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| `200` | OK | Request successful |
| `400` | Bad Request | Invalid parameters or file format |
| `413` | Payload Too Large | File exceeds 100MB limit |
| `422` | Unprocessable Entity | Invalid JSON in reference_values |
| `500` | Internal Server Error | Server-side error |

### Common Errors

#### 1. File Too Large

```json
{
  "detail": "File size exceeds maximum allowed size of 100MB"
}
```

**Solution:** Reduce file size or split into multiple files.

#### 2. Invalid File Format

```json
{
  "detail": "Invalid file extension. Allowed: pdf, png, jpg, jpeg"
}
```

**Solution:** Convert file to supported format.

#### 3. Missing Extraction Parameters

```json
{
  "detail": "Either 'reference_values' or 'instructions' must be provided"
}
```

**Solution:** Provide either `reference_values` or `instructions`.

#### 4. Invalid JSON

```json
{
  "detail": "Invalid JSON in reference_values: Expecting property name enclosed in double quotes"
}
```

**Solution:** Ensure `reference_values` is valid JSON string.

#### 5. API Key Not Configured

```json
{
  "status": "error",
  "error_message": "API key not valid. Please pass a valid API key."
}
```

**Solution:** Add valid Gemini API key to `.env` file.

---

## Rate Limits

### Free Tier (Gemini)

- **Requests per minute:** 15
- **Requests per day:** 1,500
- **Max file size:** 100MB
- **Max PDF pages:** 50

### Handling Rate Limits

If you exceed rate limits, you'll receive:

```json
{
  "status": "error",
  "error_message": "429 Resource has been exhausted"
}
```

**Solutions:**
- Implement exponential backoff
- Add delays between requests
- Upgrade to paid tier for higher limits

---

## Best Practices

### 1. File Optimization

- **Compress images** before upload (use PNG or JPEG compression)
- **Reduce PDF size** using PDF compression tools
- **Limit pages** to only necessary pages
- **Use appropriate resolution** (300 DPI is usually sufficient)

### 2. Extraction Accuracy

#### Reference-Based Extraction
✅ **Good:** Use exact text from document
```json
{"invoice_number": "Invoice Number", "total": "Total Amount"}
```

❌ **Bad:** Use generic terms
```json
{"invoice_number": "number", "total": "amount"}
```

#### Instruction-Based Extraction
✅ **Good:** Be specific and clear
```
"Extract the invoice number, date, and total amount from this invoice"
```

❌ **Bad:** Be vague
```
"Get the data"
```

### 3. Error Handling

Always check the `status` field:

```python
response = requests.post(url, files=files, data=data)
result = response.json()

if result["status"] == "success":
    data = result["extracted_data"]
    # Process data
else:
    error = result["error_message"]
    # Handle error
```

### 4. Performance Optimization

- **Batch processing:** Process multiple files sequentially
- **Async requests:** Use async/await for concurrent processing
- **Caching:** Cache results for identical documents
- **Retry logic:** Implement retry with exponential backoff

### 5. Security

- **Validate files** before upload (check size, type, content)
- **Sanitize extracted data** before using in your application
- **Use HTTPS** in production
- **Implement authentication** for production deployments
- **Rate limit** per user/API key

---

## Configuration

### Environment Variables

Create a `.env` file:

```env
# API Keys
GEMINI_API_KEY=your_gemini_api_key_here

# File Limits
MAX_FILE_SIZE=104857600  # 100MB in bytes
MAX_PDF_PAGES=50

# AI Model
GEMINI_MODEL=gemini-1.5-flash

# Application
TEMP_DIR=/tmp/vision-studio
ALLOWED_EXTENSIONS=pdf,png,jpg,jpeg
```

### Get API Key

1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Create API key
4. Copy key to `.env` file

---

## Testing

### Sample Files

Test files are available in `tests/sample_files/`:

- `invoice_sample_001.png` - Business invoice
- `receipt_sample_001.png` - Retail receipt
- `business_card_001.png` - Business card
- `form_sample_001.png` - Registration form

### Run Automated Tests

```bash
cd tests/sample_files
./run_tests.py
```

### Manual Testing

```bash
# Test with sample invoice
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@tests/sample_files/invoice_sample_001.png" \
  -F 'reference_values={"invoice_number": "Invoice", "total": "Total"}'
```

---

## Troubleshooting

### Server Won't Start

```bash
# Check if port 8000 is in use
lsof -i :8000

# Use different port
uvicorn app.main:app --reload --port 8001
```

### API Key Errors

```bash
# Verify API key in .env
cat .env | grep GEMINI_API_KEY

# Test API key directly
python test_gemini_key.py
```

### File Upload Errors

```bash
# Check file size
ls -lh your_file.pdf

# Check file format
file your_file.pdf
```

---

## Support & Resources

- **Interactive Docs:** http://localhost:8000/docs
- **API Reference:** http://localhost:8000/redoc
- **Gemini API Docs:** https://ai.google.dev/tutorials/get_started
- **GitHub Issues:** Report bugs and request features

---

## Changelog

### Version 1.0.0 (2024-12-06)

- ✅ Initial release
- ✅ Gemini AI integration
- ✅ Reference-based extraction
- ✅ Instruction-based extraction
- ✅ Multi-page PDF support
- ✅ Simplified API (Gemini as default)

---

## License

MIT License

---

**Built with ❤️ using FastAPI and Google Gemini**
