# Convert-Vott-to-yolo-format

Person collection.
Some scripts help to convert different object detection datasets formats.

## vott2yolo

A script to convert [VoTT](https://github.com/microsoft/VoTT) (Visual Object Tagging Tool) annotation file to yolo/darknet format

```text
usage: vott2yolo.py [-h] c vott imgs dst

positional arguments:
  c           class file
  vott        vott project dir
  imgs        dir path contains all images
  dst         destination path to save output files

optional arguments:
  -h, --help  show this help message and exit
```

A class file defines the origin class name and new class name.
A new class file will generated under the dst directory.

Eggs:

```text
origin_class_name1, new_class_name1
origin_class_name2, new_class_name2
origin_class_name3, new_class_name3
origin_class_name4, new_class_name4
origin_class_name5, new_class_name5

```
