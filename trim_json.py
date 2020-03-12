import os
import json

def trim(data_json, categories):
	global valid_catids

	# for data in data_json:
	for data in sorted(data_json.keys(), reverse=True):
		# check image item
		if data == 'images':
			for i in range(len(data_json['images'])):
				image = dict()
				image['id'] = data_json['images'][i]['id']
				image['file_name'] = data_json['images'][i]['file_name']
				image['width'] = data_json['images'][i]['width']
				image['height'] = data_json['images'][i]['height']
				coco['images'].append(image)

		# check category item
		elif data == 'categories':
			for i in range(len(data_json['categories'])):
				append = True
				if data_json['categories'][i]['name'] in categories:
					for cat_data in coco['categories']:
						if data_json['categories'][i]['name'] == cat_data['name']:
							append = False
							break
					if append:
						cat = dict()
						cat['id'] = data_json['categories'][i]['id']
						valid_catids.append(cat['id'])
						cat['supercategory'] = 'none'
						cat['name'] = data_json['categories'][i]['name']
						cat['original_id'] = data_json['categories'][i]['original_id']
						coco['categories'].append(cat)

		# check annotation item
		elif data == 'annotations':
			for i in range(len(data_json['annotations'])):
				if data_json['annotations'][i]['category_id'] in valid_catids:
					anno = dict()
					anno['id'] = data_json['annotations'][i]['id']
					anno['area'] = int(data_json['annotations'][i]['area'])
					anno['iscrowd'] = data_json['annotations'][i]['iscrowd']
					anno['image_id'] = data_json['annotations'][i]['image_id']
					anno['bbox'] = [int(j) for j in data_json['annotations'][i]['bbox']]
					anno['category_id'] = data_json['annotations'][i]['category_id']
					anno['original_category_id'] = data_json['annotations'][i]['original_category_id']

					anno['segmentation'] = []
					seg = []
					bbox = anno['bbox']
					#bbox[] is x,y,w,h
					#left_top
					seg.append(bbox[0])
					seg.append(bbox[1])
					#left_bottom
					seg.append(bbox[0])
					seg.append(bbox[1] + bbox[3])
					#right_bottom
					seg.append(bbox[0] + bbox[2])
					seg.append(bbox[1] + bbox[3])
					#right_top
					seg.append(bbox[0] + bbox[2])
					seg.append(bbox[1])
					anno['segmentation'].append(seg)

					coco['annotations'].append(anno)

coco = dict()
coco['images'] = []
coco['annotations'] = []
coco['categories'] = []

valid_catids = []

categories = set()
data_dir = 'data_new'

for root, dirs, files in os.walk(data_dir):
	for class_dir in dirs:
		if class_dir not in ['train', 'val', 'test', 'Label', 'annotations']:
			categories.add(class_dir)

categories = list(categories)

for subset in ['val', 'test', 'train']:
	coco['images'] = []
	coco['annotations'] = []

	in_json_file = os.path.join(data_dir, 'annotations/{}-annotations-bbox.json'.format(subset))

	print("loading {}".format(in_json_file))
	with open(in_json_file) as json_file:
		data_json = json.load(json_file)

	print("trimming...")
	trim(data_json, categories)

	out_json_file = os.path.join(data_dir, 'annotations/{}-annotations-bbox_trim.json'.format(subset))
	with open(out_json_file, 'w') as outfile:
		json.dump(coco, outfile)
