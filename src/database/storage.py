import os
from pathlib import Path
from typing import Optional, List
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Use service role for backend
BUCKET_NAME = os.getenv("SUPABASE_STORAGE_BUCKET", "content-engine")

class StorageClient:
    def __init__(self):
        if not SUPABASE_URL or not SUPABASE_KEY:
            self.client = None
            return
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    async def upload_file(self, local_path: Path, remote_path: str) -> Optional[str]:
        """
        Uploads a local file to Supabase Storage and returns the public URL.
        """
        if not self.client:
            return None
            
        try:
            with open(local_path, 'rb') as f:
                self.client.storage.from_(BUCKET_NAME).upload(
                    path=remote_path,
                    file=f,
                    file_options={"upsert": "true"}
                )
            
            # Get public URL
            res = self.client.storage.from_(BUCKET_NAME).get_public_url(remote_path)
            return res
        except Exception as e:
            print(f"Storage Upload Error: {e}")
            return None

    async def download_file(self, remote_url: str, local_path: Path) -> bool:
        """
        Downloads a file from a public URL to a local path.
        """
        import httpx
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(remote_url)
                if response.status_code == 200:
                    with open(local_path, 'wb') as f:
                        f.write(response.content)
                    return True
        except Exception as e:
            print(f"Storage Download Error: {e}")
        return False

    async def delete_file(self, remote_path: str) -> bool:
        """
        Deletes a file from Supabase Storage.
        """
        if not self.client:
            return False
        try:
            self.client.storage.from_(BUCKET_NAME).remove([remote_path])
            return True
        except Exception as e:
            print(f"Storage Delete Error: {e}")
            return False
