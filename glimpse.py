from yt_dlp import YoutubeDL, utils
import random
from random import uniform
import os
import subprocess


class glimpser():
    def __init__(self):
        self.counter = 0
    def genInds(self, duration=1,rem:int = 1,consis: float = 0.0, sort: bool=True, randGap :float = 10.0):
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

    def filename_hook(self,d):
            # print(d)
            if d["status"] == "finished":
                # print(d)
                self.counter +=1
                with open("join_video.txt", "a") as f:
                    f.write(f"file videos/{self.counter}outfile.mp4\n") 
                os.rename(d["filename"], f"videos/{self.counter}outfile.mp4")
    def genVideo(self,url: str,clips : int, time : float = 0.0, sort :bool = False, random_gap :float =10.0):
        
        
        self.counter = 0
        with YoutubeDL() as infograb:
            info = infograb.extract_info(url, download=False)
            print(info["duration"])
            print(random.sample(range(0,info["duration"]), 5))
            ydl_opts = {
                "paths": {"home": "videos"},
                "format": "mp4",
                "concurrent_fragments":6,
                "progress_hooks": [self.filename_hook],
                "default_search":"ytsearch",
                "download_ranges":utils.download_range_func(None, [ (start, end) for start,end in self.genInds(info["duration"], clips,time,sort=sort,randGap=random_gap)]),  
                "force_keyframes_at_cuts": True, 
            }
            with open("join_video.txt", "w") as f:
                f.write("")
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download(url)
                # print(info["duration"])
                ffmpeg_cmd = ['ffmpeg', '-y','-f', 'concat', '-safe', '0', '-i', 'join_video.txt', '-c', 'copy', 'output_demuxer.mp4']
                subprocess.run(ffmpeg_cmd)


if __name__ == "__main__":
    g = glimpser()

    g.genVideo("https://youtube.com/shorts/AxqNfb4DJzs?si=MuMoS2BiYBAvdKPr",100, 0.05)
# random.seed(0)
# print([getInds(100, 10, 10) for _ in range(10000)])
# print(extr.ytsearch("cats"))
# print(downloader.download("https://www.youtube.com/watch?v=zroOC4jvY1o"))