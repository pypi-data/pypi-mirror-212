import subprocess


def marg_multiple_video(input_file, output_file):
    ffmpeg_command = ["ffmpeg", "-f", "concat", "-i", input_file, "-c", "copy", output_file]
    subprocess.run(ffmpeg_command)


# Example usage:
# input_file = "C:/New folder/new.txt"
# output_file = "C:/Users/acer/Desktop/New folder/output5.mp4"

