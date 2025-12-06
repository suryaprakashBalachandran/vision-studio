# Vision Studio API - Comprehensive Test Results

**Date:** 2025-12-06 16:53:28  
**Total Tests:** 30  
**Passed:** 8 ✅  
**Partial:** 14 ⚠️  
**Failed:** 8 ❌  
**Average Processing Time:** 3.24s  

---

## Test Results

### ✅ Test 1: Basic Invoice - Reference Only

**Status:** success  
**Processing Time:** 3.80s  

**Extracted Data:**
```json
{
  "invoice_number": "INV-2024-001",
  "date": "January 15, 2024",
  "total": "$9,765"
}
```

**Expected Fields:** invoice_number, date, total  
**Found:** 3/3  

---

### ⚠️ Test 2: Basic Invoice - Instructions Only

**Status:** success  
**Processing Time:** 11.77s  

**Extracted Data:**
```json
{
  "invoice_number": "INV-2024-001",
  "total_amount": "$9,765"
}
```

**Expected Fields:** invoice_number, total  
**Found:** 1/2  
**Missing:** total  

---

### ⚠️ Test 3: Basic Invoice - Both Methods

**Status:** success  
**Processing Time:** 3.21s  

**Extracted Data:**
```json
{
  "invoice_number": "INV-2024-001"
}
```

**Expected Fields:** invoice_number, billing_address, due_date  
**Found:** 1/3  
**Missing:** billing_address, due_date  

---

### ✅ Test 4: Freelance Invoice - Reference

**Status:** success  
**Processing Time:** 4.02s  

**Extracted Data:**
```json
{
  "invoice_number": "FRL-2024-156",
  "client": "StartUp Ventures LLC",
  "total": "$4,275.00",
  "discount": "-$475.00"
}
```

**Expected Fields:** invoice_number, client, total, discount  
**Found:** 4/4  

---

### ⚠️ Test 5: Freelance Invoice - Instructions

**Status:** success  
**Processing Time:** 3.77s  

**Extracted Data:**
```json
{
  "client_name": "StartUp Ventures LLC",
  "service_line_items": [
    {
      "description": "Logo Design & Branding",
      "total_price": "$2,500.00"
    },
    {
      "description": "Website Mockups",
      "total_price": "$1,500.00"
    },
    {
      "description": "Social Media Graphics",
      "total_price": "$750.00"
    }
  ]
}
```

**Expected Fields:** client, services, total  
**Found:** 0/3  
**Missing:** client, services, total  

---

### ⚠️ Test 6: Medical Invoice - Reference

**Status:** success  
**Processing Time:** 4.59s  

**Extracted Data:**
```json
{
  "patient_name": "Michael Chen",
  "patient_id": "PMC-789456",
  "insurance": "Blue Cross PPO"
}
```

**Expected Fields:** patient_name, patient_id, total, insurance  
**Found:** 3/4  
**Missing:** total  

---

### ⚠️ Test 7: Medical Invoice - Both

**Status:** success  
**Processing Time:** 3.03s  

**Extracted Data:**
```json
{
  "patient_id": "PMC-789456"
}
```

**Expected Fields:** patient_id, services, costs  
**Found:** 1/3  
**Missing:** services, costs  

---

### ✅ Test 8: Retail Receipt - Reference

**Status:** success  
**Processing Time:** 3.38s  

**Extracted Data:**
```json
{
  "store": "SUPER MART",
  "date": "Dec 5, 2024",
  "total": "$39.89",
  "tax": "$2.96"
}
```

**Expected Fields:** store, date, total, tax  
**Found:** 4/4  

---

### ⚠️ Test 9: Retail Receipt - Instructions

**Status:** success  
**Processing Time:** 4.08s  

**Extracted Data:**
```json
{
  "purchased_items": [
    {
      "item_name": "Organic Bananas",
      "item_price": 3.99
    },
    {
      "item_name": "Whole Milk 1gal",
      "item_price": 4.49
    },
    {
      "item_name": "Bread - Whole Wheat",
      "item_price": 2.99
    },
    {
      "item_name": "Chicken Breast 2lb",
      "item_price": 12.98
    },
    {
      "item_name": "Orange Juice",
      "item_price": 5.49
    },
    {
      "item_name": "Greek Yogurt",
      "item_price": 6.99
    }
  ],
  "subtotal": 36.93
}
```

**Expected Fields:** items, prices, subtotal  
**Found:** 1/3  
**Missing:** items, prices  

---

### ⚠️ Test 10: Retail Receipt - Both

**Status:** success  
**Processing Time:** 3.61s  

**Extracted Data:**
```json
{
  "store": "SUPER MART",
  "total": "$39.89"
}
```

