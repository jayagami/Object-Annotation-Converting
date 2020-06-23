#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/10/2020 10:33 PM
# @Author  : Jay
# @Site    :
# @File    : df2text.py
# @Software: vscode
# convert vott format dataset to yolo format

import json
import os
import argparse


class Vott2Yolo:
    def __init__(self, class_file, vott_dir, dst_dir, image_dir):
        super().__init__()
        self.custom_path = class_file
        self.vott_dir = vott_dir
        self.save_dir = dst_dir
        self.image_dir = image_dir
        self.custom_class_id = self._class_gen()
        print(self.custom_path)

    def _class_gen(self, custom_path="", save_dir=""):
        # gen each class information
        custom_path = self.custom_path
        save_path = os.path.join(self.save_dir, "voc_classes.txt")
        custom_class = {}
        with open(custom_path, "r", encoding="utf8") as custom_io:
            for line in custom_io.readlines():
                if line.strip():
                    line = line.strip().split(",")
                    key = line[0]
                    item = line[1]
                    custom_class[key] = item
        class_set = set()
        for key, item in custom_class.items():
            class_set.add(item)
        class_tuple = tuple(class_set)
        class_tuple = tuple(sorted(class_tuple))

        custom_class_id = {}
        for key, item in custom_class.items():
            custom_class_id[key] = class_tuple.index(item)
        with open(save_path, "w", encoding="utf8") as voc_class:
            for class_name in class_tuple:
                voc_class.write(class_name + "\n")
            print("voc_class.txt saved!")
        return custom_class_id

    def _get_image_info(self, json_path="", custom_class_id={}):
        # get infor of each image in yolo
        custom_class_id = self.custom_class_id
        image_anno = open(json_path, "r", encoding="utf8")
        anno_dict = json.loads(image_anno.read())
        image_info = os.path.join(self.image_dir, anno_dict["asset"]["name"])
        for box in anno_dict["regions"]:
            box_class = box["tags"]
            try:
                box_id = custom_class_id[box_class[0]]
            except NameError:
                print(box_class)
                Exception()
            xmin = box["points"][0]["x"]
            ymin = box["points"][0]["y"]
            xmax = box["points"][2]["x"]
            ymax = box["points"][2]["y"]
            box_info = " " + ",".join(
                [str(int(float(v))) for v in [xmin, ymin, xmax, ymax, box_id]]
            )
            image_info += box_info
        image_anno.close()
        return image_info

    def train_gen(self, vott_dir="", save_train_path=""):
        save_train_path = os.path.join(self.save_dir, "train.txt")
        train_list = []
        for roots, dirs, files in os.walk(self.vott_dir):
            for f in files:
                if f.endswith("json"):
                    train_list.append(self._get_image_info(os.path.join(roots, f)))
        with open(save_train_path, "w", encoding="utf8") as train:
            for line in train_list:
                train.write(line + "\n")
        print("Finished!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("c", help="class file of objects")
    parser.add_argument("vott", help="vott project dir")
    parser.add_argument("dst", help="dir path to save object files")
    parser.add_argument("imgs", help="path of image dir")
    args = parser.parse_args()
    print("Starting to convert data\n =========")
    Vott2Yolo(
        class_file=args.c, vott_dir=args.vott, dst_dir=args.dst, image_dir=args.imgs,
    ).train_gen()
    print("Job finished!")

