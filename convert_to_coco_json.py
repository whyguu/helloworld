#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Author: hbchen
# @Time: 2018-01-29
# @Description: pascal_voc数据集 xml格式 转换到 coco数据集 json格式
from __future__ import print_function
import os
import json
from xml.etree.ElementTree import ElementTree
import time


XML_PATH = "../nas/xuelang/xuelang_round1_train/"
JSON_PATH = "./tmp/xuelang_round1_train_good_bad.json"
json_obj = {}
images = []
annotations = []
categories = []
# categories = [{"id": 1, "name": 'bad', "supercategory": "none"}]

categories_dict = {}
annotation_id = 1
image_id = 1
category_id = 1


def read_xml(in_path):
    # 读取并解析xml文件
    t = ElementTree()
    t.parse(in_path)
    return t


def if_match(node, kv_map):
    """
    判断某个节点是否包含所有传入参数属性
    node: 节点
    kv_map: 属性及属性值组成的map
    """
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True


def get_node_by_keyvalue(nodelist, kv_map):
    """
    根据属性及属性值定位符合的节点，返回节点
    nodelist: 节点列表
    kv_map: 匹配属性及属性值map
    """
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes


def find_nodes(tree, path):
    """
    :param tree: xml树
    :param path: 节点路径
    :return:
    """

    return tree.findall(path)


if __name__ == '__main__':
    print("-----------------Start------------------")
    tic = time.time()
    xml_names = os.listdir(XML_PATH)

    for xml in xml_names:
        if os.path.splitext(xml)[1] != '.xml':
            continue
        print(xml)
        tree = read_xml(XML_PATH + "/" + xml)
        object_nodes = get_node_by_keyvalue(find_nodes(tree, "object"), {})
        if len(object_nodes) == 0:
            print(xml, "no object")
            continue

        image = {}
        file_name = os.path.splitext(xml)[0]  # 文件名
        image["file_name"] = file_name + ".jpg"
        width_nodes = get_node_by_keyvalue(find_nodes(tree, "size/width"), {})
        image["width"] = int(width_nodes[0].text)
        height_nodes = get_node_by_keyvalue(find_nodes(tree, "size/height"), {})
        image["height"] = int(height_nodes[0].text)
        # print(file_name)
        image["id"] = image_id
        image_id += 1
        images.append(image)    # 构建images

        name_nodes = get_node_by_keyvalue(find_nodes(tree, "object/name"), {})
        xmin_nodes = get_node_by_keyvalue(find_nodes(tree, "object/bndbox/xmin"), {})
        ymin_nodes = get_node_by_keyvalue(find_nodes(tree, "object/bndbox/ymin"), {})
        xmax_nodes = get_node_by_keyvalue(find_nodes(tree, "object/bndbox/xmax"), {})
        ymax_nodes = get_node_by_keyvalue(find_nodes(tree, "object/bndbox/ymax"), {})

        for index, _ in enumerate(object_nodes):
            if name_nodes[index].text not in categories_dict.keys():
                categories_dict[name_nodes[index].text] = category_id
                category = dict()
                category["supercategory"] = "none"
                category["id"] = category_id
                category_id += 1
                category["name"] = name_nodes[index].text
                categories.append(category)
            x_min = max(int(xmin_nodes[index].text), 0)
            x_max = min(int(xmax_nodes[index].text), image["width"])
            y_min = max(int(ymin_nodes[index].text), 0)
            y_max = min(int(ymax_nodes[index].text), image["height"])
            annotation = {}
            segmentation = []
            bbox = []
            seg_coordinate = []  # 坐标
            seg_coordinate.append(x_min)
            seg_coordinate.append(y_min)
            seg_coordinate.append(x_min)
            seg_coordinate.append(y_max)
            seg_coordinate.append(x_max)
            seg_coordinate.append(y_max)
            seg_coordinate.append(x_max)
            seg_coordinate.append(y_min)
            # seg_coordinate.append(int(ymin_nodes[index].text))
            segmentation.append(seg_coordinate)
            # width = int(xmax_nodes[index].text) - int(xmin_nodes[index].text)
            # height = int(ymax_nodes[index].text) - int(ymin_nodes[index].text)
            width = x_max - x_min
            height = y_max - y_min
            area = width * height

            bbox.append(x_min)
            bbox.append(y_min)
            # bbox.append(x_max)
            # bbox.append(y_max)
            bbox.append(width)
            bbox.append(height)

            annotation["segmentation"] = segmentation
            annotation["area"] = area
            annotation["iscrowd"] = 0
            annotation["image_id"] = image['id']  # file_name
            annotation["bbox"] = bbox
            annotation["category_id"] = categories_dict[name_nodes[index].text]
            annotation["id"] = annotation_id
            annotation_id += 1
            annotation["ignore"] = 0
            annotations.append(annotation)

    json_obj["images"] = images
    json_obj["type"] = "instances"
    json_obj["annotations"] = annotations
    json_obj["categories"] = categories

    f = open(JSON_PATH, "w")
    # json.dump(json_obj, f)
    json_str = json.dumps(json_obj, indent=4)
    f.write(json_str)
    f.close()

    print('cost: {:.2f} sec'.format(time.time() - tic))
    print("------------------End-------------------")
