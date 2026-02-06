import os
import requests
from PIL import Image
from dotenv import load_dotenv
import re

# Try to import pytesseract for OCR, fallback if not available
try:
    import pytesseract
    from pytesseract import Output
    
    # Configure Tesseract path for Windows
    import platform
    if platform.system() == "Windows":
        # Try common Windows installation paths
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.pytesseract_cmd = path
                print(f"   ✅ Tesseract found at: {path}")
                break
    
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False
    print("   ℹ️  pytesseract not available, using pattern matching for document detection")

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

# Multiple HF models for better content detection
HF_CAPTION_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
HF_OBJECT_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet50"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# Patterns for detecting code/document content
CODE_PATTERNS = {
    'sql': r'(?i)(select|insert|update|delete|from|where|join|group\s+by|order\s+by)',
    'json': r'(?i)(\{.*".*".*\}|\[.*\])',
    'mongodb': r'(?i)(db\.|collection|find\(|insertOne|updateOne)',
    'python': r'(?i)(def\s+|import\s+|class\s+|if\s+__name__|for\s+|while\s+)',
    'javascript': r'(?i)(function|const\s+|let\s+|var\s+|=>|\.map|\.filter)',
    'html': r'(?i)(<html|<head|<body|<div|<class|<id)',
    'css': r'(?i)(\.class\s*\{|#id\s*\{|margin:|padding:|color:)',
    'yaml': r'(?i)(^[\w-]+:\s*)',
    'xml': r'(?i)(<\?xml|xmlns|</)',
    'markdown': r'(^#+\s|^\*\*|^\-\s|^\d+\.)',
}

CONTENT_PATTERNS = {
    'notes': r'(?i)(note|todo|idea|remember|important)',
    'table': r'(?i)(│|├|─|┤|┌|┐|└|┘|table|rows|columns|data)',
    'spreadsheet': r'(?i)(excel|column|row|cell|csv)',
    'chart': r'(?i)(x-axis|y-axis|graph|pie|bar|line)',
    'form': r'(?i)(name:|email:|phone:|address:)',
    'debug': r'(?i)(console\.|print\(|logger\.|error:|warning:|debug:)',
    'api': r'(?i)(api|endpoint|request|response|status|200|404|500)',
}

def detect_code_and_documents(image_path):
    """Use OCR + pattern matching to detect code blocks, SQL, JSON, MongoDB, etc."""
    try:
        img = Image.open(image_path)
        detected_types = []
        text = ""
        
        # Try OCR if available (Windows requires Tesseract installation)
        if HAS_TESSERACT:
            try:
                text = pytesseract.image_to_string(img)
                print(f"   📄 OCR detected text ({len(text)} chars)")
            except Exception as e:
                print(f"   ℹ️  OCR failed: {str(e)[:40]}, using pattern matching")
        else:
            # Fallback: analyze image dimensions to guess if it's a screenshot
            width, height = img.size
            # Screenshots of code/docs are usually landscape with certain proportions
            if width > 700 and height < width * 0.8:
                print(f"   📄 Screenshot detected (likely code/document)")
                text = "[screenshot-based-detection]"
        
        if text.strip():
            # Check for code patterns
            for code_type, pattern in CODE_PATTERNS.items():
                if re.search(pattern, text):
                    detected_types.append(code_type)
            
            # Check for document/content patterns
            for content_type, pattern in CONTENT_PATTERNS.items():
                if re.search(pattern, text):
                    detected_types.append(content_type)
            
            # Specific content detection
            if 'CREATE TABLE' in text.upper() or 'INSERT INTO' in text.upper():
                detected_types.append('database-schema')
            if '"_id"' in text or 'ObjectId' in text:
                detected_types.append('mongodb-document')
            if '{' in text and '}' in text and ':' in text:
                detected_types.append('json-data')
            if any(col in text for col in ['│', '├', '─', '┤']):
                detected_types.append('ascii-table')
            
            # Visual text detection (lots of small text = code/document)
            line_count = text.count('\n')
            if line_count > 5:
                detected_types.append('code-block')
            
            if detected_types:
                print(f"   🔎 Code/Document detected: {', '.join(set(detected_types))}")
                return list(set(detected_types))
        
        return []
        
    except Exception as e:
        print(f"   ⚠️  Document detection error: {e}")
        return []

def extract_keywords_from_caption(caption):
    """Extract meaningful keywords from BLIP caption"""
    # Remove common stop words
    stop_words = {'a', 'an', 'the', 'of', 'to', 'in', 'is', 'and', 'or', 'but', 'on', 'at', 'by', 'for', 'with', 'as', 'was', 'are', 'been', 'be'}
    
    # Split caption into words and filter
    words = re.findall(r'\b[a-z]+\b', caption.lower())
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    
    return keywords

