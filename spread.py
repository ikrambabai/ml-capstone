from PIL import Image
import os
import glob
import shutil
import operator
import math
import random
from shutil import copytree, ignore_patterns
from pathlib import Path


def remove_folder(folder_name):
    if os.path.exists(folder_name) and os.path.isdir(folder_name):
        print('Deleting folder' + folder_name)
        shutil.rmtree(folder_name)


def copy_content(src, destination, structure_only=True):
    copytree(src, destination, ignore=ignore_patterns('train', 'test', 'valid'))
    if structure_only:
        print('Removing contents of the subdirectories of {}'.format(destination))
        for directory in os.listdir(destination):
            print('Removing all content from directory {}'.format(destination + "/" + directory))
            delete_dir_content(destination + "/" + directory)


def delete_dir_content(directory):
    files = glob.glob(directory + '/*')
    for f in files:
        os.remove(f)


def count_files(folder):
    if os.path.exists(folder) and os.path.isdir(folder):
        return len(os.listdir(folder))
    return 0


def move_files(source_sub_folder_path, destination_sub_folder_path, collected_test_files_indices):
    for file in os.listdir(source_sub_folder_path):
        for target_file in collected_test_files_indices:
            if file.endswith('_' + str(target_file) + '.jpg'):
                source = source_sub_folder_path + '/' + file
                destination = destination_sub_folder_path + '/' + file
                shutil.move(source, destination)
                # print('File {} will be moved to {}'.format(source, destination))


def train_valid_files_index(all_images, test_destination, valid_destination, test_percentage=10, valid_percentage=10):
    total_files = 0
    file_counts = dict()
    for s_folder in os.listdir(all_images):
        if s_folder.startswith('.'):
            continue

        source_sub_folder_path = all_images + '/' + s_folder
        this_folder_count = count_files(source_sub_folder_path)
        total_files = total_files + this_folder_count
        file_counts[s_folder] = this_folder_count

        # count the total test and valid percentage that needs to get out reduced from valid
        total_deductable_percentage = valid_percentage + test_percentage

        effective_files_going_out = math.ceil((total_deductable_percentage / 100) * this_folder_count)

        collected_files = random.sample(range(1, this_folder_count), effective_files_going_out)
        print('{} percent of {} is {}'.format(total_deductable_percentage, this_folder_count,
                                              effective_files_going_out))

        effective_test_percentage = (test_percentage * 100) / total_deductable_percentage
        effective_valid_percentage = (valid_percentage * 100) / total_deductable_percentage

        index_at_dividing_percentage = math.floor((effective_test_percentage/100) * len(collected_files))

        print('effective_test_percentage {} , effective_valid_percentage {}'.
              format(effective_test_percentage, effective_valid_percentage))

        print('Collected files {}. Dividing index {}'.format(collected_files, index_at_dividing_percentage))

        collected_test_files_indices = collected_files[:index_at_dividing_percentage]
        collected_valid_files_indices = collected_files[index_at_dividing_percentage:]

        print('Will collect {} for test and {} for valid files.'
              .format(collected_test_files_indices, collected_valid_files_indices))

        move_files(source_sub_folder_path, test_destination + '/' + s_folder, collected_test_files_indices)
        move_files(source_sub_folder_path, valid_destination + '/' + s_folder, collected_valid_files_indices)

    sorted_d = sorted(file_counts.items(), key=operator.itemgetter(1), reverse=True)

    random.sample(range(1, 100), 3)
    return sorted_d,


def rename_files(source):
    for directory in os.listdir(source):
        if directory.startswith('.'):
            continue
        counter = 1
        for file in os.listdir(source + "/" + directory):
            old_path = source + "/" + directory + "/" + file
            new_name = source + "/" + directory + "/" + directory + "_" + str(counter) + ".jpg"
            print('Renamed {} to {}'.format(old_path, new_name))
            os.rename(old_path, new_name)
            counter = counter + 1


# rename_files('/Users/fi241c/dev/machine-learning/ml-capstone/rename-test')


def do_all():
    classified_images = '/Users/fi241c/dev/machine-learning/ml-capstone/image-low-separated2'

    final = '/Users/fi241c/dev/machine-learning/ml-capstone/images'
    train_folder = final + '/train'
    test_folder = final + '/test'
    valid_folder = final + '/valid'

    # 0. Create main / destination folder
    Path(final).mkdir(parents=True, exist_ok=True)

    # 1. Prepare train folder
    remove_folder(train_folder)
    copy_content(classified_images,  train_folder, structure_only=False)
    rename_files(train_folder)

    # 2. Prepare test folder
    remove_folder(test_folder)
    copy_content(classified_images, test_folder)

    # 3. Prepare valid folder
    remove_folder(valid_folder)
    copy_content(classified_images, valid_folder)

    a = train_valid_files_index(train_folder, test_folder, valid_folder)

    print('Total files you have collected {}'.format(a))


do_all()
