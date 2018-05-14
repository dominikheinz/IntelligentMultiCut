
# Intelligent MultiCut
Automated video cutting based on neural networks for human pose and face analysis.

## Overview

![alt-text-2](https://i.imgur.com/m4bFb0z.png)

*Intelligent MultiCut* is a PoC for automated video cutting based on human pose detection and analysis. This project uses the [OpenPose library](https://github.com/CMU-Perceptual-Computing-Lab/openpose) for pose and face detection. *Intelligent MultiCut* chooses the best camera position based on best pose and face estimation. It utilizes different algorithms to evaluate pose and face orientation as well as the distance to the camera to choose the best scenes. 
More detailed information can be found in **[Algorithms](#algorithms)**.
This project was developed in three months for a university assignment. 

## Architecture

### Model
Every class that acts as model such as `User`, `MetaDta` etc can be found under `src/classes/models/` and can be used from a controller class.

### Controller
All controller classes are stored at `src/classes/controllers/`. Controller classes inherit from the base class and can access the core attributres (such as Config) of the parent.

### View
All classes related to the graphical user interface are stored here. Data is passed from the `View` to the `Controller` for further proceessing and returned to the GUI upon completion. 

## Algorithms
*Intelligent MultiCut* offers 4 different algorithms for different scenarios. Each algorithm is controlled via `AlgorithmController.py`. 

1.  AlgorithmController
2.  Algorithms
    -   Singleperson
    -   Multiperson Closeup
    -   Multiperson Peoplecount
    -   Distance Detection
3.  Error correction

### 1 AlgorithmController
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

#### 2.4 Multiperson Peoplecount algorithm

By measuring the distance from the detected person to the camera the distance detection algorithm evaluates the best scene. (The closer the better)

<img src="/doc/markdown/Distance1.gif?raw=true"> ![alt-text-2](https://i.imgur.com/aDejcoV.jpg)

By calculating the eye distance and the eye-nose distance the algorithm calculates a score. When a person comes closer to the camera the score increases. The method`def run_distance_algorithm(self, show_graph):` applies the algorithm on the frames provided in the constructor. The `show_graph` parameter shows a graph after successful processing.
After successful processing `def run_distance_algorithm(self, show_graph):` returns an array with information which video clip should be cut at which timestamp.

#### 3 Error correction

In some cases the OpenPose framework fails to properly detect people during the video analysis. These measurement errors falsify the reults of the algorithms. To counter this issue a smoothing algorithm got implemented. By using <b>median filtering</b> the measured data is corrected. The smoothing factor `s` defines how many values to the left and right should be used to calculate a correected value. The values get sorted in ascending order and the middle value is used. E.g. Let's assume we have a smoothing factor of <code>3</code>. That means `3` values to the left and right are included. That gives us `7` values, for example `[4,8,6,7,9,6,4]`. These values are sorted and the middle value is picked. `[4,4,6,6,7,8,9]` -> `6`. This makes it possible to ignore score spikes caused my missdetection.
For comparison a raw graph and a smooth graph on the example of the distance detection algorithm:

![alt-text-2](https://i.imgur.com/mniifra.jpg)

(Before error correection)

![alt-text-2](https://i.imgur.com/NC5ECoW.jpg)

(After error correction)

## Installation

1. Download the [OpenPose Demo](http://posefs1.perception.cs.cmu.edu/OpenPose/OpenPose_demo_1.0.1.zip). 
2. Download and install [Python 3.6.3](https://www.python.org/downloads/).
3. Run the install script in `%YOUR_LOCATION%/multicut/installer/setup_win_64.bat`. It will download all the missing python dependencies, ffmpeg etc.
4. Start the program using the `Intelligent_Multicut.bat` in the root directory.

## Dependencies & Requirements
- [OpenPose library](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
- [OpenCV](https://github.com/opencv/opencv)
- [FFMPEG](https://ffmpeg.zeranoe.com/builds/)
- NVIDIA GPU (min. 1,6 GB RAM) + CUDA 8 + cuDNN 5.1
- Python Packages: moviepy,numpy,OpenCV(3.3.1),psutil,pydub,matplotlib

## License

ToDo Add License