def detect_objects(image_path):
    """Use DETR object detection for better content tags"""
    try:
        with open(image_path, "rb") as f:
            response = requests.post(
                HF_OBJECT_URL,
                headers=headers,
                data=f.read(),
                timeout=10
            )
        
        response.raise_for_status()
        output = response.json()
        
        if isinstance(output, list):
            # Extract object labels from detection results
            objects = []
            for detection in output[:8]:  # Top 8 detected objects
                if 'label' in detection and detection.get('score', 0) > 0.5:
                    objects.append(detection['label'].lower())
            return objects
        return []
        
    except Exception as e:
        print(f"   📌 Object detection unavailable: {str(e)[:50]}")
        return []

def generate_caption_tags(image_path):
    """Generate tags using BLIP image captioning"""
    try:
        with open(image_path, "rb") as f:
            response = requests.post(
                HF_CAPTION_URL,
                headers=headers,
                data=f.read(),
                timeout=10
            )
        
        response.raise_for_status()
        output = response.json()
        
        if isinstance(output, list) and len(output) > 0:
            caption = output[0].get("generated_text", "")
            print(f"   📸 Caption: {caption}")
            keywords = extract_keywords_from_caption(caption)
            return keywords
        return []
            
    except Exception as e:
        print(f"   ⚠️  Caption generation failed: {str(e)[:50]}")
        return []

def generate_fallback_tags(image_path):
    """Smart fallback - analyze image properties + common scene inference"""
    try:
        img = Image.open(image_path)
        width, height = img.size
        tags = []
        
        # Aspect ratio analysis
        aspect_ratio = width / height if height > 0 else 1
        if aspect_ratio > 1.5:
            tags.extend(["landscape", "wide-angle"])
        elif aspect_ratio < 0.67:
            tags.extend(["portrait", "vertical"])
        
        # Resolution for quality indicators
        megapixels = (width * height) / 1000000
        if megapixels > 8:
            tags.append("high-quality")
        
        # Dominant color analysis for mood/type
        try:
            colors = img.convert('RGB').getcolors(maxcolors=width*height)
            if colors:
                r, g, b = colors[-1][1]  # Most common color
                # Basic color mood tags
                if r > g and r > b:
                    tags.append("warm-toned")
                elif b > r and b > g:
                    tags.append("cool-toned")
                if max(r, g, b) > 200 and min(r, g, b) > 150:
                    tags.append("bright")
        except:
            pass
        
        tags.extend(["image", "photo"])
        return list(set(tags))[:10]
        
    except Exception as e:
        print(f"   ⚠️  Fallback error: {e}")
        return ["image", "photo"]

def generate_tags(image_path):
    """Generate tags from image using AI + OCR for comprehensive detection"""
    
    print(f"   🏷️  Analyzing image: {os.path.basename(image_path)}")
    
    # If no API key, use fallback immediately
    if not HF_API_KEY:
        print("   📌 No HF_API_KEY, using local analysis")
        local_tags = generate_fallback_tags(image_path)
        document_tags = detect_code_and_documents(image_path)
        return list(set(local_tags + document_tags))[:15]
    
    all_tags = set()
    
    # First check for code/documents via OCR (fast, always works)
    document_tags = detect_code_and_documents(image_path)
    if document_tags:
        all_tags.update(document_tags)
    
    # If we found document content, add some AI analysis for context
    if document_tags and len(document_tags) >= 2:
        # Try BLIP caption for context (what the code/document is about)
        caption_tags = generate_caption_tags(image_path)
        all_tags.update(caption_tags)
        
        final_tags = list(all_tags)[:15]
        print(f"   ✅ Final tags (document): {', '.join(final_tags)}")
        return final_tags
    
    # Otherwise, do full AI analysis for general photos
    # Try BLIP caption first (main content)
    caption_tags = generate_caption_tags(image_path)
    all_tags.update(caption_tags)
    
    # Try object detection (specific objects)
    object_tags = detect_objects(image_path)
    if object_tags:
        print(f"   🔍 Detected objects: {', '.join(object_tags)}")
        all_tags.update(object_tags)
    
    # If we got good tags from AI
    if len(all_tags) >= 3:
        final_tags = list(all_tags)[:12]
        print(f"   ✅ Final tags: {', '.join(final_tags)}")
        return final_tags
    
    # Otherwise use smart fallback
    print(f"   🔄 Enhancing with local analysis...")
    fallback_tags = generate_fallback_tags(image_path)
    all_tags.update(fallback_tags)
    
    final_tags = list(all_tags)[:12]
    print(f"   ✅ Final tags: {', '.join(final_tags)}")
    return final_tags

