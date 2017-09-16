#coding:utf-8

import os
import ConfigParser


def detect_local_config():
	results = {}
	config = ConfigParser.ConfigParser()
	with open('controller/lib/config.conf') as conf:
		try:
			config.readfp(conf)
			results['vulhub_path'] = config.get('base', 'vulhub_path')
			results['docker_switch'] = config.get('base', 'docker_switch')
		except:
			pass
	return results


def detect_local_vulhub():
	pass

def get_vulhub_version():
	vh_version = detect_local_config()

	if vh_version['vulhub_path']:
		vulhub_path = vh_version['vulhub_path'] if vh_version['vulhub_path'][-1] == '/' else vh_version['vulhub_path'] + "/"
		version_file = vulhub_path + '.git/FETCH_HEAD'
		if os.path.exists(version_file):
			return open(version_file).readline()[0:7]
		else:
			return ".git"
	else:
		return "None"