import csv
import pandas as pd
from bs4 import BeautifulSoup
import json
from moviepy.editor import VideoFileClip


def read_csv_file(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data


def write_csv_file(filename, data):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


#
# input_file = 'C:\\Users\\acer\\Desktop\\New folder (2)\\first.csv'
# output_file = 'C:\\Users\\acer\\Desktop\\New folder (2)\\output.csv'


# csv_data = read_csv_file(input_file)
# write_csv_file(output_file, csv_data)


# ----------------------------------------Read and Write Excel File-----------------------------------


def read_excel_file(filename, sheet_name):
    return pd.read_excel(filename, sheet_name=sheet_name)


def write_excel_file(data, filename, sheet_name):
    df = pd.DataFrame(data)
    df.to_excel(filename, sheet_name=sheet_name, index=False)


# Example usage
# input_file = 'C:\\Users\\acer\\Desktop\\New folder (2)\\firstexcel.xlsx'
# output_file = 'C:\\Users\\acer\\Desktop\\New folder (2)\\output1excel.xlsx'
# sheet = 'Sheet1'
#
# excel_data = read_excel_file(input_file, sheet)
# write_excel_file(excel_data, output_file, sheet)


# =================================Read And Write Text File=====================================


def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        file_contents = file.read()
        return file_contents


def write_txt_file(file_path, contents):
    with open(file_path, 'w') as file:
        file.write(contents)


# txt_file_path = 'C:\\Users\\acer\\Desktop\\New folder (2)\\first.txt'
# output_path = 'C:\\Users\\acer\\Desktop\\New folder (2)\\firsttxt8.txt'
#
# read_txt_file = read_txt_file(txt_file_path)
# write_txt_file(output_path, read_txt_file)


# ===================================Read and Write Html File ==============================

def read_html_file(file_path):
    with open(file_path, 'r') as file:
        contents = file.read()
    soup = BeautifulSoup(contents, 'html.parser')
    return soup


def write_html_file(soup, file_path):
    with open(file_path, 'w') as file:
        file.write(str(soup))


# input_file = 'C:\\Users\\acer\\Desktop\\New folder (2)\\html.html'
# output_file = 'C:\\Users\\acer\\Desktop\\New folder (2)\\html4.html'

# read_html_file = read_html_file(input_file)
# write_html_file(read_html_file, output_file):


# =====================Json File Read And Write ===============================
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


# input_file_path = 'C:\\Users\\acer\\Desktop\\New folder (2)\\first.json'
# output_file_path = 'C:\\Users\\acer\\Desktop\\New folder (2)\\first3.json'
#
# input_data = read_json(input_file_path)
# write_json(output_file_path, input_data)


# ========================Read Mov File and Write mp4========================


def read_mov(file_path):
    video_clip = VideoFileClip(file_path)
    return video_clip


def write_mp4(file_path, video_clip):
    video_clip.write_videofile(file_path, codec='libx264', audio_codec="aac")


# input_file_path = 'C:\\Users\\acer\\Desktop\\New folder (2)\\movfile.mov'
# output_file_path = 'C:\\Users\\acer\\Desktop\\New folder (2)\\movfile1.mp4'
#
# input_video_clip = read_mov(input_file_path)
# write_mp4(output_file_path, input_video_clip)