**Expected Fields:** store, total, payment_method, cashier  
**Found:** 2/4  
**Missing:** payment_method, cashier  

---

### ✅ Test 11: Restaurant Receipt - Reference

**Status:** success  
**Processing Time:** 4.33s  

**Extracted Data:**
```json
{
  "restaurant": "BELLA ITALIA",
  "total": "$129.00",
  "tip": "$20.00",
  "tax": "$9.00"
}
```

**Expected Fields:** restaurant, total, tip, tax  
**Found:** 4/4  

---

### ❌ Test 12: Restaurant Receipt - Instructions

**Status:** error  
**Processing Time:** 0.50s  
**Expected Fields:** restaurant, items, prices  
**Found:** 0/3  
**Missing:** restaurant, items, prices  

**Error:** 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/usage?tab=rate-limit. 
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 10, model: gemini-2.5-flash
Please retry in 28.650768849s. [links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-2.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 10
}
, retry_delay {
  seconds: 28
}
]  

---

### ❌ Test 13: Gas Station Receipt - Reference

**Status:** error  
**Processing Time:** 0.51s  
**Expected Fields:** station, gallons, price_per_gallon, total  
**Found:** 0/4  
**Missing:** station, gallons, price_per_gallon, total  

**Error:** 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/usage?tab=rate-limit. 
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 10, model: gemini-2.5-flash
Please retry in 27.620728828s. [links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-2.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 10
}
, retry_delay {
  seconds: 27
}
]  

---

### ❌ Test 14: Gas Station Receipt - Both

**Status:** error  
**Processing Time:** 0.55s  
**Expected Fields:** total, fuel_type, additional_items  
**Found:** 0/3  
**Missing:** total, fuel_type, additional_items  

**Error:** 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/usage?tab=rate-limit. 
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 10, model: gemini-2.5-flash
Please retry in 26.570608546s. [links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-2.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 10
}
, retry_delay {
  seconds: 26
}
]  

---

### ❌ Test 15: Business Card - Reference

**Status:** error  
**Processing Time:** 0.54s  
**Expected Fields:** name, title, company, email, phone  
**Found:** 0/5  
**Missing:** name, title, company, email, phone  

**Error:** 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/usage?tab=rate-limit. 
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 10, model: gemini-2.5-flash
Please retry in 25.527748632s. [links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-2.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 10
}
, retry_delay {
  seconds: 25
}
]  

---

### ❌ Test 16: Business Card - Instructions

**Status:** error  
**Processing Time:** 0.54s  
**Expected Fields:** name, email, phone, address, company  
**Found:** 0/5  
**Missing:** name, email, phone, address, company  

**Error:** 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/usage?tab=rate-limit. 
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 10, model: gemini-2.5-flash
Please retry in 24.518119952s. [links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-2.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 10
}
, retry_delay {
  seconds: 24
}
]  

---

### ⚠️ Test 17: Business Card - Both

**Status:** success  
**Processing Time:** 3.49s  

**Extracted Data:**
```json
{
  "name": "JOHN ANDERSON",
  "email": "john.anderson@techvision.com"
}
```

**Expected Fields:** name, email, website, social_media  
**Found:** 2/4  
**Missing:** website, social_media  

---

### ⚠️ Test 18: Creative Business Card - Instructions

**Status:** success  
**Processing Time:** 3.89s  

**Extracted Data:**
```json
{
  "name": "Maria Santos",
  "email": "maria@pixelperfect.co",
  "website": "www.pixelperfect.co",
  "phone_number": "+1 (555) 345-6789",
  "address": "250 Design District, Miami, FL 33130"
}
```

**Expected Fields:** name, email, phone, website  
**Found:** 3/4  
**Missing:** phone  

---

### ✅ Test 19: Registration Form - Reference

**Status:** success  
**Processing Time:** 4.34s  

**Extracted Data:**
```json
{
  "full_name": "Emily Rodriguez",
  "email": "emily.rodriguez@email.com",
  "phone": "(555) 876-5432",
  "address": "234 Oak Avenue, Apt 5B, Portland, OR 97201"
}
```

**Expected Fields:** full_name, email, phone, address  
**Found:** 4/4  

---

### ⚠️ Test 20: Registration Form - Instructions

**Status:** success  
**Processing Time:** 4.87s  

**Extracted Data:**
```json
{
  "full_name": "Emily Rodriguez",
  "email": "emily.rodriguez@email.com",
  "phone": "(555) 876-5432",
  "date_of_birth": "03/15/1990",
  "address": "234 Oak Avenue, Apt 5B",
  "city": "Portland",
  "state": "OR",
  "zip": "97201",
  "preferred_contact_method": {
    "email": true,
    "phone": false,
    "mail": false
  },
  "newsletter_subscription": {
    "yes": true,
    "no": false
  },
  "signature": "Emily Rodriguez",
  "signature_date": "12/01/2024"
}
```

