from __future__ import annotations

import os
from pathlib import Path

from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

LAYER_TO_CONTAINER_ENV = {
    "raw": "AZURE_STORAGE_CONTAINER_RAW",
    "bronze": "AZURE_STORAGE_CONTAINER_BRONZE",
    "silver": "AZURE_STORAGE_CONTAINER_SILVER",
    "gold": "AZURE_STORAGE_CONTAINER_GOLD",
}


def upload_directory(blob_service: BlobServiceClient, local_dir: Path, container_name: str) -> int:
    container = blob_service.get_container_client(container_name)
    try:
        container.create_container()
    except Exception:
        # Container may already exist. In a production project, catch ResourceExistsError specifically.
        pass

    uploaded = 0
    for path in local_dir.rglob("*"):
        if path.is_file():
            blob_name = str(path.relative_to(local_dir)).replace("\\", "/")
            with path.open("rb") as file:
                container.upload_blob(name=blob_name, data=file, overwrite=True)
            uploaded += 1
    return uploaded


def main() -> None:
    load_dotenv()
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not connection_string:
        raise RuntimeError("AZURE_STORAGE_CONNECTION_STRING is not set. Copy .env.example to .env first.")

    blob_service = BlobServiceClient.from_connection_string(connection_string)

    total_uploaded = 0
    for layer, env_name in LAYER_TO_CONTAINER_ENV.items():
        container_name = os.getenv(env_name, layer)
        local_dir = DATA_DIR / layer
        if local_dir.exists():
            count = upload_directory(blob_service, local_dir, container_name)
            print(f"Uploaded {count} files from {local_dir} to container '{container_name}'.")
            total_uploaded += count

    print(f"Azure Blob upload complete. Total files uploaded: {total_uploaded}")


if __name__ == "__main__":
    main()
