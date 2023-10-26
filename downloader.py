from yt_dlp import YoutubeDL, utils
import random
from random import uniform
import os
import subprocess
test_url = "https://www.youtube.com/shorts/-gYtmdi8Ypo"
counter = 0
def filename_hook(d):
    # print(d)
    global counter
    
    if d["status"] == "finished":
        # print(d)
        counter +=1
        with open("join_video.txt", "a") as f:
            f.write(f"file videos/{counter}outfile.mp4\n") 
        os.rename(d["filename"], f"videos/{counter}outfile.mp4")

test = "https://www.youtube.com/watch?v=zroOC4jvY1o"
# print(help(YoutubeDL))


def getInds(duration : int = 1 , rem : int= 1 , consis : int = 0 ):
    
    ops = [list(range(0, duration))]
    out = []
    while rem > 0:
        # print(ops)
        ops.sort(key = lambda x: len(x),reverse=True)
        li = ops[0] #random.choice(ops)
        ops.remove(li)

        start = random.choice(li)
        end =  (  min(start + consis, max(li)) if consis != 0 else random.randint(start,min(start+10, max(li))) )
        out.append((start,end))
        # print(start,end)
        fhalf = li[:li.index(start)]
        if(fhalf != []):
            ops.append(fhalf) 
        lhalf = li[li.index(end):]
        if(lhalf != []):
            ops.append(lhalf)
        
        rem -= 1
    return out

def genInds(duration=1,rem:int = 1,consis: float = 0.0, sort: bool=True, randGap :float = 10.0):
    ops = [(0,duration)]
    out = []
    while rem > 0:
        # print(ops)
        ops.sort(key = lambda x: x[1]-x[0],reverse=True)
        li = ops[0] #random.choice(ops)
        ops.remove(li)

        start = round(uniform(li[0], li[1]),2)
        end =  (  round(min(start + consis, max(li)),2) if consis != 0 else round(uniform(start,min(start+randGap, max(li))),2) )
        if(start != end):
            out.append((start,end))
            # print(start,end)
            fhalf = (li[0], start)
            
            ops.append(fhalf) 
            lhalf = (end,li[1])
            ops.append(lhalf)
            
            rem -= 1
    if(sort):
        out.sort(key=lambda x:x[0])
    return out
# print([genInds(100,10,0.1) for _ in range(100)])


with YoutubeDL() as infograb:
    info = infograb.extract_info(test_url, download=False)
    print(info["duration"])
    print(random.sample(range(0,info["duration"]), 5))
    ydl_opts = {
        "paths": {"home": "videos"},
        "format": "mp4",
        "concurrent_fragments":6,
        "progress_hooks": [filename_hook],
        "default_search":"ytsearch",
        "download_ranges":utils.download_range_func(None, [ (start, end) for start,end in genInds(info["duration"], 100, .1,sort=False)]),  
        "force_keyframes_at_cuts": True, 
    }
    with open("join_video.txt", "w") as f:
        f.write("")
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(test_url)
        # print(info["duration"])
        ffmpeg_cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'join_video.txt', '-c', 'copy', 'output_demuxer.mp4']
        subprocess.run(ffmpeg_cmd)



# random.seed(0)
# print([getInds(100, 10, 10) for _ in range(10000)])
# print(extr.ytsearch("cats"))
# print(downloader.download("https://www.youtube.com/watch?v=zroOC4jvY1o"))