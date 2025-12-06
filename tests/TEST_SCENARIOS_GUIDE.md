# Test Scenarios Guide

## Overview

This file contains 30 comprehensive test scenarios for the Vision Studio API, covering all document types and extraction methods.

## File Location

**CSV File:** `tests/TEST_SCENARIOS.csv`

This CSV file can be opened in:
- Microsoft Excel
- Google Sheets
- LibreOffice Calc
- Any spreadsheet application

## CSV Columns

| Column | Description |
|--------|-------------|
| **Test ID** | Unique test identifier (1-30) |
| **Test Name** | Descriptive name of the test |
| **Document Type** | Type of document (Invoice, Receipt, Business Card, Form, Bill) |
| **File Name** | Sample file to use (in `tests/sample_files/`) |
| **Extraction Method** | Reference, Instructions, or Both |
| **Reference Values (JSON)** | JSON string for reference-based extraction |
| **Instructions** | Natural language instructions |
| **Expected Fields** | Fields expected to be extracted (pipe-separated) |
| **Notes** | Additional information about the test |
| **Priority** | Test priority (High, Medium, Low) |

## Test Coverage

### By Document Type
- **Invoices:** 7 tests (Tests 1-7)
- **Receipts:** 7 tests (Tests 8-14)
- **Business Cards:** 5 tests (Tests 15-18, 28)
- **Forms:** 4 tests (Tests 19-21, 29)
- **Bills:** 3 tests (Tests 22-24)
- **Multi-field:** 4 tests (Tests 25-27, 30)

### By Extraction Method
- **Reference Only:** 11 tests
- **Instructions Only:** 10 tests
- **Both Combined:** 9 tests

### By Priority
- **High Priority:** 10 tests
- **Medium Priority:** 14 tests
- **Low Priority:** 6 tests

## How to Use

### Option 1: Manual Testing (Excel/Sheets)

1. Open `TEST_SCENARIOS.csv` in Excel or Google Sheets
2. For each row:
   - Copy the **File Name**
   - Copy the **Reference Values** or **Instructions**
   - Run the curl command (see examples below)
   - Check if **Expected Fields** are extracted

### Option 2: Automated Testing

Use the provided test runner script (see below).

## Example Commands

### Test 1: Basic Invoice - Reference Only
```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@tests/sample_files/invoice_sample_001.png" \
  -F 'reference_values={"invoice_number": "Invoice Number", "date": "Date", "total": "Total"}'
```

### Test 2: Basic Invoice - Instructions Only
```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@tests/sample_files/invoice_sample_001.png" \
  -F "instructions=Extract the invoice number and total amount"
```

### Test 3: Basic Invoice - Both Methods
```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -F "file=@tests/sample_files/invoice_sample_001.png" \
  -F 'reference_values={"invoice_number": "Invoice Number"}' \
  -F "instructions=Also extract the billing address and due date"
```

## Automated Test Runner

Create a Python script to run all tests:

```python
import csv
import requests
import json

def run_test_from_csv(row):
    """Run a single test from CSV row."""
    url = "http://localhost:8000/api/v1/extract"
    file_path = f"tests/sample_files/{row['File Name']}"
    
    data = {}
    
    # Add reference values if present
    if row['Reference Values (JSON)']:
        data['reference_values'] = row['Reference Values (JSON)']
    
    # Add instructions if present
    if row['Instructions']:
        data['instructions'] = row['Instructions']
    
    # Make request
    with open(file_path, 'rb') as f:
        response = requests.post(
            url,
            files={'file': f},
            data=data
        )
    
    return response.json()

# Read CSV and run tests
with open('tests/TEST_SCENARIOS.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"Running Test {row['Test ID']}: {row['Test Name']}")
        result = run_test_from_csv(row)
        print(f"Status: {result['status']}")
        print(f"Extracted: {list(result['extracted_data'].keys())}")
        print()
```

## Test Scenarios Summary

### High Priority Tests (Must Pass)

1. **Basic Invoice - Reference Only** - Core functionality
2. **Basic Invoice - Instructions Only** - Natural language
3. **Basic Invoice - Both Methods** - Combined extraction
8. **Retail Receipt - Reference** - Receipt parsing
9. **Retail Receipt - Instructions** - Item extraction
15. **Business Card - Reference** - Contact extraction
16. **Business Card - Instructions** - Flexible contact info
19. **Registration Form - Reference** - Form fields
20. **Registration Form - Instructions** - Complete form
30. **Multi-Field Invoice** - Comprehensive extraction

### Medium Priority Tests (Should Pass)

4-7. **Various Invoice Types** - Different invoice formats
10-12. **Receipt Variations** - Restaurant, retail
17-18. **Business Card Variations** - Different layouts
21. **Form - Both Methods** - Hybrid form extraction
22-23. **Utility Bill** - Bill parsing
26. **Detailed Instructions** - Complex extraction

### Low Priority Tests (Nice to Have)

13-14. **Gas Station Receipt** - Fuel transactions
24. **Utility Bill - Both** - Complete bill info
25. **Minimal Reference** - Single field
27-29. **Specific Scenarios** - Edge cases

## Expected Results

Each test should return:
- `status: "success"`
- `extracted_data` containing the expected fields
- `processing_time` < 10 seconds
- `model_used: "gemini"`

## Tips for Testing

1. **Start with High Priority** tests first
2. **Test one method at a time** (Reference → Instructions → Both)
3. **Compare extracted fields** with Expected Fields column
4. **Note any discrepancies** in field names or values
5. **Check processing time** for performance issues

## Troubleshooting

### If a test fails:
1. Check if the file exists in `tests/sample_files/`
2. Verify JSON syntax in Reference Values
3. Check API server is running
4. Review error message in response
5. Try with different extraction method

### Common Issues:
- **Missing fields:** Try more specific reference values
- **Wrong field names:** Use instructions for flexible naming
- **Timeout:** File might be too large or complex
- **JSON error:** Check quotes and escaping in reference values

## Next Steps

1. Open CSV in Excel/Google Sheets
2. Start with Test ID 1
3. Run each test and mark results
4. Document any issues or improvements needed
5. Use results to optimize extraction prompts

---

**Happy Testing!** 🧪
