import os
import shutil
import subprocess
import tempfile

from fastapi import UploadFile

from .logger import setup_logger

logger = setup_logger(__name__)

# Validate file type and return extension if true
def validate_file_type(file: UploadFile, target_file: str):
    return file.content_type.split("/")[0] == target_file

def get_audio_file_extension(file: UploadFile):
    return file.content_type.split("/")[1]

# Add binary files
def save_to_FS(type: str, file_name: str, extension: str, file_content: bytes):
    generated_name = f"./static/{type}/{file_name}.{extension}"
    # generated_name = f"/var/static/{type}/{file_name}.{extension}"
    with open(generated_name, "wb") as file:
        file.write(file_content)
    logger.info(f"Save  {file_name} with the path: {generated_name} ")
    file.close()


def convert_file(file_content: bytes):
    temp_dir = tempfile.mkdtemp()
    try:
        temp_file_path = os.path.join(temp_dir, "init.mp4")
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file_content)
        output_file_path = os.path.join(temp_dir, "converted.mp4")
        ffmpeg_cmd = [
            "ffmpeg",
            "-i",
            temp_file_path,
            "-vcodec",
            "libx264",
            output_file_path,
        ]
        subprocess.run(ffmpeg_cmd, check=True)
        with open(output_file_path, "rb") as output_file:
            converted_content = output_file.read()
        shutil.rmtree(temp_dir)
        return {
            "message": "File converted successfully",
            "status": True,
            "file_data": converted_content,
        }

    except Exception as e:
        shutil.rmtree(temp_dir)
        return {"message": "Error converting file: " + str(e), "status": False}
