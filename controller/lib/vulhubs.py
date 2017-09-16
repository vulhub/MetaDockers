#coding:utf-8
#事情是这样的，本来tables的实现是state匹配已经build的 -> 根据build的id or child id —> 匹配run的
#放弃了被docker child交叉复用的坑，将containers独立出来，也精确。

import os
import yaml
import json
from controller.lib import localDetect
from dockerfile_parse import DockerfileParser
from dockerOperation import dockerOperation

class vulhubOperation:
	def __init__(self):
		self.vulhub_path = localDetect.detect_local_config()['vulhub_path']
		self.vulhub_base = []
		self.dockerOperation = dockerOperation()
		#:problem
		self.docker_images = self.dockerOperation.get_docker_images()

	def detection_local_vulhub_struct(self):
		results = []

		for i in os.walk(self.vulhub_path):
			dict_tmp = {}
			if 'docker-compose.yml' in i[-1]:
				dict_tmp['name'] = i[0].replace(self.vulhub_path, '')[1:]
				dict_tmp['engine'] = []
				dict_tmp['author'] = 'Anonymous'

				if os.path.isfile(i[0] + "/Dockerfile"):
					dfp = DockerfileParser()
					dfp.content = open(i[0] + "/Dockerfile").read()
					for j in json.loads(dfp.json):
						if j.keys()[0].upper() == 'FROM': dict_tmp['engine'].append([j.values()[0]])
						if j.keys()[0].upper() == 'MAINTAINER': dict_tmp['author'] = j.values()[0]

				with open(i[0] + "/docker-compose.yml") as f:
					for k, v in yaml.load(f)['services'].items():
						if 'image' in v.keys():
							dict_tmp['engine'].append([v['image']])

				# whetherBuild = map(lambda x: x in [i['RepoTags'][0] for i in self.docker_images], dict_tmp['engine'])

				flag = []
				for k, v in enumerate(dict_tmp['engine']):
					if v[0] in [x['RepoTags'][0] for x in self.docker_images]:
						flag.append(True)
						dict_tmp['engine'][k].append("true")
					else:
						flag.append(False)
						dict_tmp['engine'][k].append("false")

				if False not in flag:
					dict_tmp['state'] = 'Ready'
				else:
					dict_tmp['state'] = 'noPull'

				results.append(dict_tmp)

		return results

	def run(self):
		pass

if __name__ == '__main__':
	print vulhubOperation().detection_local_vulhub_struct()