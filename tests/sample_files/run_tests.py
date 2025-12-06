#!/usr/bin/env python3
"""
Test runner for Vision Studio API using sample files.
Runs all test cases defined in test_cases.json and reports results.
"""

import json
import os
import sys
import requests
from pathlib import Path
from typing import Dict, Any, List
import time


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class APITester:
    """Test runner for Vision Studio API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_endpoint = f"{base_url}/api/v1/extract"
        self.results: List[Dict[str, Any]] = []
        
    def load_test_cases(self, test_file: str = "test_cases.json") -> List[Dict[str, Any]]:
        """Load test cases from JSON file."""
        test_file_path = Path(__file__).parent / test_file
        
        if not test_file_path.exists():
            print(f"{Colors.RED}Error: Test cases file not found: {test_file_path}{Colors.RESET}")
            sys.exit(1)
            
        with open(test_file_path, 'r') as f:
            data = json.load(f)
            return data.get('test_cases', [])
    
    def run_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single test case."""
        test_name = test_case['name']
        file_name = test_case['file']
        ai_model = test_case['ai_model']
        extraction_type = test_case['extraction_type']
        
        # Build file path
        file_path = Path(__file__).parent / file_name
        
        if not file_path.exists():
            return {
                'test_name': test_name,
                'status': 'FAILED',
                'error': f'File not found: {file_name}',
                'processing_time': 0
            }
        
        # Prepare request
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {'ai_model': ai_model}
                
                if extraction_type == 'reference':
                    data['reference_values'] = json.dumps(test_case['reference_values'])
                elif extraction_type == 'instruction':
                    data['instructions'] = test_case['instructions']
                
                # Make API request
                start_time = time.time()
                response = requests.post(self.api_endpoint, files=files, data=data, timeout=60)
                elapsed_time = time.time() - start_time
                
                # Parse response
                if response.status_code == 200:
                    result = response.json()
                    
                    # Check if expected fields are present
                    expected_fields = test_case.get('expected_fields', [])
                    extracted_data = result.get('extracted_data', {})
                    
                    missing_fields = []
                    for field in expected_fields:
                        if field not in extracted_data or not extracted_data[field]:
                            missing_fields.append(field)
                    
                    status = 'PASSED' if not missing_fields else 'PARTIAL'
                    
                    return {
                        'test_name': test_name,
                        'status': status,
                        'api_status': result.get('status'),
                        'model_used': result.get('model_used'),
                        'processing_time': result.get('processing_time', elapsed_time),
                        'extracted_data': extracted_data,
                        'missing_fields': missing_fields,
                        'pages_processed': result.get('pages_processed', 1)
                    }
                else:
                    return {
                        'test_name': test_name,
                        'status': 'FAILED',
                        'error': f'HTTP {response.status_code}: {response.text}',
                        'processing_time': elapsed_time
                    }
                    
        except requests.exceptions.ConnectionError:
            return {
                'test_name': test_name,
                'status': 'FAILED',
                'error': 'Could not connect to API. Is the server running?',
                'processing_time': 0
            }
        except Exception as e:
            return {
                'test_name': test_name,
                'status': 'FAILED',
                'error': str(e),
                'processing_time': 0
            }
    
    def print_result(self, result: Dict[str, Any]):
        """Print a single test result."""
        status = result['status']
        test_name = result['test_name']
        
        # Color code based on status
        if status == 'PASSED':
            status_color = Colors.GREEN
            status_symbol = '✓'
        elif status == 'PARTIAL':
            status_color = Colors.YELLOW
            status_symbol = '⚠'
        else:
            status_color = Colors.RED
            status_symbol = '✗'
        
        print(f"\n{status_color}{status_symbol} {status}{Colors.RESET} - {Colors.BOLD}{test_name}{Colors.RESET}")
        
        if 'error' in result:
            print(f"  {Colors.RED}Error: {result['error']}{Colors.RESET}")
        else:
            print(f"  Model: {result.get('model_used', 'N/A')}")
            print(f"  Processing Time: {result.get('processing_time', 0):.2f}s")
            
            if status == 'PARTIAL' and result.get('missing_fields'):
                print(f"  {Colors.YELLOW}Missing Fields: {', '.join(result['missing_fields'])}{Colors.RESET}")
            
            if result.get('extracted_data'):
                print(f"  {Colors.BLUE}Extracted Data:{Colors.RESET}")
                for key, value in result['extracted_data'].items():
                    # Truncate long values
                    value_str = str(value)
                    if len(value_str) > 60:
                        value_str = value_str[:57] + "..."
                    print(f"    • {key}: {value_str}")
    
    def run_all_tests(self):
        """Run all test cases and print summary."""
        print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}Vision Studio API Test Runner{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*70}{Colors.RESET}")
        print(f"API Endpoint: {self.api_endpoint}\n")
        
        # Load test cases
        test_cases = self.load_test_cases()
        total_tests = len(test_cases)
        
        print(f"Running {total_tests} test cases...\n")
        
        # Run each test
        for i, test_case in enumerate(test_cases, 1):
            print(f"{Colors.BOLD}[{i}/{total_tests}]{Colors.RESET} Running: {test_case['name']}...")
            result = self.run_test_case(test_case)
            self.results.append(result)
            self.print_result(result)
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary."""
        passed = sum(1 for r in self.results if r['status'] == 'PASSED')
        partial = sum(1 for r in self.results if r['status'] == 'PARTIAL')
        failed = sum(1 for r in self.results if r['status'] == 'FAILED')
        total = len(self.results)
        
        print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}Test Summary{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*70}{Colors.RESET}")
        print(f"Total Tests: {total}")
        print(f"{Colors.GREEN}Passed: {passed}{Colors.RESET}")
        print(f"{Colors.YELLOW}Partial: {partial}{Colors.RESET}")
        print(f"{Colors.RED}Failed: {failed}{Colors.RESET}")
        
        # Calculate average processing time
        processing_times = [r.get('processing_time', 0) for r in self.results if r['status'] != 'FAILED']
        if processing_times:
            avg_time = sum(processing_times) / len(processing_times)
            print(f"\nAverage Processing Time: {avg_time:.2f}s")
        
        print(f"{Colors.BOLD}{'='*70}{Colors.RESET}\n")
        
        # Exit with appropriate code
        if failed > 0:
            sys.exit(1)
        elif partial > 0:
            sys.exit(2)
        else:
            sys.exit(0)


def main():
    """Main entry point."""
    # Parse command line arguments
    base_url = "http://localhost:8000"
    
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    # Run tests
    tester = APITester(base_url)
    tester.run_all_tests()


if __name__ == "__main__":
    main()
