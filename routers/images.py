import os
from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi.responses import FileResponse

AUDIOS_FOLDER = os.path.join("static", "images")

router = APIRouter(prefix='/images', tags=["images"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.get('/{audio_filename}', status_code=status.HTTP_200_OK)
async def get_audio(audio_filename: str, background_tasks: BackgroundTasks):
    audio_fullpath = os.path.join(AUDIOS_FOLDER, audio_filename)
    if os.path.exists(audio_fullpath):
        #background_tasks.add_task(delete_file, audio_fullpath)
        return FileResponse(audio_fullpath, media_type="image/png")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

def delete_file(filename: str):
    if os.path.isfile(filename):
        os.remove(filename)