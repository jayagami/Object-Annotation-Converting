#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import argparse
import os
import pprint
import xmltodict
import numpy as np
from model_data.net_config import config
import zipfile
import shutil
import time
from functools import wraps


# def args():
#     """
#     no need to recive args anymore, so comment.

#     Returns:
#         [args] -- [输入参数]
#     """
#     praser = argparse.ArgumentParser()
#     praser.add_argument("-s", help="源文件夹", dest="source_dir")
#     # praser.add_argument('-p',help="图片文件夹",dest='picture_dir')
#     praser.add_argument("-t", help="输出文件夹", dest="target_dir")
#     args = praser.parse_args()
#     return args


def timer(f):
    @wraps(f)
    def wrapper():
        print("start at {}".format(time.asctime()))
        start = time.time()
        f()
        end = time.time()
        print("Job finished, spend {}s".format(end - start))

    return wrapper


def get_classes(classes_path):
    """loads the classes"""
    with open(classes_path, encoding="utf8") as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]
    return class_names


def convert_to_eval(voc_data=None, gt_dir=None):
    """
    convert train.txt to separate file to calculate map
    :param trian_path:train.txt file path
    :param gt_dir:test dir path
    :return:ground truth box file per image
    """
    # os.makedirs(temp_dir)
    if voc_data and gt_dir:
        print("Direct generate from voc data!")
        if not os.path.isdir(gt_dir):
            os.mkdir(gt_dir)
        temp_dir = os.path.join(gt_dir, "temp")
        if not os.path.isdir(temp_dir):
            os.mkdir(temp_dir)
        print("Converting voc data to train.txt......")
        convert_voc_2_train(voc_data, temp_dir)
        print("Converting finished!")
        train_path = os.path.join(temp_dir, "train.txt")
        class_path = os.path.join(temp_dir, "voc_classes.txt")
    else:
        print("Load from train.txt")
        train_path = input("train.txt file path:  ")
        class_path = input("voc_class.txt file path: ")
        gt_dir = input("dir to save output:  ")
        temp_dir = os.path.join(gt_dir, "temp")
        if not os.path.isdir(gt_dir):
            os.mkdir(gt_dir)
    classes_name = get_classes(class_path)
    with open(train_path, "r") as train_txt:
        train_lines = train_txt.readlines()
        img_box_list = [img.strip() for img in train_lines]
    for boxes in img_box_list:
        img_info = boxes.split(" ")
        img_name = os.path.basename(img_info[0])
        gt_boxes_list = img_info[1:]
        if len(gt_boxes_list) > 0:
            gt_box_file = open(
                os.path.join(gt_dir, os.path.splitext(img_name)[0] + ".txt"), "w"
            )
            for box in gt_boxes_list:
                # print(box)
                box = box.split(",")
                x_min, y_min, x_max, y_max, class_id = box
                gt_box_file.write(
                    "{} {} {} {} {}\n".format(
                        classes_name[int(class_id)], x_min, y_min, x_max, y_max
                    )
                )
        # print("{} gt box saved!".format(img_name))
    if os.path.isdir(temp_dir):
        shutil.rmtree(temp_dir)
    print("\nJob Finished! ")


@timer
def compress():
    path = input("Input path: ")
    save_path = path
    shutil.make_archive(save_path, "zip", path)
    print("saved at {}".format(save_path))
    # zipf = zipfile.ZipFile(save_path, "w")
    # pre_len = len(os.path.dirname(path))
    # for parent, dirnames, filenames in os.walk(path):
    #     for filename in filenames:
    #         pathfile = os.path.join(parent, filename)
    #         archname = pathfile[pre_len:].strip(os.path.sep)
    #         zipf.write(pathfile, archname)
    # zipf.close()


@timer
def extract(path=config.PATH.VOCDIR):
    files = [os.path.join(path, file) for file in os.listdir(path)]
    files = list(filter(os.path.isfile, files))
    files = list(filter(lambda file: file.endswith(".zip"), files))
    for i, f in enumerate(files):
        print("id: {}, file: {}".format(i, f))
    file_id = input("choose id:")
    file_path = files[int(file_id)]
    # file_path = os.path.join(path, file_name)
    with zipfile.ZipFile(file_path, "r") as zip:
        extract_path = os.path.splitext(file_path)[0]
        if not os.path.isdir(extract_path):
            os.mkdir(extract_path)
        zip.printdir()
        zip.extractall(path=extract_path)
    print("Extrall finished!")


def remove():
    # log_dirs = list(
    # os.path.join(logs_path, dir) for dir in os.listdir(logs_path)
    # )
    # for i, d in enumerate(log_dirs):
    # print("id:{}, dir: {}".format(i, d))
    while True:
        # index = input("Input id to delete: ")
        # try:
        # path = log_dirs[int(index)]
        # except Exception:
        # print("Please Input Right ID!!！")
        # break
        path = input("Input path to delete: ")
        make_sure = input("Input 'y' to remove {}, others to exit: ".format(path))
        if make_sure == "y":
            if os.path.isdir(path):
                try:
                    # shutil.rmtree(log_dirs[int(index)])
                    shutil.rmtree(path)
                except Exception:
                    print("Can't remove floder {}".format(path))
                else:
                    print("{} removed".format(path))
            elif os.path.isfile(path):
                try:
                    os.remove(path)
                except Exception:
                    print("Can't remove file {}".format(path))
                else:
                    print("{} removed".format(path))
        else:
            break


