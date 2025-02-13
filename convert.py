from markitdown import MarkItDown
from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Get environment variables
api_key = os.getenv('OPENAI_API_KEY')

# Check if API key exists
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Define input and output directories
input_dir = Path('assets/f2-vejledninger')
output_dir = Path('assets/f2-vejledninger-md')

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

client = OpenAI(api_key=api_key)
md = MarkItDown(llm_client=client, llm_model="gpt-4o-mini-2024-08-01-preview")
supported_extensions = ('.pptx', '.docx', '.pdf', '.jpg', '.jpeg', '.png')

# Get files from input directory
files_to_convert = [f for f in os.listdir(input_dir) if f.lower().endswith(supported_extensions)]

for file in files_to_convert:
    print(f"\nConverting {file}...")
    try:
        input_path = input_dir / file
        output_path = output_dir / (Path(file).stem + '.md')
        
        result = md.convert(str(input_path))
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.text_content)
        
        print(f"Successfully converted {file} to {output_path}")
    except Exception as e:
        print(f"Error converting {file}: {str(e)}")

print("\nAll conversions completed!")