import urllib.request
import os, zipfile
import sys
import shutil
import pip

def install(package):
    print("Install: "+ package)
    pip.main(['install', package])

def download(url,local):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, local)

def unzip(path,out_name):
    archive = zipfile.ZipFile(path)

    archive.extractall(out_name)

def is_venv():
    return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

if is_venv():
    print('virtualenv detected')

install("numpy")

install("moviepy")

install("checksumdir")

install ("psutil")

install ("pydub")

install ("matplotlib")

install("data/opencv_python-3.3.1-cp36-cp36m-win_amd64.whl")

import checksumdir

#Download ffmpeg
if(os.path.isdir('../src/lib/ffmpeg_x64/') and checksumdir.dirhash('../src/lib/ffmpeg_x64')=='c6f76a82e889404a156b7ac93e367524'):
    print("ffmpeg_x64 already existing")
else:

    if(os.path.isdir('../src/lib/ffmpeg_x64/')):
        print('removing corrupt ffmpeg installation')
        shutil.rmtree('../src/lib/ffmpeg_x64/')
        print('reinstalling ffmpeg')

    print("Unzipping directory...")
    unzip("data/ffmpeg_x64.zip","data/ffmpeg_x64")
    print("Unzipping finished")
    print("Copying extracted files")
    shutil.copytree('data/ffmpeg_x64/ffmpeg-20171203-5a93a85-win64-static','../src/lib/ffmpeg_x64')
    shutil.rmtree('data/ffmpeg_x64')

    print("ffmpeg installed ")

#Download OpenPose_demo
if(os.path.isdir('../src/lib/openpose') and checksumdir.dirhash('../src/lib/openpose')=='3690da7d6607743bbdf0121b96d3aa0b'):
    print("OpenPose_demo_1.0.1 already existing")
else:
    if(os.path.isdir('../src/lib/openpose')):
        print('removing corrupt OpenPose installation')
        shutil.rmtree('../src/lib/openpose')
        print('reinstalling OpenPose')
    print("Downloading OpenPose_demo... This may take several minutes")
    download('http://posefs1.perception.cs.cmu.edu/OpenPose/OpenPose_demo_1.0.1.zip','OpenPose_demo.zip')
    print("Download finished")
    print("Unzipping directory...")
    unzip('OpenPose_demo.zip','OpenPose_demo')
    print("Unzipping finished")
    print("Copying extracted files")
    shutil.copytree('OpenPose_demo/OpenPose_demo_1.0.1','../src/lib/openpose')
    shutil.rmtree('OpenPose_demo')
    os.remove('OpenPose_demo.zip')
    print("Done!")



