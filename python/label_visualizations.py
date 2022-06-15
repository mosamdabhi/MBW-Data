"""
This script visualizes the 2D, 3D, or Bounding-Box labels generated
by MBW.
Author: Mosam Dabhi
Date: June 8, 2022
"""

import argparse
import os
from pathlib import Path

import _pickle as cPickle
import matplotlib.image as img
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objs as go
import scipy.io as sio
from matplotlib.patches import Rectangle
from natsort import natsorted
from tqdm import tqdm

from joints_function import extract_bone_connections, get_joints


def make_dir(str_path):
    """ Make directory """
    if not os.path.isdir(str_path):
        os.mkdir(str_path)


def get_colors():
    """ Get color palette """
    color_palette = {
        "color_blue": "rgb(0, 0, 255)",
        "color_red": "rgb(255, 0, 0)",
        "color_green": "rgb(0,255,0)",
    }
    return color_palette


def get_trace3d(joint_connections, points3d, point_color=None, line_color=None, name="PointCloud"):
    """Yields plotly traces for visualization"""
    if point_color is None:
        point_color = "rgb(30, 20, 160)"
    if line_color is None:
        line_color = "rgb(30, 20, 160)"

    # Trace of points
    trace_pts = go.Scatter3d(
        x=points3d[:, 0],
        y=points3d[:, 2],
        z=points3d[:, 1],
        mode="markers",
        name=name,
        marker=dict(symbol="circle", size=6, color=point_color),
    )

    # Trace of line
    xlines, ylines, zlines = [], [], []
    for line in joint_connections:
        for point in line:
            xlines.append(points3d[point, 0])
            ylines.append(points3d[point, 2])
            zlines.append(points3d[point, 1])
        xlines.append(None)
        ylines.append(None)
        zlines.append(None)
    trace_lines = go.Scatter3d(
        x=xlines, y=ylines, z=zlines, mode="lines", name=name, line=dict(width=6, color=line_color)
    )

    return [trace_pts, trace_lines]


def get_figure3d(color, joint_connections, camera_angles, points3d, gt=None, range_scale=2500):

    """Yields plotly figure for visualization"""

    traces = get_trace3d(joint_connections, points3d, color[0], color[0], "Predicted KP")
    if gt is not None:
        traces += get_trace3d(gt, color[1], color[1], "Groundtruth KP")

    layout = go.Layout(
        scene=dict(
            aspectratio=dict(x=0.8, y=0.8, z=2),
            xaxis=dict(range=(-0.4 * range_scale, 0.4 * range_scale)),
            yaxis=dict(range=(-0.4 * range_scale, 0.4 * range_scale)),
            zaxis=dict(range=(-1 * range_scale, 1 * range_scale)),
        ),
        width=700,
        margin=dict(r=20, l=10, b=10, t=10),
        scene_camera=dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=camera_angles[0], y=camera_angles[1], z=1.25),
        ),
    )
    return go.Figure(data=traces, layout=layout)


def process_dataset(args, pkl_names):
    """
    Dataset processing
    """
    W_Pred = []
    S_Pred = []
    W_GT = []
    confidence = []
    BBox = []

    for cam_idx in range(len(pkl_names)):

        """ Load the pickle file """
        with open(pkl_names[cam_idx], "rb") as fid:
            pickled_data = cPickle.load(fid)

        """ Fill the data relevant to the camera id """
        W_tmp = []
        S_tmp = []
        W_GT_tmp = []
        confidence_tmp = []
        BBox_tmp = []

        for frame_idx in range(len(pickled_data)):
            W_tmp.append(pickled_data[frame_idx]["W_Pred"])
            S_tmp.append(pickled_data[frame_idx]["S_Pred"])
            confidence_tmp.append(pickled_data[frame_idx]["confidence"])
            W_GT_tmp.append(pickled_data[frame_idx]["W_GT"])
            BBox_tmp.append(pickled_data[frame_idx]["BBox"])

        W_tmp = np.asarray(W_tmp)
        S_tmp = np.asarray(S_tmp)
        W_GT_tmp = np.asarray(W_GT_tmp)
        confidence_tmp = np.asarray(confidence_tmp)
        BBox_tmp = np.asarray(BBox_tmp)
        W_Pred.append(W_tmp)
        S_Pred.append(S_tmp)
        W_GT.append(W_GT_tmp)
        confidence.append(confidence_tmp)
        BBox.append(BBox_tmp)

    W_Pred = np.asarray(W_Pred)
    S_Pred = np.asarray(S_Pred)
    W_GT = np.asarray(W_GT)
    confidence = np.asarray(confidence)
    BBox = np.asarray(BBox)

    return W_Pred, S_Pred, confidence, BBox, W_GT


