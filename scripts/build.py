# -*- coding: utf-8 -*-
import os
import sys
import argparse
from pathlib import Path

def main(input_data_path,output_data_path):
    comp='bazel build -c opt --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/multi_hand_tracking:multi_hand_tracking_cpu'
    #명령어 컴파일
    cmd='GLOG_logtostderr=1 bazel-bin/mediapipe/examples/desktop/multi_hand_tracking/multi_hand_tracking_cpu --calculator_graph_config_file=mediapipe/graphs/hand_tracking/multi_hand_tracking_desktop_live_image.pbtxt'
    #미디어 파이프 명령어 저장listfile
    listfile=os.listdir(input_data_path)
    #os.system('echo yess')
    print(listfile)

    Path(output_data_path+"/Relative/").mkdir(parents=True, exist_ok=True)
    Path(output_data_path+"/Absolute/").mkdir(parents=True, exist_ok=True)

    #if not(os.path.isdir(output_data_path+"Relative/")):
    #    os.mkdir(output_data_path+"Relative/")
    #if not(os.path.isdir(output_data_path+"Absolute/")):
    #    os.mkdir(output_data_path+"Absolute/")

    for file in listfile:
    #    if not(os.path.isdir(input_data_path+file)): #ignore .DS_Store
    #        continue
        word = "/"+file+"/"
        fullfilename=os.listdir(input_data_path+word)

        Path(output_data_path+word).mkdir(parents=True, exist_ok=True)
        Path(output_data_path+"/Relative"+word).mkdir(parents=True, exist_ok=True)
        Path(output_data_path+"/Absolute"+word).mkdir(parents=True, exist_ok=True)

        # if not(os.path.isdir(output_data_path+word)):
        #     os.mkdir(output_data_path+word)
        # if not(os.path.isdir(output_data_path+"Relative/"+word)):
        #     os.mkdir(output_data_path+"Relative/"+word)
        # if not(os.path.isdir(output_data_path+"Absolute/"+word)):
        #     os.mkdir(output_data_path+"Absolute/"+word)

        os.system(comp)

        outputfilelist=os.listdir(output_data_path+word)
        for datalist in fullfilename:
            #if ".DS_Store" in mp4list:
            #    continue
            inputfilen='   --input_image_path='+input_data_path+word+datalist
            outputfilen='   --output_image_path='+output_data_path+word+datalist
            cmdret=cmd+inputfilen+outputfilen
            os.system(cmdret)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='operating Mediapipe')
    parser.add_argument("--input_data_path",help=" ")
    parser.add_argument("--output_data_path",help=" ")
    args=parser.parse_args()
    input_data_path=args.input_data_path
    output_data_path=args.output_data_path
    #print(input_data_path)
    main(input_data_path,output_data_path)
