# Sample Test Files for Vision Studio API

This directory contains sample files for testing the Vision Studio API's data extraction capabilities.

## Available Sample Files

### Invoices
1. **invoice_sample_001.png** - Business invoice from ACME Corporation
   - Invoice #: INV-2024-001
   - Contains: Line items, subtotal, tax, total
   - Good for testing: Reference-based extraction of invoice fields

2. **invoice_sample_002.png** - Freelance invoice from Creative Designs Studio
   - Invoice #: FRL-2024-156
   - Contains: Services, discount, bank details
   - Good for testing: Discount calculations, payment information extraction

3. **invoice_medical_001.png** - Medical invoice from City Medical Center
   - Patient ID: PMC-789456
   - Contains: Medical services, insurance coverage, patient responsibility
   - Good for testing: Healthcare document extraction

### Receipts
1. **receipt_sample_001.png** - Retail store receipt from Super Mart
   - Receipt #: RCP-45678
   - Contains: Itemized grocery list with prices
   - Good for testing: Line item extraction, total calculation

2. **receipt_restaurant_001.png** - Restaurant receipt from Bella Italia
   - Contains: Food items, tax, tip, total
   - Good for testing: Restaurant bill parsing, tip calculation

3. **receipt_gas_station.png** - Gas station receipt from Quick Fuel
   - Receipt #: GS-789012
   - Contains: Fuel purchase, additional items
   - Good for testing: Fuel transaction extraction

### Business Cards
1. **business_card_001.png** - Tech professional business card
   - Name: John Anderson
   - Company: TechVision Labs
   - Good for testing: Contact information extraction

2. **business_card_002.png** - Creative professional business card
   - Name: Maria Santos
   - Company: Pixel Perfect Agency
   - Good for testing: Designer contact extraction

### Forms
1. **form_sample_001.png** - Customer registration form
   - Name: Emily Rodriguez
   - Contains: Personal information, checkboxes, signature
   - Good for testing: Form field extraction, checkbox detection

### Bills
1. **bill_utility_001.png** - Utility bill from Metro Power & Light
   - Account #: 9876543210
   - Contains: Usage data, charges breakdown
   - Good for testing: Utility bill parsing, usage metrics

## Testing Examples

### Example 1: Extract Invoice Data (Reference-based)
```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@tests/sample_files/invoice_sample_001.png" \
  -F "ai_model=gemini" \
  -F 'reference_values={"invoice_number": "Invoice", "date": "Date", "total": "Total"}'
```

### Example 2: Extract Receipt Items (Instruction-based)
```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@tests/sample_files/receipt_sample_001.png" \
  -F "ai_model=claude" \
  -F "instructions=Extract all purchased items with their individual prices and the total amount"
```

### Example 3: Extract Business Card Info
```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@tests/sample_files/business_card_001.png" \
  -F "ai_model=gemini" \
  -F 'reference_values={"name": "Name", "email": "Email", "phone": "Phone", "company": "Company"}'
```

### Example 4: Extract Form Data
```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@tests/sample_files/form_sample_001.png" \
  -F "ai_model=claude" \
  -F "instructions=Extract all filled form fields including name, email, phone, address, and checkbox selections"
```

## Python Testing Script

```python
import requests
import json

def test_extraction(file_path, ai_model, reference_values=None, instructions=None):
    url = "http://localhost:8000/api/v1/extract"
    
    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {"ai_model": ai_model}
        
        if reference_values:
            data["reference_values"] = json.dumps(reference_values)
        if instructions:
            data["instructions"] = instructions
        
        response = requests.post(url, files=files, data=data)
        return response.json()

# Test invoice extraction
result = test_extraction(
    "tests/sample_files/invoice_sample_001.png",
    "gemini",
    reference_values={
        "invoice_number": "Invoice",
        "date": "Date",
        "total": "Total"
    }
)
print(json.dumps(result, indent=2))
```

## File Formats
- All current samples are PNG images
- The API also supports PDF and JPEG formats
- Maximum file size: 100MB (configurable)

## Adding More Samples
To add your own test files:
1. Place files in this directory
2. Update this README with file descriptions
3. Include expected extraction fields for testing
