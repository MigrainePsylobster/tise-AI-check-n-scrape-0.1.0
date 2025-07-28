import os
import json
import hashlib
import requests
import logging
from typing import List, Dict, Optional
from urllib.parse import urlparse
from PIL import Image
from pathlib import Path

from config import DOWNLOADS_FOLDER
from database import DatabaseManager

class FileDownloader:
    """Handles downloading and saving files from scraped posts."""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.downloads_folder = Path(DOWNLOADS_FOLDER)
        self.downloads_folder.mkdir(parents=True, exist_ok=True)
        
    def download_post_content(self, post_data: Dict) -> List[str]:
        """Download all content for a post and return file paths."""
        downloaded_files = []
        
        try:
            # Create folder for this post
            post_folder = self._create_post_folder(post_data)
            
            # Download images
            image_urls = json.loads(post_data.get('image_urls', '[]'))
            for i, img_url in enumerate(image_urls):
                file_path = self._download_image(img_url, post_folder, f"image_{i+1}")
                if file_path:
                    downloaded_files.append(str(file_path))
            
            # Save post metadata
            metadata_file = self._save_post_metadata(post_data, post_folder)
            if metadata_file:
                downloaded_files.append(str(metadata_file))
            
            # Mark as downloaded in database
            if downloaded_files:
                self.db.mark_post_downloaded(post_data['post_url'], downloaded_files)
                logging.info(f"Downloaded {len(downloaded_files)} files for post: {post_data['title']}")
            
            return downloaded_files
            
        except Exception as e:
            logging.error(f"Error downloading post content: {e}")
            return []
    
    def _create_post_folder(self, post_data: Dict) -> Path:
        """Create username-organized folder structure."""
        # Extract username from profile URL
        profile_name = self._get_profile_name(post_data['profile_url'])
        
        # Create username-based folder structure
        user_folder = self.downloads_folder / profile_name
        images_folder = user_folder / 'images'
        metadata_folder = user_folder / 'metadata'
        
        # Create all necessary folders
        images_folder.mkdir(parents=True, exist_ok=True)
        metadata_folder.mkdir(parents=True, exist_ok=True)
        
        return user_folder
    
    def _get_profile_name(self, profile_url: str) -> str:
        """Extract profile name from URL."""
        try:
            # Extract username from URL
            parts = profile_url.rstrip('/').split('/')
            return self._sanitize_filename(parts[-1] if parts else 'unknown_profile')
        except:
            return 'unknown_profile'
    
    def _sanitize_filename(self, filename: str) -> str:
        """Remove invalid characters from filename."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename[:50]  # Limit length
    
    def _download_image(self, img_url: str, folder: Path, base_name: str) -> Optional[Path]:
        """Download a single image with unique naming to prevent overwrites."""
        try:
            response = requests.get(img_url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Extract unique ID from Tise URL pattern
            # Example: https://tise-static.telenorcdn.net/.../4c2bc7f2-1bce-490e-95b2-ef040a840e6b/perfect-jeans
            unique_id = self._extract_unique_id_from_url(img_url)
            
            # Determine file extension
            content_type = response.headers.get('content-type', '')
            if 'jpeg' in content_type or 'jpg' in content_type:
                ext = '.jpg'
            elif 'png' in content_type:
                ext = '.png'
            elif 'gif' in content_type:
                ext = '.gif'
            elif 'webp' in content_type:
                ext = '.jpg'  # Convert webp to jpg automatically
            else:
                # Try to get extension from URL
                parsed_url = urlparse(img_url)
                path_ext = Path(parsed_url.path).suffix
                if path_ext == '.webp':
                    ext = '.jpg'  # Convert webp to jpg automatically
                else:
                    ext = path_ext if path_ext in ['.jpg', '.jpeg', '.png', '.gif'] else '.jpg'
            
            # Create unique filename: perfect-jeans_4c2bc7f2.jpg
            unique_filename = f"{base_name}_{unique_id}{ext}"
            file_path = folder / 'images' / unique_filename
            
            # Download and save
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Convert webp to jpg if needed, then verify and optimize
            self._convert_and_optimize_image(file_path, ext)
            
            logging.debug(f"Downloaded image: {file_path}")
            return file_path
            
        except Exception as e:
            logging.error(f"Error downloading image {img_url}: {e}")
            return None
    
    def _convert_and_optimize_image(self, file_path: Path, target_ext: str):
        """Convert webp to jpg if needed, then verify and optimize image."""
        try:
            with Image.open(file_path) as img:
                # Convert webp to jpg if the target extension is jpg but original might be webp
                if target_ext == '.jpg' and (img.format == 'WEBP' or file_path.suffix.lower() == '.webp'):
                    # Convert WEBP to RGB (removes transparency) then save as JPG
                    if img.mode in ('RGBA', 'LA', 'P'):
                        # Convert to RGB, using white background for transparency
                        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                        img = rgb_img
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Save as JPG with good quality
                    img.save(file_path, 'JPEG', optimize=True, quality=90)
                    logging.debug(f"Converted WEBP to JPG: {file_path}")
                else:
                    # Verify image can be opened
                    img.verify()
                    img = Image.open(file_path)  # Reopen after verify
                
                # Optionally resize very large images
                if img.width > 2000 or img.height > 2000:
                    img.thumbnail((2000, 2000), Image.Resampling.LANCZOS)
                    if target_ext == '.jpg':
                        img.save(file_path, 'JPEG', optimize=True, quality=85)
                    else:
                        img.save(file_path, optimize=True, quality=85)
                    logging.debug(f"Optimized large image: {file_path}")
                    
        except Exception as e:
            logging.warning(f"Image processing failed for {file_path}: {e}")
            # Remove invalid image file
            if file_path.exists():
                file_path.unlink()
    
    def _verify_and_optimize_image(self, file_path: Path):
        """Verify image is valid and optionally optimize it."""
        try:
            with Image.open(file_path) as img:
                # Verify image can be opened
                img.verify()
                
                # Optionally resize very large images
                img = Image.open(file_path)  # Reopen after verify
                if img.width > 2000 or img.height > 2000:
                    img.thumbnail((2000, 2000), Image.Resampling.LANCZOS)
                    img.save(file_path, optimize=True, quality=85)
                    logging.debug(f"Optimized large image: {file_path}")
                    
        except Exception as e:
            logging.warning(f"Image verification failed for {file_path}: {e}")
            # Remove invalid image file
            if file_path.exists():
                file_path.unlink()
    
    def _save_post_metadata(self, post_data: Dict, folder: Path) -> Optional[Path]:
        """Save post metadata as JSON file."""
        try:
            metadata_file = folder / "metadata.json"
            
            # Prepare metadata
            metadata = {
                'post_url': post_data['post_url'],
                'profile_url': post_data['profile_url'],
                'title': post_data.get('title', ''),
                'description': post_data.get('description', ''),
                'price': post_data.get('price', ''),
                'scraped_date': post_data.get('scraped_date', ''),
                'image_count': len(json.loads(post_data.get('image_urls', '[]'))),
            }
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            return metadata_file
            
        except Exception as e:
            logging.error(f"Error saving post metadata: {e}")
            return None
    
    def get_download_statistics(self) -> Dict:
        """Get download statistics."""
        try:
            total_size = 0
            file_count = 0
            
            for root, dirs, files in os.walk(self.downloads_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
                        file_count += 1
            
            # Convert bytes to MB
            total_size_mb = total_size / (1024 * 1024)
            
            return {
                'total_files': file_count,
                'total_size_mb': round(total_size_mb, 2),
                'downloads_folder': str(self.downloads_folder)
            }
            
        except Exception as e:
            logging.error(f"Error getting download statistics: {e}")
            return {}
    
    def cleanup_old_downloads(self, days_to_keep: int = 30):
        """Clean up downloads older than specified days."""
        try:
            import time
            from datetime import datetime, timedelta
            
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            cutoff_timestamp = cutoff_date.timestamp()
            
            removed_count = 0
            for root, dirs, files in os.walk(self.downloads_folder):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    if os.path.getmtime(dir_path) < cutoff_timestamp:
                        import shutil
                        shutil.rmtree(dir_path)
                        removed_count += 1
                        logging.info(f"Removed old download folder: {dir_path}")
            
            logging.info(f"Cleanup completed. Removed {removed_count} old folders.")
            
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")

    def _extract_unique_id_from_url(self, img_url: str) -> str:
        """Extract unique ID from Tise image URL for filename uniqueness."""
        try:
            # Tise URL pattern: https://tise-static.telenorcdn.net/.../4c2bc7f2-1bce-490e-95b2-ef040a840e6b/perfect-jeans
            url_parts = img_url.split('/')
            if len(url_parts) >= 2:
                # Get the UUID part (second to last segment)
                uuid_part = url_parts[-2]
                # Return first 8 characters of UUID for shorter filenames
                return uuid_part[:8] if len(uuid_part) >= 8 else uuid_part
        except Exception as e:
            logging.debug(f"Could not extract unique ID from URL {img_url}: {e}")
        
        # Fallback: use hash of full URL
        return hashlib.md5(img_url.encode()).hexdigest()[:8]
