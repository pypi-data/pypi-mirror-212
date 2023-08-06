import xml.etree.ElementTree as ET
from tqdm import tqdm
import os
import io
import random
import pandas as pd
import tensorflow as tf
import numpy as np
from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict
import glob
import shutil

def xml_to_dataframe(path, include_string):
    classes_names = []

    classes_names.clear()
    if not os.path.exists(path) or len(include_string) == 0:
        print(f'invalid parameters: {path} {include_string}')
        return
    xml_list = []
    xml_target = os.path.join(path, include_string)
    file_list = glob.glob(xml_target)
    for xml_file in tqdm(file_list, desc=include_string):
        # sprint('---> ', xml_file)
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            classes_names.append(member.find('name').text)
            bndbox = member.find('bndbox')
            value = (root.find('filename').text,
                     int(root.find('size').find('width').text),
                     int(root.find('size').find('height').text),
                     member.find('name').text,
                     int(bndbox.find('xmin').text),
                     int(bndbox.find('ymin').text),
                     int(bndbox.find('xmax').text),
                     int(bndbox.find('ymax').text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    classes_names = list(set(classes_names))
    classes_names.sort()
    return xml_df, classes_names


def convert_to_csv(xml_path, include_string, output_file, labelmap_name):

    xml_df, classes_names = xml_to_dataframe(xml_path, include_string)

    # label map 생성
    labelmap_dir = os.path.dirname(output_file)
    label_map_path = os.path.join(labelmap_dir, labelmap_name)
    print(f'label_map_path > {label_map_path}')
    pbtxt_content = ""

    for i, class_name in enumerate(classes_names):
        pbtxt_content = (
                pbtxt_content
                + "item {{\n    id: {0}\n    name: '{1}'\n}}\n\n".format(i + 1, class_name)
        )
    pbtxt_content = pbtxt_content.strip()
    with open(label_map_path, "w") as f:
        f.write(pbtxt_content)
        print(f'Successfully created {labelmap_name}')

    # csv 파일 생성.
    output_path = os.path.dirname(output_file)
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

    xml_df.to_csv(output_file, index=None)

def __split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]

def create_one_tf_example(group, path, class_dict):
    with tf.io.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        if set(['xmin_rel', 'xmax_rel', 'ymin_rel', 'ymax_rel']).issubset(set(row.index)):
            xmin = row['xmin_rel']
            xmax = row['xmax_rel']
            ymin = row['ymin_rel']
            ymax = row['ymax_rel']
            xmins.append(xmin)
            xmaxs.append(xmax)
            ymins.append(ymin)
            ymaxs.append(ymax)

        elif set(['xmin', 'xmax', 'ymin', 'ymax']).issubset(set(row.index)):
            xmn = row['xmin'] / width
            if xmn < 0.0:
                xmn = 0.0
            elif xmn > 1.0:
                xmn = 1.0
            xmins.append(xmn)

            xmx = row['xmax'] / width
            if xmx < 0.0:
                xmx = 0.0
            elif xmx > 1.0:
                xmx = 1.0
            xmaxs.append(xmx)

            ymn = row['ymin'] / height
            if ymn < 0.0:
                ymn = 0.0
            elif ymn > 1.0:
                ymn = 1.0
            ymins.append(ymn)

            ymx = row['ymax'] / height
            if ymx < 0.0:
                ymx = 0.0
            elif ymx > 1.0:
                ymx = 1.0
            ymaxs.append(ymx)

        # xmins.append(xmin)
        # xmaxs.append(xmax)
        # ymins.append(ymin)
        # ymaxs.append(ymax)
        classes_text.append(str(row['class']).encode('utf8'))
        classes.append(class_dict[str(row['class'])])

    tf_example = tf.train.Example(features=tf.train.Features(
        feature={
            'image/height': dataset_util.int64_feature(height),
            'image/width': dataset_util.int64_feature(width),
            'image/filename': dataset_util.bytes_feature(filename),
            'image/source_id': dataset_util.bytes_feature(filename),
            'image/encoded': dataset_util.bytes_feature(encoded_jpg),
            'image/format': dataset_util.bytes_feature(image_format),
            'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
            'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
            'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
            'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
            'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
            'image/object/class/label': dataset_util.int64_list_feature(classes), }))
    return tf_example

def class_dict_from_pbtxt(pbtxt_path):
    # open file, strip \n, trim lines and keep only
    # lines beginning with id or display_name

    with open(pbtxt_path, 'r', encoding='utf-8-sig') as f:
        data = f.readlines()

    name_key = None
    if any('display_name:' in s for s in data):
        name_key = 'display_name:'
    elif any('name:' in s for s in data):
        name_key = 'name:'

    if name_key is None:
        raise ValueError(
            "label map does not have class names, provided by values with the 'display_name' or 'name' keys in the contents of the file"
        )

    data = [l.rstrip('\n').strip() for l in data if 'id:' in l or name_key in l]

    ids = [int(l.replace('id:', '')) for l in data if l.startswith('id')]
    names = [
        l.replace(name_key, '').replace('"', '').replace("'", '').strip() for l in data
        if l.startswith(name_key)]

    # join ids and display_names into a single dictionary
    class_dict = {}
    for i in range(len(ids)):
        class_dict[names[i]] = ids[i]

    return class_dict

# convert_to_csv(d:\python_work\tf-train-data\faces,
#                 "new_face_train_label01.csv,new_face_train_label02.csv",
#                 d:\python_work\tf-train-data\faces\face_label_map.pbtxt,
#                 d:\python_work\tf-train-data\faces\new_face_images,
#                 d:\python_work\tf-train-data\faces\new_face_train.tfrecord)
def convert_to_tfrecord(csv_path, csv_list, pbtxt_path, image_path, output_path):
    image_path = os.path.join(image_path)

    class_dict = class_dict_from_pbtxt(pbtxt_path)
    writer = tf.compat.v1.python_io.TFRecordWriter(output_path)

    csv_list = csv_list.split(',')
    for csv_input in csv_list:
        csv_target = os.path.join(csv_path, csv_path.strip())

        examples = pd.read_csv(csv_target)
        grouped = __split(examples, 'filename')

        for group in tqdm(grouped, desc='groups'):
            tf_example = create_one_tf_example(group, image_path, class_dict)
            writer.write(tf_example.SerializeToString())

        print(f'{csv_input} was processed')
        writer.flush()

    writer.close()
    print('Successfully created the TFRecords: {}'.format(output_path))

def divide_annotation(annotation_path, train_label, test_label):
    if not os.path.exists(annotation_path):
        print('Not Found: {}'.format(annotation_path))
        return

    if not os.path.exists(train_label):
        os.makedirs(train_label, exist_ok=True)

    if not os.path.exists(test_label):
        os.makedirs(test_label, exist_ok=True)

    # annotation_target_path = os.path.join(annotation_path, '*.xml')
    # all_anno_list = os.listdir(annotation_target_path)
    all_anno_list = glob.glob(annotation_path + '/*.xml')
    total_size = len(all_anno_list)
    print('size:', total_size)
    random.shuffle(all_anno_list)
    random.shuffle(all_anno_list)
    train_count = int(total_size * 0.8)
    test_count = total_size - train_count
    print('train:{} test:{}'.format(train_count, test_count))

    # progress = tqdm(total_size)
    # idx = 0
    list_range = np.arange(0, total_size)
    for idx in tqdm(list_range, desc='dividing annotations to train & test set'):
    # while idx < total_size:
        # print(idx, '-', all_anno_list[idx])
        xml_fullpath = all_anno_list[idx]
        if not os.path.exists(xml_fullpath):
            print('Not Found: {}'.format(xml_fullpath))
            # progress.update()
            continue
        if idx < train_count:
            target_path = os.path.join(train_label, os.path.basename(all_anno_list[idx]))
        else:
            target_path = os.path.join(test_label, os.path.basename(all_anno_list[idx]))

        if os.path.exists(target_path):
            os.remove(target_path)
        shutil.copy(xml_fullpath, target_path)