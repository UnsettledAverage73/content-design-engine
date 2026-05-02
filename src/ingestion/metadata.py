import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from PIL import Image
from PIL.ExifTags import TAGS
import exifread

def extract_metadata(file_path: Path) -> Dict[str, Any]:
    """
    Extracts metadata from an image or video file.
    """
    metadata = {
        "file_name": file_path.name,
        "file_path": str(file_path),
        "file_size": file_path.stat().st_size,
        "creation_time": datetime.datetime.fromtimestamp(file_path.stat().st_ctime).isoformat(),
        "extension": file_path.suffix.lower()
    }

    if file_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
        metadata.update(extract_image_metadata(file_path))
    
    return metadata

def extract_image_metadata(file_path: Path) -> Dict[str, Any]:
    img_metadata = {}
    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
            if tags:
                for tag in tags.keys():
                    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                        img_metadata[tag] = str(tags[tag])
    except Exception as e:
        img_metadata["error"] = f"Failed to extract EXIF: {str(e)}"
        
    try:
        with Image.open(file_path) as img:
            img_metadata["width"], img_metadata["height"] = img.size
            img_metadata["format"] = img.format
    except Exception as e:
        img_metadata["pil_error"] = f"Failed to open with PIL: {str(e)}"
        
    return img_metadata
