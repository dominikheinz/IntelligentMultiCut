import sys, os
path = os.getcwd()
path = path.replace("\\", "/")
os.environ['PATH'] = path + "/lib/ffmpeg_x64/bin"
sys.path.append('../')

from src.classes.core.App import App

if __name__ == "__main__":
  a = App()

  while(a.restart):
    a = 0
    a = App()
