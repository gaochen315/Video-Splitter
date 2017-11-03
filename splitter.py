# --------------------------------------------------------
# Video Splitter
# Written by Chen Gao
# chengao@umich.edu
# --------------------------------------------------------

"""Split a video into several chunks"""

import subprocess
import os
import math
import glob

# Determine the chunk length
chunk_length = 300 # 300s --- 5mins





length_regexp = 'Duration: (\d{2}):(\d{2}):(\d{2})\.\d+,'
re_length     = re.compile(length_regexp)


# Get current folder name. All generated file will be saved in the under the parent folder.
dir_path    = os.path.dirname(os.path.realpath(__file__))
folder_name = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]


# Loop all the avi files in the folder
for file in glob.glob("*.avi"):

    # Get the video filename
    filename        = file
    file_prefix     = filename.split(".")[0]
    file_extension  = filename.split(".")[-1]
    output_dir      = os.path.abspath(os.path.join( os.path.dirname(os.path.realpath(__file__)), os.pardir)) + '/' + folder_name + '_split/' + file_prefix + '/'    
    #ipdb.set_trace()
    os.makedirs(output_dir)

    # Get the duration of the video
    output = subprocess.Popen("ffmpeg -i '"+filename+"' 2>&1 | grep 'Duration'",
                              shell = True,
                              stdout = subprocess.PIPE
                              ).stdout.read()

    matches      = re_length.search(output)
    video_length = int(matches.group(1)) * 3600 + int(matches.group(2)) * 60 + int(matches.group(3))
    print "Video name:" + filename, "Video length in seconds: " + str(video_length)                        


    # Calculate the number of chunks
    chunk_count = int(math.ceil(video_length / float(chunk_length)))


    for n in range(0, chunk_count):

        #if n == 0: 
        #    chunk_start = 0
        #else:
        #    chunk_start = chunk_length * n
        chunk_start = chunk_length * n
        
        # output filename
        output_name = output_dir + file_prefix + '_' + str(n).zfill(3) + '.' + file_extension



        split_cmd = ['ffmpeg' , '-i', filename, '-ss' , str(chunk_start), '-t' , str(chunk_length), '-vcodec', 'copy', '-acodec',  'copy', output_name]
        subprocess.call(split_cmd)




