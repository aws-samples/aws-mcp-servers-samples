#!/usr/bin/env python3
"""
Simple test script to verify the S3 upload server functionality
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from server import upload_file

def test_upload():
    """Test the upload_file function"""
    print("Testing S3 upload server...")
    
    # Test with a simple text file
    test_content = "Hello, World! This is a test file uploaded via MCP server."
    test_filename = "test-file.txt"
    
    try:
        result = upload_file(test_filename, test_content)
        print("Upload result:")
        print(result)
    except Exception as e:
        print(f"Error during test: {str(e)}")

if __name__ == "__main__":
    test_upload()
