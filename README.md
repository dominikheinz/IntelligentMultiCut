
# Intelligent MultiCut
Automated video cutting based on neural networks for human pose and face analysis.

## Overview
*Intelligent MultiCut* is a PoC for automated video cutting based on human pose detection and analysis. This project uses the [OpenPose library](https://github.com/CMU-Perceptual-Computing-Lab/openpose) for pose and face detection. *Intelligent MultiCut* chooses the best camera position based on best pose and face estimation. It utilizes different algorithms to evaluate pose and face orientation as well as the distance to the camera to choose the best scenes. 
More detailed information can be found in **[Algorithms](#algorithms)**.
This project was developed in three months for a university assignment. 

## Algorithms
*Intelligent MultiCut* offers 4 different algorithms for different scenarios. Each algorithm is controlled via `AlgorithmController.py`. 

1.  AlgorithmController
2.  Algorithms
    -   Singleperson
    -   Multiperson Closeup
    -   Multiperson Peoplecount
    -   Distance Detection
3.  Error correction

### 1. AlgorithmController
The `AlgorithmController` is used to control each algorithm. To initialize a new `AlgorithmController` object a `MetaDataController` object must be provided. The class offers two functions  `run_algorithm(self, algo_id)` and `filter_cut_frames(self, switch_frames)`. 
The `filter_cut_frames(self, switch_frames)` method is used to extract relevant frames from the video.  The `run_algorithm(self, algo_id)` method uses an algorithm on the in the constructor provided metadata.  Valid values for the  `algo_id` parameter are `0`, `1`, `2` or `3`.

#### 2.1 Singleperson algorithm
The singleperson algorithm calculates an average score based on the precision of each detect pose joint. Therefore the camera view which detects more body joints get a higher score and are more likely to be selected. Calling `def run_pose_algorithm(self, show_graph):` applies the algorithm on the frames provided in the constructor. It returns an array which contains metadata on how video clips need to be cut. The `show_graph` parameter shows a graph after successful processing. This is an example of a person walking up and down in a hallway between two cameras.

![alt-text-2](https://i.imgur.com/alesAzE.jpg)

When the person is facing the camera a higher score is given compared to the camera only seeing the persons back. When the person turns around the graphs switch to the opposite.

#### 2.2 Multiperson Closeup algorithm

The Multiperson Closeup algorithm is a combination of the distance detection and multi peerson detection. The algorithm evaluates from a group of people in a frame the one closest to the camera. The camera which has most people standing close gets the highest score and will be selected.

#### 2.3 Multiperson Peoplecount algorithm

The Multiperson Peoplecount algorithm checks which frame has the most people. The camera perspective with most recognized people is selected.

## Installation

To install *Intelligent MultiCut* on windows..... todo

## Dependencies & Requirements
- [OpenPose library](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
- [OpenCV](https://github.com/opencv/opencv)
- [FFMPEG](https://ffmpeg.zeranoe.com/builds/)
- NVIDIA GPU (min. 1,6 GB RAM) + CUDA 8 + cuDNN 5.1

## Licewith CUDAnse
