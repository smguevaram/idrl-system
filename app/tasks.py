from flask import current_app
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, ImageClip
from moviepy.video.fx.resize import resize
import time
import os

from celery import Celery
from .celery_config import make_celery

celery = make_celery()

@celery.task(bind=True)
def process_video(self, filename):
    uploads_dir = os.getenv('UPLOAD_FOLDER', '/app/uploads')
    path_to_video = os.path.join(uploads_dir, filename)
    path_to_logo = os.path.join(uploads_dir, 'idrl_logo.png')
    milliseconds = int(round(time.time() * 1000))
    output_path = os.path.join(uploads_dir, f"{str(milliseconds)}_{filename}")

    try:
        clip = VideoFileClip(path_to_video)

        if clip.duration > 20:
            print(clip.duration)
            clip = clip.subclip(0, 20)

        clip_resized = resize(clip, width=clip.w, height=int(clip.w * 9 / 16))
        logo_clip = ImageClip(path_to_logo)
        logo_clip = logo_clip.set_duration(clip_resized.duration)
        logo_clip = logo_clip.resize(height=int(clip_resized.h * 0.1))
        logo_clip = logo_clip.margin(right=8, top=8, opacity=0)
        logo_clip = logo_clip.set_pos(("right", "top"))

        final_clip = CompositeVideoClip([clip_resized, logo_clip])

        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    except Exception as e:
        print(f"Error processing video {filename}: {str(e)}")
