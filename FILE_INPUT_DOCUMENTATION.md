# API File Input Documentation

## File Upload Specification

### Input Parameter

**Parameter Name:** `file`  
**Type:** File Object (Binary Upload)  
**Required:** Yes  
**Description:** PDF or image file to extract data from

### Supported File Formats

| Format | Extension | MIME Type | Max Size |
|--------|-----------|-----------|----------|
| PDF | `.pdf` | `application/pdf` | 100MB |
| PNG | `.png` | `image/png` | 100MB |
| JPEG | `.jpg`, `.jpeg` | `image/jpeg` | 100MB |

### File Upload Methods

## 1. cURL (Command Line)

### Basic Upload
```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@/path/to/document.pdf" \
  -F 'reference_values={"total": "Total"}'
```

### With Full Path
```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@/Users/username/Documents/invoice.pdf" \
  -F "instructions=Extract invoice number and total"
```

**Note:** The `@` symbol tells cURL to upload the file as binary data.

---

## 2. Python (requests)

### Method 1: Using `open()` with context manager (Recommended)
```python
import requests

url = "http://localhost:8000/api/v1/extract"

# File is automatically closed after the request
with open("invoice.pdf", "rb") as f:
    response = requests.post(
        url,
        files={"file": f},  # File object
        data={
            "reference_values": '{"total": "Total"}'
        }
    )

result = response.json()
print(result)
```

### Method 2: Using file path directly
```python
import requests

url = "http://localhost:8000/api/v1/extract"

# requests handles file opening/closing
with open("document.pdf", "rb") as file_obj:
    files = {"file": file_obj}
    data = {"instructions": "Extract all fields"}
    
    response = requests.post(url, files=files, data=data)

print(response.json())
```

### Method 3: Multiple files (sequential)
```python
import requests
import os

url = "http://localhost:8000/api/v1/extract"
files_to_process = ["invoice1.pdf", "invoice2.pdf", "receipt.jpg"]

for filename in files_to_process:
    with open(filename, "rb") as f:
        response = requests.post(
            url,
            files={"file": f},
            data={"reference_values": '{"total": "Total"}'}
        )
        print(f"{filename}: {response.json()['status']}")
```

---

## 3. JavaScript (Node.js)

### Using FormData
```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();

// Add file as stream
form.append('file', fs.createReadStream('invoice.pdf'));
form.append('reference_values', JSON.stringify({
  invoice_number: "Invoice Number",
  total: "Total"
}));

axios.post('http://localhost:8000/api/v1/extract', form, {
  headers: form.getHeaders()
})
.then(response => {
  console.log(response.data);
})
.catch(error => {
  console.error(error);
});
```

### Using fetch (Browser)
```javascript
const fileInput = document.querySelector('input[type="file"]');
const file = fileInput.files[0];

const formData = new FormData();
formData.append('file', file);  // File object from input
formData.append('instructions', 'Extract invoice number and total');

fetch('http://localhost:8000/api/v1/extract', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error(error));
```

---

## 4. Postman

### Steps:
1. Set method to **POST**
2. URL: `http://localhost:8000/api/v1/extract`
3. Go to **Body** tab
4. Select **form-data**
5. Add key `file` with type **File**
6. Click **Select Files** and choose your PDF/image
7. Add other parameters:
   - Key: `reference_values`, Value: `{"total": "Total"}`
   - Key: `instructions`, Value: `Extract all fields`
8. Click **Send**

---

## 5. Python (httpx - async)

```python
import httpx
import asyncio

async def extract_data(file_path):
    url = "http://localhost:8000/api/v1/extract"
    
    async with httpx.AsyncClient() as client:
        with open(file_path, "rb") as f:
            files = {"file": f}
            data = {"reference_values": '{"total": "Total"}'}
            
            response = await client.post(url, files=files, data=data)
            return response.json()

# Run async
result = asyncio.run(extract_data("invoice.pdf"))
print(result)
```

---

## File Object Details

### What is a File Object?

A file object is a binary stream that represents the file contents. In the API:

