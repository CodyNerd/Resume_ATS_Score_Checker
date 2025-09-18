#!/usr/bin/env python3
"""
Test script to debug PDF parsing issues
"""

import os
import io

def test_imports():
    print("Testing imports...")
    
    try:
        import PyPDF2
        print("✅ PyPDF2 imported successfully")
        print(f"   Version: {PyPDF2.__version__}")
    except ImportError as e:
        print(f"❌ PyPDF2 import failed: {e}")
        return False
    
    try:
        from docx import Document
        print("✅ python-docx imported successfully")
    except ImportError as e:
        print(f"❌ python-docx import failed: {e}")
    
    try:
        from utils.parser import extract_text
        print("✅ utils.parser imported successfully")
    except ImportError as e:
        print(f"❌ utils.parser import failed: {e}")
        return False
    
    return True

def test_pdf_parsing():
    print("\nTesting PDF parsing...")
    
    pdf_file = "RESUME-1.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"❌ PDF file '{pdf_file}' not found in current directory")
        return
    
    print(f"✅ Found PDF file: {pdf_file}")
    print(f"   File size: {os.path.getsize(pdf_file)} bytes")
    
    # Test direct PyPDF2 parsing
    try:
        import PyPDF2
        print("\n--- Testing direct PyPDF2 parsing ---")
        
        with open(pdf_file, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            print(f"✅ PDF loaded successfully")
            print(f"   Number of pages: {len(pdf_reader.pages)}")
            
            text_content = []
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                text_content.append(page_text)
                print(f"   Page {page_num + 1}: {len(page_text)} characters")
            
            full_text = '\n'.join(text_content)
            print(f"✅ Total extracted text: {len(full_text)} characters")
            
            if full_text.strip():
                print("✅ Text extraction successful")
                print("   Preview:", full_text[:200] + "..." if len(full_text) > 200 else full_text)
            else:
                print("❌ No text extracted from PDF")
                
    except Exception as e:
        print(f"❌ Direct PyPDF2 parsing failed: {e}")
    
    # Test using our parser function
    try:
        from utils.parser import extract_text_from_pdf
        print("\n--- Testing utils.parser.extract_text_from_pdf ---")
        
        # Create a mock uploaded file object
        class MockUploadedFile:
            def __init__(self, file_path):
                self.name = os.path.basename(file_path)
                with open(file_path, 'rb') as f:
                    self._content = f.read()
                self._position = 0
            
            def read(self):
                content = self._content[self._position:]
                self._position = len(self._content)
                return content
            
            def seek(self, position):
                self._position = position
        
        mock_file = MockUploadedFile(pdf_file)
        extracted_text = extract_text_from_pdf(mock_file)
        
        print(f"✅ Parser function successful")
        print(f"   Extracted text length: {len(extracted_text)}")
        print("   Preview:", extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text)
        
    except Exception as e:
        print(f"❌ Parser function failed: {e}")

if __name__ == "__main__":
    if test_imports():
        test_pdf_parsing()
    else:
        print("❌ Import tests failed, skipping PDF parsing test")