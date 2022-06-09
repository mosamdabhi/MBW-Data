#!/bin/bash 

### Argument with values
dataset='Chimpanzee'                # Options: 'Chimpanzee', 'Fish', 'Colobus_Monkey'
generate_labels_type='3D'           # Options: '2D', '3D', 'BBox'
vis_labels_path='Visualizations'    # Path to store label visualizations
label_color='blue'                  # Landmark color for visualization
img_format='.jpg'                   # Image storage format. Options: .jpg or .png

### Argument with flags. Enable or disable this flag when calling main file.
#visualize_only_confident           # Only visualize "confident" labels, i.e. verified as correct by MV-NRSfM

python3 label_visualizations.py --dataset=$dataset \
                                --generate_labels_type=$generate_labels_type \
                                --vis_labels_path=$vis_labels_path \
                                --img_format=$img_format \
                                --visualize_only_confident