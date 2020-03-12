import os
import shutil

categories = set()
image_dir = 'OID/Dataset'

for root, dirs, files in os.walk(image_dir):
	for class_dir in dirs:
		if class_dir not in ['train', 'validation', 'test', 'Label']:
			categories.add(class_dir)

categories = list(categories)

for class_name in categories:
	image_filenames = []

	for subset in ['train', 'validation', 'test']:
		src_dir = 'OID/Dataset/{}/{}'.format(subset, class_name)

		for root, dirs, files in os.walk(src_dir):
			for file in files:
				if file.endswith('.jpg'):
					image_filenames.append(file)

	num_img = len(image_filenames)
	num_train = int(num_img * 0.8)
	num_val = int(num_img * 0.1)

	print("class: {}".format(class_name))
	print("num img: {}".format(num_img))
	print("num train: {}".format(num_train))
	print("num val: {}".format(num_val))
	print("num test: {}".format(num_img - num_train - num_val))

	dst_dir_train = 'data_new/train/{}'.format(class_name)
	dst_dir_val = 'data_new/val/{}'.format(class_name)
	dst_dir_test = 'data_new/test/{}'.format(class_name)

	if not os.path.exists(dst_dir_train):
		os.mkdir(dst_dir_train)
	if not os.path.exists(dst_dir_val):
		os.mkdir(dst_dir_val)
	if not os.path.exists(dst_dir_test):
		os.mkdir(dst_dir_test)

	for root, dirs, files in os.walk(image_dir):
		for file in files:
			jpgfile = os.path.join(root, file)

			if file not in image_filenames:
				continue

			## first 80% put into train
			if num_train > 0:
				shutil.copy(jpgfile, dst_dir_train)
				num_train -= 1

			## next 10% put into val
			elif num_val > 0:
				shutil.copy(jpgfile, dst_dir_val)
				num_val -= 1

			## rest of images put into test
			else:
				shutil.copy(jpgfile, dst_dir_test)

			# take care of duplicates
			image_filenames.remove(file)