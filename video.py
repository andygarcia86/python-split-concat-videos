import ffmpeg  #https://pypi.org/project/ffmpeg-python/
import subprocess
import random
import numpy as np, numpy.random
import datetime

ffmpeg_path = "C:/Program Files/ffmpeg/bin/ffmpeg"

def get_video_length(filename):
    cmd = ["C:/Program Files/ffmpeg/bin/ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

def cut_video(source_filename, out_filename, start_time, end_time):
	subprocess.call([ffmpeg_path,
                 '-i',source_filename,
                 '-ss',start_time,
                 '-to',end_time,
                 out_filename])

def split_video_random(filename):
	duration_total = get_video_length(filename)
	randPartitions = random.randint(3, 5)
	rand = np.random.dirichlet(np.ones(randPartitions), size=1)
	start_seconds = 0
	end_seconds = 0
	idx = 0

	for (x,y), value in numpy.ndenumerate(rand):
		seconds = rand[x][y] * duration_total
		idx = idx + 1

		if (x != 0 | y != 0):
			start_seconds = end_seconds
		end_seconds = end_seconds + seconds

		start = str(start_seconds - start_seconds % 0.001)
		end = str(end_seconds - end_seconds % 0.001)

		cut_video(filename, 'out-' + str(idx) + '.mp4', start, end)

def concatenate():
	subprocess.call([ffmpeg_path,
					'-f', 'concat',
					'-i', 'inputs.txt'
					'-vcodec', 'copy'
					'-acodec', 'copy',
					'mux1.mp4'])

	"""
	cmd="( "

	h264options="-vcodec libx264 -b 512k -flags +loop+mv4 -cmp 256 \
	-partitions +parti4x4+parti8x8+partp4x4+partp8x8+partb8x8 \
	-me_method hex -subq 7 -trellis 1 -refs 5 -bf 3 \
	-flags2 +bpyramid+wpred+mixed_refs+dct8x8 -coder 1 -me_range 16 \
	-g 250 -keyint_min 25 -sc_threshold 40 -i_qfactor 0.71 -qmin 10\
	-qmax 51 -qdiff 4"

	outfile="out-`date +%F-%H%M.%S`.mp4"

	cmd="${cmd}${ffmpeg_path} -i out-1.mp4 -ab 256000 -vb 10000000 -mbd rd -trellis 2 -cmp 2 -subcmp 2 -g 100 -f mpeg -; "

	cmd="${cmd} ) | ${ffmpeg_path} -y -i - -threads 8 ${h264options} -vb 10000000 -acodec libfaac -ar 44100 -ab 128k -s 1280x720 ${outfile}"
	subprocess.call([ffmpeg_path,
                 '-i','concat:out-1.mp4|out-2.mp4|out-3.mp4',
                 '-c','copy',
                 'output.mp4'])
	"""

concatenate()

#split_video_random('video.mp4')
