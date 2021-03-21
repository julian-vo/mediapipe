# -*- coding: utf-8 -*-
import os
import sys
import argparse
import csv
import re
#from StringIO import StringIO
from pathlib import Path


#python trimVideo.py --input_vid=/home/julian/Desktop/Work/Thesis/videoData/videoClips/test2/testInput.m4v --timestamp_csv=/home/julian/Desktop/Work/Thesis/videoData/1615594159297.csv --output_path=/home/julian/Desktop/Work/Thesis/videoData
def main(input_vid,timestamp_csv,output_path):

    # Get filename & extension
    input_filename_ext = re.search(r'(.*)\/(.*)',input_vid).group(2)
    input_filename = re.search(r'(.*)\.(.*)',input_filename_ext).group(1)
    input_ext = re.search(r'(.*)\.(.*)',input_filename_ext).group(2)

    # Open CSV timestamp file
    f = open(timestamp_csv)
    times = csv.reader(f)

    # Loop CSV timestamps
    for row in times:

        # Create output video path
        out_folder_vid = output_path+"/trainingVideos/"+row[2]
        Path(out_folder_vid).mkdir(parents=True, exist_ok=True)
        out_vid_name = input_filename + "_" + row[0] + "_" + row[1]
        out_vid_path = out_folder_vid + "/" + out_vid_name + "." + input_ext

        # Trim video using FFMPEG
        # ffmpeg -n -i '/home/julian/Desktop/Work/Thesis/videoData/videoClips/test2/testInput.m4v' -ss '0.76670' -to '1.700' '/home/julian/Desktop/Work/Thesis/videoData/videoClips/test2/testOutput.m4v'
        trim_cmd = "ffmpeg -n -i '" + input_vid + "' -ss '" + row[0] + "' -to '" + row[1] + "' '" + out_vid_path + "'"
        os.system(trim_cmd)
        
        
	# Create output video path
        out_folder_img = output_path+"/trainingImages/"+row[2]
        Path(out_folder_img).mkdir(parents=True, exist_ok=True)
        out_img_path = out_folder_img + "/" + out_vid_name + "_%03d.jpg"
        
        # Extract frames
        # ffmpeg -i 'video.m4v' -s 1080x1920 'video_%03d.jpg' 
        frame_cmd = "ffmpeg -i '" + out_vid_path + "' -s 1080x1920 '" + out_img_path + "'"
        os.system(frame_cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Trimming videos')
    parser.add_argument("--input_vid",help=" ")
    parser.add_argument("--timestamp_csv",help=" ")
    parser.add_argument("--output_path",help=" ")
    args=parser.parse_args()
    input_vid=args.input_vid
    timestamp_csv=args.timestamp_csv
    output_path=args.output_path
    main(input_vid,timestamp_csv,output_path)