def get_class(class_dir, target_dir):
    """
    获取VOC目录内所有的分类种类
    :param dir: voc数据集目录
    :return: 分类序号字典
    """
    class_set = set()
    for file in os.listdir(class_dir):
        file = file.split(".")[0]
        class_set.add(file.split("_")[0])
        # print(class_set)
    with open(os.path.join(target_dir, "voc_classes.txt"), "w") as voc_classes:
        for class_name in class_set:
            voc_classes.write("{}\n".format(class_name))
    # print("getting class {}".format(os.path.basename(class_dir)))
    return class_set


def read_xml(xml_file, class_dict):
    xml_name = os.path.basename(xml_file)
    # print("reading {}".format(xml_name))
    with open(xml_file, "rb") as xml:
        content = xmltodict.parse(xml)
    # pprint.pprint(content)
    # return content
    if "object" not in content["annotation"]:
        return None
    img_path = content["annotation"]["path"]

    # ! vott has many bugs, one is the image path is wrong.
    # img_path = os.path.join(
    #     img_path.split("/")[0], "JPEGImages", img_path.split("/")[2]
    # )
    # print(img_path)

    # ! Deprecated to use, now all image path was in the same dir.
    #  img_path = os.path.join("/".join(xml_file.split("/")[:-3]), img_path)

    img_name = content["annotation"]["filename"]
    img_path = os.path.join(config.PATH.IMGDIR, img_name)
    # img_anno.append(img_path)
    boxes = content["annotation"]["object"]
    # pprint.pprint(boxes)
    img_path = os.path.abspath(img_path)
    img_list = [img_path]

    if type(boxes) is list:
        for box in boxes:
            img_anno = []
            # print('---Box is',box)
            img_anno.append(box["bndbox"]["xmin"])
            img_anno.append(box["bndbox"]["ymin"])
            img_anno.append(box["bndbox"]["xmax"])
            img_anno.append(box["bndbox"]["ymax"])
            try:
                img_anno.append(class_dict[box["name"]])
            except KeyError:
                print(xml_file)
                continue
            img_anno = np.array(img_anno).astype(float).astype(int).astype(str).tolist()
            # print(img_anno)
            # print(type(img_anno))
            box_value = ",".join(img_anno)
            img_list.append(box_value)
    else:
        img_anno = []
        img_anno.append(boxes["bndbox"]["xmin"])
        img_anno.append(boxes["bndbox"]["ymin"])
        img_anno.append(boxes["bndbox"]["xmax"])
        img_anno.append(boxes["bndbox"]["ymax"])
        try:
            img_anno.append(class_dict[boxes["name"]])
        except KeyError:
            print("Not in classes!!!")
            print(xml_file)
        img_anno = np.array(img_anno).astype(float).astype(int).astype(str).tolist()
        # print(boxes["name"])
        box_value = ",".join(img_anno)
        img_list.append(box_value)
    annotation = " ".join(img_list)
    # with open(os.path.join(target_dir,), 'w') as to_write:
    # to_write.write(annotation)
    # print("finish {}".format(img_name))
    return annotation


def all_dir_dataset(source_path):
    all_Annotation_dir = []
    all_Main_dir = []
    for roots, dirs, files in os.walk(source_path):
        for floder in dirs:
            if floder == "Annotations":
                all_Annotation_dir.append(os.path.join(roots, "Annotations"))
            elif floder == "Main":
                all_Main_dir.append(os.path.join(roots, "Main"))
    return all_Annotation_dir, all_Main_dir


def convert_voc_2_train(source_dir=None, target_dir=None):
    if not (source_dir and target_dir):
        source_dir = config.PATH.VOCDIR
        target_dir = "/".join(str(config.PATH.ANNO).split("/")[:-1])
        print("Source dir is {}".format(os.path.abspath(source_dir)))
        print("Output dir is {}".format(os.path.abspath(target_dir)))
        confirm = input("Input 'y' to continue, 'c' to change:")
        if confirm == "y":
            print("save to model_data")
        elif confirm == "c":
            source_dir = input("Input source path: ")
            target_dir = input("Input out path: ")
            print("Path changed! train.txt and voc_classes will be saved to outdir")
            print("Source dir is {}".format(os.path.abspath(source_dir)))
            print("Output dir is {}".format(os.path.abspath(target_dir)))
        else:
            assert confirm == "y", "You are not ready!!!"

    # current_dir = os.getcwd()
    # true_target_dir = os.path.abspath(target_dir)
    Annotation_dirs, Main_dirs = all_dir_dataset(source_dir)
    Class = set()
    for main_dir in Main_dirs:
        new_class = get_class(main_dir, target_dir)
        Class = Class.union(new_class)
    with open(os.path.join(target_dir, "voc_classes.txt"), "w") as voc_classes:
        for class_name in Class:
            voc_classes.write("{}\n".format(class_name))
    Class_dict = {v: str(k) for k, v in enumerate(Class)}  # all class
    pprint.pprint(Class_dict)
    annotation_file = open(os.path.join(target_dir, "train.txt"), "w")
    annotation_list = []
    for annotation_dir in Annotation_dirs:
        for roots, dirs, files in os.walk(annotation_dir):
            for voc_xml in files:
                img_annotation = read_xml(os.path.join(roots, voc_xml), Class_dict)
                if img_annotation is None:
                    continue
                annotation_list.append(img_annotation)
    for annotation in annotation_list:
        annotation_file.write(annotation + "\n")
    annotation_file.close()
    print("Congratulations, data has been transformed!")

if __name__ == "__main__":
    source_dir=""
    target_dir=""
    convert_voc_2_train(source_dir,target_dir)