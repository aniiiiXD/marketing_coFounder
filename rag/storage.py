"""
Storage Service - Simple Local Implementation

Handles local file storage and retrieval for the RAG system.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class StorageService:
    """Simple local storage service"""
    
    def __init__(self, storage_path: str = "storage"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.storage_path / "outputs").mkdir(exist_ok=True)
        (self.storage_path / "cache").mkdir(exist_ok=True)
        (self.storage_path / "logs").mkdir(exist_ok=True)
    
    def save_output(self, content: str, filename: str, output_type: str = "text") -> str:
        """Save generated content to outputs directory"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{timestamp}_{filename}"
            
            output_path = self.storage_path / "outputs" / safe_filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Saved output: {safe_filename}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error saving output {filename}: {e}")
            return ""
    
    def save_json(self, data: Dict[str, Any], filename: str) -> str:
        """Save JSON data"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{timestamp}_{filename}.json"
            
            output_path = self.storage_path / "outputs" / safe_filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved JSON: {safe_filename}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error saving JSON {filename}: {e}")
            return ""
    
    def load_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Load cached data"""
        try:
            cache_path = self.storage_path / "cache" / f"{cache_key}.json"
            if cache_path.exists():
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading cache {cache_key}: {e}")
        return None
    
    def save_cache(self, cache_key: str, data: Dict[str, Any]) -> bool:
        """Save data to cache"""
        try:
            cache_path = self.storage_path / "cache" / f"{cache_key}.json"
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving cache {cache_key}: {e}")
            return False
    
    def list_outputs(self) -> List[str]:
        """List all saved outputs"""
        try:
            outputs_path = self.storage_path / "outputs"
            return [f.name for f in outputs_path.iterdir() if f.is_file()]
        except Exception as e:
            logger.error(f"Error listing outputs: {e}")
            return []
