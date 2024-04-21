from flask import Flask, render_template, url_for, request, redirect, send_file
import uuid

import os
import shutil

from moviepy.editor import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/edit", methods=["POST", "GET"])
def edit():
    if request.method == "POST":
        file = request.files["file"]

        if file:

            extension = str(file.filename).split(".")[1]
            
            if request.form["id"] == "0":
                user_id = uuid.uuid4()
                file_iter = 1

                os.mkdir(f"../Subclips/{user_id}/")
                file.save(f"../Subclips/{user_id}/file{file_iter}.{extension}")

                return render_template("home.html", id=user_id, iter=file_iter)
            else:
                user_id = str(request.form["id"])
                file_iter = int(request.form["file_iter"]) + 1
                print(user_id)
                print(file_iter)

                file.save(f"../Subclips/{user_id}/file{file_iter}.{extension}")
                return render_template("home.html", id=user_id, iter=file_iter)
    
@app.route("/done", methods=["POST"])
def combine():

    print("abc")
    user_id = str(request.form["id"])
    output_folder = f"../Subclips/{user_id}/"

    file_paths = [os.path.join(output_folder, filename) for filename in os.listdir(output_folder)] 

    print(file_paths)

    if "music" in file_paths[0]:
        video_clips = [VideoFileClip(path) for path in file_paths[1:]]

        video = concatenate_videoclips(video_clips, method="compose")

        music_clip = AudioFileClip(file_paths[0])
        music_clip = music_clip.set_duration(video.duration)

        final_clip = video.set_audio(music_clip)

        final_clip.write_videofile(output_folder+"video.mp4", fps=24)


    else:
        video_clips = [VideoFileClip(path) for path in file_paths]

        video = concatenate_videoclips(video_clips, method="compose")
        video.write_videofile(output_folder+"video.mp4", fps=24)

    
    return send_file(output_folder+"video.mp4", as_attachment=True, download_name="video.mp4")

@app.route("/music", methods=["POST"])
def music():
    user_id = str(request.form["id"])
    file_iter = int(request.form["file_iter"]) + 1

    output_folder = f"../Subclips/{user_id}/"

    file = request.files["file"]
    extension = str(file.filename).split(".")[-1]

    file.save(f"{output_folder}/music.{extension}")
    print("saved")
    return render_template("home.html", id=user_id, iter=file_iter)


if __name__ == "__main__":
    app.run()