**Expected Fields:** all_fields, checkboxes, signature  
**Found:** 1/3  
**Missing:** all_fields, checkboxes  

---

### ⚠️ Test 21: Registration Form - Both

**Status:** success  
**Processing Time:** 3.30s  

**Extracted Data:**
```json
{
  "full_name": "Emily Rodriguez",
  "email": "emily.rodriguez@email.com"
}
```

**Expected Fields:** full_name, email, dob, checkboxes  
**Found:** 2/4  
**Missing:** dob, checkboxes  

---

### ✅ Test 22: Utility Bill - Reference

**Status:** success  
**Processing Time:** 4.48s  

**Extracted Data:**
```json
{
  "account_number": "9876543210",
  "customer_name": "Jennifer Williams",
  "usage": "450",
  "total": "$98.45"
}
```

**Expected Fields:** account_number, customer_name, usage, total  
**Found:** 4/4  

---

### ⚠️ Test 23: Utility Bill - Instructions

**Status:** success  
**Processing Time:** 4.67s  

**Extracted Data:**
```json
{
  "billing_period": "Nov 1 - Nov 30, 2024",
  "charges_breakdown": {
    "energy_charge": "$67.50",
    "delivery_charge": "$22.00",
    "taxes_and_fees": "$8.95",
    "total_current_charges": "$98.45"
  }
}
```

**Expected Fields:** billing_period, charges, total  
**Found:** 1/3  
**Missing:** charges, total  

---

### ⚠️ Test 24: Utility Bill - Both

**Status:** success  
**Processing Time:** 3.81s  

**Extracted Data:**
```json
{
  "account_number": "9876543210",
  "total": "$98.45"
}
```

**Expected Fields:** account_number, total, due_date, payment_options  
**Found:** 2/4  
**Missing:** due_date, payment_options  

---

### ✅ Test 25: Invoice - Minimal Reference

**Status:** success  
**Processing Time:** 3.20s  

**Extracted Data:**
```json
{
  "total": "$9,765"
}
```

**Expected Fields:** total  
**Found:** 1/1  

---

### ⚠️ Test 26: Invoice - Detailed Instructions

**Status:** success  
**Processing Time:** 4.32s  

**Extracted Data:**
```json
{
  "invoice_number": "INV-2024-001",
  "services": [
    {
      "description": "Web Development Services",
      "quantity": "40 hours",
      "unit_price": "$150/hr"
    },
    {
      "description": "UI/UX Design",
      "quantity": "20 hours",
      "unit_price": "$125/hr"
    },
    {
      "description": "Hosting & Maintenance",
      "quantity": "1 month",
      "unit_price": "$500"
    }
  ]
}
```

**Expected Fields:** invoice_number, services, quantities, prices  
**Found:** 2/4  
**Missing:** quantities, prices  

---

### ✅ Test 27: Receipt - Payment Method

**Status:** success  
**Processing Time:** 3.17s  

**Extracted Data:**
```json
{
  "payment_method": "VISA",
  "receipt_number": "RCP-45678"
}
```

**Expected Fields:** payment_method, receipt_number  
**Found:** 2/2  

---

### ❌ Test 28: Business Card - Minimal

**Status:** error  
**Processing Time:** 0.49s  
**Expected Fields:** email  
**Found:** 0/1  
**Missing:** email  

**Error:** 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/usage?tab=rate-limit. 
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 10, model: gemini-2.5-flash
Please retry in 34.314853087s. [links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-2.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 10
}
, retry_delay {
  seconds: 34
}
]  

---

### ❌ Test 29: Form - Checkbox Focus

**Status:** error  
**Processing Time:** 0.54s  
**Expected Fields:** checkboxes  
**Found:** 0/1  
**Missing:** checkboxes  

**Error:** 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/usage?tab=rate-limit. 
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 10, model: gemini-2.5-flash
Please retry in 33.295416074s. [links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-2.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 10
}
, retry_delay {
  seconds: 33
}
]  

---

### ❌ Test 30: Multi-Field Invoice

**Status:** error  
**Processing Time:** 0.49s  
**Expected Fields:** invoice_number, date, due_date, bill_to, subtotal, tax, total  
**Found:** 0/7  
**Missing:** invoice_number, date, due_date, bill_to, subtotal, tax, total  

**Error:** 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/usage?tab=rate-limit. 
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 10, model: gemini-2.5-flash
Please retry in 32.259991347s. [links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-2.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 10
}
, retry_delay {
  seconds: 32
}
]  

---