def visualize_labels(args, im, W, BBox, confidence, img_store_location, joint_connections):

    total_views = len(im)
    color_kpts = args.label_color

    subplots = plt.subplots(1, total_views)
    fig = subplots[0]
    axes = subplots[1]

    for cam_idx in range(total_views):
        axes[cam_idx].imshow(im[cam_idx])

        # 2D label visualizations
        if args.generate_labels_type == "2D":
            if args.visualize_only_confident:
                if confidence[cam_idx]:
                    axes[cam_idx].scatter(
                        x=W[cam_idx, :, 0], y=W[cam_idx, :, 1], c=color_kpts, s=40
                    )
                    xlines, ylines = extract_bone_connections(W[cam_idx, :, :], joint_connections)
                    axes[cam_idx].plot(xlines, ylines, c=color_kpts, linewidth=4)
            else:
                axes[cam_idx].scatter(x=W[cam_idx, :, 0], y=W[cam_idx, :, 1], c=color_kpts, s=40)
                xlines, ylines = extract_bone_connections(W[cam_idx, :, :], joint_connections)
                axes[cam_idx].plot(xlines, ylines, c=color_kpts, linewidth=4)

        # BBox label visualizations
        elif args.generate_labels_type == "BBox":
            xmax, xmin, ymax, ymin = (
                BBox[cam_idx, 0],
                BBox[cam_idx, 1],
                BBox[cam_idx, 2],
                BBox[cam_idx, 3],
            )
            axes[cam_idx].add_patch(
                Rectangle(
                    (xmin, ymin),
                    (xmax - xmin),
                    (ymax - ymin),
                    edgecolor=color_kpts,
                    facecolor="none",
                    linewidth=3,
                )
            )

        axes[cam_idx].axes.xaxis.set_visible(False)
        axes[cam_idx].axes.yaxis.set_visible(False)

    figure = plt.gcf()
    figure.set_size_inches(38, 36)
    plt.savefig(img_store_location, bbox_inches="tight")
    plt.cla()
    plt.clf()
    plt.close()


def main(args):

    # Extract annotation and image file paths
    dataset_img = "../Data/" + args.dataset + "/images/"
    dataset_annot = "../Data/" + args.dataset + "/annot/"

    # Generate directories to store visualizations
    logs_path = "../" + args.vis_labels_path
    make_dir(logs_path)
    logs_path = logs_path + "/" + args.dataset
    make_dir(logs_path)

    # Extract annotations
    pkl_names = []
    for path in Path(dataset_annot).rglob("*.pkl"):
        pkl_names.append(path)
    pkl_names = [Path(p) for p in natsorted([str(p) for p in pkl_names])]

    # Find total number of views
    total_views = len(pkl_names)

    # Find total number of frames
    with open(str(pkl_names[0]), "rb") as fid:
        pickled_data = cPickle.load(fid)
    total_frames = len(pickled_data)

    # Find number of joints/keypoints
    num_joints = pickled_data[0]["W_GT"].shape[1]

    # Extract joint connections
    joint_connections, range_scale, rigid_rotation = get_joints(args.dataset)

    # Extract all labels
    W_Pred, S_Pred, confidence, BBox, W_GT = process_dataset(args, pkl_names)
    S_Pred = S_Pred[0, :, :, :]

    # Make directory to store label visualizations
    logs_path = logs_path + "/" + args.generate_labels_type
    make_dir(logs_path)

    ################### 2D and BBox Visualizations ##################
    if args.generate_labels_type == "2D" or args.generate_labels_type == "BBox":
        image_paths = []
        for cam_idx in range(total_views):
            image_paths_ = []
            for path in Path(dataset_img + "/CAM_" + str(cam_idx + 1) + "/").rglob("*.jpg"):
                image_paths_.append(path)
            image_paths_ = [Path(p) for p in natsorted([str(p) for p in image_paths_])]
            image_paths.append(image_paths_)
        image_paths = np.asarray(image_paths)

        for frame_idx in tqdm(range(total_frames)):
            im = []
            for cam_idx in range(total_views):
                im.append(img.imread(image_paths[cam_idx, frame_idx]))
            img_store_location = logs_path + "/" + str(frame_idx) + args.img_format
            visualize_labels(
                args,
                im,
                W_Pred[:, frame_idx, :, :],
                BBox[:, frame_idx],
                confidence[:, frame_idx],
                img_store_location,
                joint_connections,
            )

    ################### 3D Visualizations ##################
    elif args.generate_labels_type == "3D":

        # Grab colors for 3D visualization
        colors = get_colors()
        color_blue, color_red = colors["color_blue"], colors["color_red"]
        colors = []
        colors.append(color_blue)
        colors.append(color_red)

        # Get camera rotations to look around the object.
        mat_contents = sio.loadmat("camera_rotations.mat")
        cam_x = mat_contents["x_final"][0].tolist()
        cam_y = mat_contents["y_final"][0].tolist()
        cam_counter = 0
        for idx in tqdm(range(S_Pred.shape[0])):
            if ~np.any(S_Pred[idx, :, :] == 0):
                if cam_counter == len(cam_x):
                    cam_counter = 0
                cam_angle = (cam_x[cam_counter], cam_y[cam_counter])
                img_store_location = logs_path + "/" + str(idx) + args.img_format
                fig = get_figure3d(
                    colors,
                    joint_connections,
                    cam_angle,
                    S_Pred[idx, :, :] @ rigid_rotation,
                    range_scale=range_scale,
                )
                fig.write_image(img_store_location)
                cam_counter = cam_counter + 1

    print("Finished the visualization of {} labels.".format(args.generate_labels_type))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", help="dataset selection", default="Chimpanzee")
    parser.add_argument("--generate_labels_type", help="2D, 3D, BBox", default="2D")
    parser.add_argument(
        "--vis_labels_path", help="Path to store label visualizations", default="Label_Vis"
    )
    parser.add_argument("--label_color", help="Landmark color for visualization", default="blue")
    parser.add_argument(
        "--img_format", help="Image storage format. Choose from .jpg or .png", default="blue"
    )

    parser.add_argument(
        "--visualize_only_confident", help="Only visualize confident labels", action="store_true"
    )
    args = parser.parse_args()
    main(args)