- **Input:** Binary file data (not file path string)
- **Format:** Multipart form-data
- **Encoding:** Binary (not base64 or text)
- **Streaming:** Supports large files up to 100MB

### Important Notes

✅ **DO:**
- Use binary mode (`"rb"`) when opening files
- Use multipart/form-data encoding
- Close files after upload (use context managers)
- Check file size before upload

❌ **DON'T:**
- Send file path as string
- Use text mode (`"r"`)
- Send base64 encoded files
- Forget to close file handles

---

## File Size Limits

### Current Limits
- **Maximum file size:** 100MB (104,857,600 bytes)
- **Maximum PDF pages:** 50 pages
- **Timeout:** 60 seconds per request

### Check File Size
```python
import os

file_path = "document.pdf"
file_size = os.path.getsize(file_path)
max_size = 100 * 1024 * 1024  # 100MB

if file_size > max_size:
    print(f"File too large: {file_size / (1024*1024):.2f}MB")
else:
    print(f"File size OK: {file_size / (1024*1024):.2f}MB")
```

---

## Error Handling

### File Too Large
```json
{
  "detail": "File size exceeds maximum allowed size of 100MB"
}
```

**Solution:** Compress or split the file

### Invalid File Type
```json
{
  "detail": "Invalid file extension. Allowed: pdf, png, jpg, jpeg"
}
```

**Solution:** Convert to supported format

### File Not Found (Client-side)
```python
try:
    with open("nonexistent.pdf", "rb") as f:
        response = requests.post(url, files={"file": f})
except FileNotFoundError:
    print("File not found. Check the path.")
```

---

## Best Practices

### 1. Always Use Binary Mode
```python
# ✅ Correct
with open("file.pdf", "rb") as f:
    files = {"file": f}

# ❌ Wrong
with open("file.pdf", "r") as f:  # Text mode
    files = {"file": f}
```

### 2. Use Context Managers
```python
# ✅ Correct - File automatically closed
with open("file.pdf", "rb") as f:
    response = requests.post(url, files={"file": f})

# ❌ Wrong - File handle may leak
f = open("file.pdf", "rb")
response = requests.post(url, files={"file": f})
# f.close() might not be called if error occurs
```

### 3. Validate Before Upload
```python
import os

def validate_file(file_path):
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Check file size
    size = os.path.getsize(file_path)
    if size > 100 * 1024 * 1024:
        raise ValueError(f"File too large: {size / (1024*1024):.2f}MB")
    
    # Check file extension
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ['.pdf', '.png', '.jpg', '.jpeg']:
        raise ValueError(f"Invalid file type: {ext}")
    
    return True

# Use it
try:
    validate_file("invoice.pdf")
    with open("invoice.pdf", "rb") as f:
        response = requests.post(url, files={"file": f})
except (FileNotFoundError, ValueError) as e:
    print(f"Validation error: {e}")
```

### 4. Handle Upload Errors
```python
import requests

def upload_file(file_path):
    url = "http://localhost:8000/api/v1/extract"
    
    try:
        with open(file_path, "rb") as f:
            response = requests.post(
                url,
                files={"file": f},
                data={"instructions": "Extract all fields"},
                timeout=60  # 60 second timeout
            )
            response.raise_for_status()  # Raise error for bad status
            return response.json()
    
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.ConnectionError:
        print("Could not connect to API")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    
    return None
```

---

## Summary

### File Input Requirements

| Aspect | Requirement |
|--------|-------------|
| **Parameter Name** | `file` |
| **Type** | File Object (Binary) |
| **Encoding** | Multipart/form-data |
| **Mode** | Binary (`"rb"`) |
| **Max Size** | 100MB |
| **Formats** | PDF, PNG, JPG, JPEG |

### Quick Reference

```python
# ✅ Correct way to upload
import requests

with open("document.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/v1/extract",
        files={"file": f},
        data={"reference_values": '{"total": "Total"}'}
    )

print(response.json())
```

**The API accepts file objects (binary uploads) via multipart/form-data encoding!** 📄✅
