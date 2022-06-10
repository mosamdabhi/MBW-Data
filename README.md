[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6626508.svg)](https://doi.org/10.5281/zenodo.6626508)

# MBW: Multiview Bootstrapping in the wild
<!-- ![Alt Text](overview.gif | width=100) -->
<!-- <img src=overview.gif width="750"> -->
<p align="center">
  <img width="750" src=graphics/overview.gif>
</p>

Labeling articulated objects in unconstrained settings have a wide variety of applications including entertainment, neuroscience, psychology, ethology, and many fields of medicine. Large offline labeled datasets do not exist for all but the most common articulated object categories (e.g., humans). With just a few annotations (representing 1-2% of the frames), we are able to produce 2D results comparable to state-of-the-art fully supervised methods, and obtain 3D reconstructions that are impossible with other existing approaches. Our Multi-view Bootstrapping in the Wild (MBW) approach demonstrates results on standard human datasets, as well as tigers, cheetahs, fish, colobus monkeys, chimpanzees, and flamingos from videos captured casually in a zoo. 

We release this challenging dataset consisting image frames of tail-end distribution categories (such as Fish, Colobus Monkeys, Chimpanzees, etc.) with their corresponding 2D, 3D, and Bounding-Box labels generated from minimal human intervention.



# Basic setup

1. Clone the repository and pull data using lfs. 
    ```
    git clone git@github.com:mosamdabhi/MBW-Data.git
    cd MBW-Data
    ```
2. Download the data zip file from Zenodo: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6626508.svg)](https://doi.org/10.5281/zenodo.6626508)
3. Uncompress the data zip file `MBW-Data.zip` and place it in the current working directory.
4. Create a conda environment to run the visualization scripts.
    ```
    conda env create -f environment.yml && conda activate mbw
    ```

# Dataset capture
We capture 2-View videos from handheld smartphone cameras. In our case, we used an iPhone 11 Pro Max and an iPhone 12 Pro Max to capture the video sequences. We use Final Cut Pro to manually synchronize the 2-View video sequences using the audio signal and time stamps. 

## Overall object cateogories
In total, the instances in this dataset arise from 7 different object categories, coming from 2 camera views:
<p align="center">
  <img width="750" src=graphics/all_instances.jpg>
</p>



## Sequential data example
Example 2-View sequences from the capture of Fish, Chimpanzee, Colobus Monkey, and Tiger categories are shown below:
<p align="center">
  <img width="750" src=graphics/data_capture_1.gif>
</p>

# Dataset preprocessing
Please note that all we require are 2-view synchronized image frames and manual annotations for 1-2% of the data. No camera calibration (intrinsics or extrinsics) is required to run MBW. 


# Dataset format
The dataset is divided into two directories: `annot` and `images`. As names suggest, the `annot` directory contains annotations and `images` directory consists of N-view synchronized image frames. Here, N=2, i.e. this dataset consists of 2-View video sequences. 


# Annotation
We manually annotate 1-2% of the image frames per view. Our annotation consists of the 2D landmark keypoints. 

## Joint connection visualization

- We specify the number of keypoints and visualizae keypoint connections (joint connections) in the section below.

    | Fish        | Chimpanzee | Colobus Monkey | Tiger | Clown fish | Seahorse | Turtle |
    | :---:          | :---:     | :---:     |:---:     |:---:     |:---:     |:---:     |
    | <img width="250" src=graphics/joints_fish_no_name.jpg>     | <img width="150" src=graphics/joints_chimpanzee.jpg>    | <img width="150" src=graphics/joints_colobus_monkey.jpg>    | <img width="250" src=graphics/joints_tiger.jpg>    | <img width="150" src=graphics/joints_clownfish.jpg>    | <img width="150" src=graphics/joints_seahorse.jpg>    | <img width="150" src=graphics/joints_turtle.jpg>    

    


## Annotation format (.pkl file)
- The annotations are provided as a `.pkl` file. The pickle files consists of following keys:

    | Key        | Description |
    | :---          | :---     |
    | W_GT          | Manual annotation. Non-NaN values for 1-2% of data. NaN values for the rest.      |
    | W_Pred        | 2D landmark predictions (labels) generated from MBW.       | 
    | S_Pred         | 3D landmark predictions (labels) generated from MBW. The 3D reconstructions are up-to-scale.       | 
    | BBox    | Bounding box crops generated from MBW          | 
    | confidence    | Flag specifying confidence for the MBW predictions. `True` specifies high confidence. `False` specifies low confidence. This flag is generated from the uncertainty equation (Eq. 2) given in the paper.          | 

# Images
Corresponding images are stored in the `images` directory as `.jpg` files. Each directory consists of 2-view synchronized image frames. 


# Visualization of labels
- The generated annotations (labels) could be visualized with the following shell script. To run the visualzation, run the following:
    ```
    cd python
    ./label_visualizations.sh
    ``` 
- Above shell script accepts the following arguments which you can change according to the need:
    | Argument        | Input options | Description | 
    | :---          | :---     | :---     |
    |    dataset       | `Fish`, `Colobus_Monkey`, `Chimpanzee` | Choose the object whose labels you want to visualize. 
    |    generate_labels_type       | `2D`, `3D`, `BBox` | Choose the type of label visualization. `2D` and `BBox` overlays the 2D landmark predictions and Bounding Box crops onto the images while `3D` label visualization generates a 3D skeleton structures with moving camera viewing angles.  
    |    vis_labels_path       | `Visualizations` | Path to store label visualizations 
    |   label_color | `blue`, `red` | Landmark (keypoint) colors for visualization 
    |img_format | `.jpg`, `.png` | Image storage format 
    | visualize_only_confident | Boolean flag |  Only visualize "confident" labels, i.e. verified as correct by MV-NRSfM Eq. (2) |
    
    

# Run on your own data (coming soon)!
- Since all we need are N-view synchroized image frames and annotations for 1-2% of data, all you need to provide are 2 or more views synchronized image frames and manual annotations for 1-2% of your data. After putting these annotations and image frames in the format shown above, MBW is able to provide 2D, 3D, and Bounding Box labels for your data. We will release the code for MBW soon.


