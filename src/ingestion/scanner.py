import asyncio
from pathlib import Path
from typing import List, Set
from src.config import SUPPORTED_IMAGE_EXTENSIONS, SUPPORTED_VIDEO_EXTENSIONS

async def scan_directory(directory: Path) -> List[Path]:
    """
    Asynchronously scans a directory for supported media files.
    """
    supported_extensions = SUPPORTED_IMAGE_EXTENSIONS.union(SUPPORTED_VIDEO_EXTENSIONS)
    media_files = []
    
    # Using run_in_executor for directory scanning if it's large, 
    # but for simplicity we'll use Path.rglob which is blocking.
    # In a more complex setup, we'd use a non-blocking walker.
    for ext in supported_extensions:
        media_files.extend(list(directory.rglob(f"*{ext}")))
        media_files.extend(list(directory.rglob(f"*{ext.upper()}")))
        
    return sorted(list(set(media_files)))
