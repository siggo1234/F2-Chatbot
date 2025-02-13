from markitdown import MarkItDown
from openai import AzureOpenAI
import os
from pathlib import Path
import sys
from dotenv import load_dotenv, find_dotenv
from urllib.parse import urlparse

def get_base_url_from_endpoint(endpoint_url):
    """Extract base URL from full endpoint URL"""
    parsed = urlparse(endpoint_url)
    return f"{parsed.scheme}://{parsed.netloc}"

def convert_pdfs_to_markdown(input_dir, output_dir):
    """
    Convert all PDF files in input_dir to Markdown files in output_dir
    using MarkItDown library with Azure OpenAI
    """
    # Load environment variables and print status
    env_path = find_dotenv()
    if not env_path:
        print("Error: .env file not found")
        sys.exit(1)
        
    load_dotenv(env_path)
    print(f"Loading environment from: {env_path}")
    
    # Get environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    full_endpoint = os.getenv('OPENAI_ENDPOINT')
    model_name = os.getenv('CHAT_MODEL')
    
    # Validate environment variables
    if not all([api_key, full_endpoint, model_name]):
        print("\nError: Missing required environment variables")
        print(f"OPENAI_API_KEY: {'Found' if api_key else 'Missing'}")
        print(f"OPENAI_ENDPOINT: {'Found' if full_endpoint else 'Missing'}")
        print(f"CHAT_MODEL: {'Found' if model_name else 'Missing'}")
        sys.exit(1)
    
    # Get base URL for Azure OpenAI client
    base_url = get_base_url_from_endpoint(full_endpoint)
    
    print("\nConfiguration:")
    print(f"Base URL: {base_url}")
    print(f"Model: {model_name}")
    
    try:
        # Initialize Azure OpenAI client
        client = AzureOpenAI(
            api_key=api_key,
            api_version="2024-08-01-preview",
            azure_endpoint=base_url
        )
        
        # Initialize MarkItDown with just the required parameters
        md = MarkItDown(
            llm_client=client,
            llm_model=model_name
        )
        
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Get all PDF files
        pdf_files = list(Path(input_dir).glob('*.pdf'))
        total_files = len(pdf_files)
        print(f"\nFound {total_files} PDF files to convert")
        
        # # Set console to UTF-8 mode on Windows
        # if sys.platform == 'win32':
        #     os.system('chcp 65001')
        
        # Process each PDF
        for index, pdf_path in enumerate(pdf_files, 1):
            print(f"\nProcessing {index}/{total_files}: {pdf_path.name}")
            
            try:
                # Create output markdown filename
                markdown_path = Path(output_dir) / f"{pdf_path.stem}.md"
                
                # Convert the file
                result = md.convert(str(pdf_path))
                
                # Write the result to file with UTF-8 encoding
                with open(markdown_path, 'w', encoding='utf-8') as f:
                    f.write(result.text_content)
                    
                print(f"✓ Successfully converted to {markdown_path.name}")
                
            except Exception as e:
                print(f"✗ Error processing {pdf_path.name}")
                print(f"Error details: {str(e)}")
                import traceback
                print(traceback.format_exc())
                
    except Exception as e:
        print(f"✗ Error initializing Azure OpenAI client or MarkItDown:")
        print(f"Error details: {str(e)}")
        import traceback
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    input_directory = "assets/f2-vejledninger"
    output_directory = "assets/f2-vejledninger-md"
    
    print("Starting PDF to Markdown conversion...")
    convert_pdfs_to_markdown(input_directory, output_directory)
    print("\nConversion process completed!")