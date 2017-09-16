#coding:utf-8

import time
import json
import docker
from localDetect import detect_local_config as dlc
from misc import bytesConvert

class dockerOperation:
	def __init__(self):
		self.client = self.docker_switch_init()


	def docker_switch_init(self):
		docker_switch = False
		try:
			if docker.from_env().version():
				docker_switch = docker.from_env()
			elif dlc()['docker_switch']:
				if docker.DockerClient(base_url=dlc()['docker_switch']).version():
					docker_switch = docker.DockerClient(base_url=dlc()['docker_switch'])
		except:
			pass
		finally:
			return docker_switch


	def get_docker_info(self, args):
		infos = self.client.info()

		if args == 'all':
			return infos
		elif args == 'base':
			attrs_tmp = {}
			attrs_tmp['version'] = infos['ServerVersion']
			attrs_tmp['MemSize'] = bytesConvert(infos['MemTotal'])
			attrs_tmp['cpu'] = infos['NCPU']
			attrs_tmp['Containers'] = infos['Containers']
			attrs_tmp['ContainersRunning'] = infos['ContainersRunning']
			return attrs_tmp


	def get_docker_images(self):
		docker_attrs = []
		for i in self.client.images.list():
			i.attrs['Size'] = bytesConvert(i.attrs['Size'])
			i.attrs['Created'] = '/'.join([str(t) for t in time.localtime(i.attrs['Created'])][:3])
			docker_attrs.append(i.attrs)
		return docker_attrs


	def get_docker_images_num(self, args):
		imagesList = self.client.images.list()

		if args == 'sum':
			return len(imagesList)
		elif args == 'size':
			return bytesConvert(reduce(lambda x, y: x + y, map(lambda x: x['Size'], [i.attrs for i in self.client.images.list()])))


	def get_docker_images_info(self, imageId):
		return self.client.images


	def get_containers(self, **kwargs):
		if kwargs:
			result_attrs = self.client.containers.get(kwargs['csId']).attrs
			result_attrs['inPorts'] = []
			csNetworks = result_attrs['NetworkSettings']
			if csNetworks:
				result_attrs['ip'] = csNetworks['Networks'].values()[0]['IPAddress']
				for k, v in csNetworks['Ports'].items():
					if v != None:
						result_attrs['inPorts'].append("{}:{}->{}".format(v[0]['HostIp'], v[0]['HostPort'], k))
					else:
						result_attrs['inPorts'].append(k)

			return result_attrs

		containers_attrs = [i.attrs for i in self.client.containers.list(all=True)]
		result_attrs = []
		for x in containers_attrs:
			attrs_tmp = {}
			attrs_tmp['Id'] = x['Id'][:12]
			attrs_tmp['Name'] = x['Name'][1:] if x['Name'][0] == '/' else x['Name']
			attrs_tmp['Image'] = x['Config']['Image']
			attrs_tmp['State'] = x['State']['Status']
			result_attrs.append(attrs_tmp)

		return result_attrs


	def get_docker_child(self, issince):
		return self.client.images.list(filters={"since": issince})


	def get_docker_networks(self, args=None,**kwargs):

		if args == 'sum':
			return len(self.client.networks.list())
		elif args == 'all':
			networks_attrs = [i.attrs for i in self.client.networks.list()]
			result_attrs = []
			for x in networks_attrs:
				attrs_tmp = {}
				attrs_tmp['Name'] = x['Name']
				attrs_tmp['Id'] = x['Id'][:12]
				attrs_tmp['Scope'] = x['Scope']
				attrs_tmp['Driver'] = x['Driver']
				attrs_tmp['IPAM_Driver'] = x['IPAM']['Driver'] if x['IPAM']['Driver'] else '-'
				attrs_tmp['IPAM_Subnet'] = x['IPAM']['Config'][0]['Subnet'] if x['IPAM']['Config'] else '-'
				attrs_tmp['IPAM_Gateway'] = x['IPAM']['Config'][0]['Gateway'] if x['IPAM']['Config'] else '-'
				result_attrs.append(attrs_tmp)
			return result_attrs
		elif kwargs:
			result_attrs = {}
			nwTarget = self.client.networks.get(kwargs['nwId'])
			result_attrs['Id'] = nwTarget.id
			result_attrs['options'] = nwTarget.attrs['Options']
			result_attrs['containers'] = []

			if nwTarget.containers:
				for i in nwTarget.containers:
					attrs_tmp = {}
					attrs_tmp['Id'] = i.attrs['Id'][:12]
					attrs_tmp['Name'] = i.attrs['Name'][1:] if i.attrs['Name'][0] == '/' else i.attrs['Name']
					attrs_tmp['IPv4'] = "{}/{}".format(i.attrs['NetworkSettings']['IPAddress'], i.attrs['NetworkSettings']['IPPrefixLen'])
					attrs_tmp['IPv6'] = i.attrs['NetworkSettings']['GlobalIPv6Address'] if i.attrs['NetworkSettings']['GlobalIPv6Address'] else '-'
					attrs_tmp['Mac'] = i.attrs['NetworkSettings']['MacAddress']
					result_attrs['containers'].append(attrs_tmp)
			return result_attrs
		else:
			pass


	def get_docker_volumes(self, args):

		if args == 'sum':
			return len(self.client.volumes.list())
		elif args == 'detail':
			volumes_attrs = [i.attrs for i in self.client.volumes.list()]
			result_attrs = []
			for x in volumes_attrs:
				attrs_tmp = {}
				attrs_tmp['Name'] = x['Name']
				attrs_tmp['Scope'] = x['Scope']
				attrs_tmp['Driver'] = x['Driver']
				attrs_tmp['Mountpoint'] = x['Mountpoint']
				result_attrs.append(attrs_tmp)
			return result_attrs


	def image_operation(self, dicts):
		opt = dicts['opt']
		imageId = dicts['imageId']

		try:
			if opt == 'runCmd':
				return self.client.containers.run(imageId, dicts['cmd'])
			elif opt == 'run':
				dictsTmp = json.loads(dicts['cmdAttrs'])
				blkioWeightDevice = {}

				if dictsTmp['blkio_weight_device'][0]:
					for x in dictsTmp['blkio_weight_device']: blkioWeightDevice[x.split("=")[0]] = x.split("=")[1]

				if dictsTmp['run_detach'] == 'True':
					return "csId=" + self.client.containers.run(imageId,dictsTmp['run_command'] if dictsTmp['run_command'] else '',
					                                            detach=True,
					                                            blkio_weight_device=blkioWeightDevice if blkioWeightDevice else None,
					                                            blkio_weight=int(dictsTmp['run_blkio_weight']) if dictsTmp['run_blkio_weight'] else None).id[:12]
				else:
					return "true"
			else:
				pass
		except docker.errors.APIError, e:
			return e


	def container_operation(self, dicts):
		opt = dicts['opt']
		csId = dicts['csId']
		oper_obj = self.client.containers.get(csId)

		try:
			if opt == 'cs_logs':
				return self.client.containers.get(csId).logs()
			elif opt == 'cs_rename':
				oper_obj.rename(dicts['newName'])
			elif opt == 'cs_remove':
				oper_obj.remove(force=True)
			else:
				eval("oper_obj.{}()".format(opt[3:]))
			return "true"
		except docker.errors.APIError, e:
			return e


	def volume_operation(self, dicts):
		opt = dicts['opt']
		try:
			if opt == 'add_volume':
				addDetail = json.loads(dicts['addDetail'])

				newLabels = {}
				if addDetail['newLabels'][0]:
					for x in addDetail['newLabels']: newLabels[x.split("=")[0]] = x.split("=")[1]

				newDriverOpt = {}
				if addDetail['newDriverOpt'][0]:
					for x in addDetail['newDriverOpt']: newDriverOpt[x.split("=")[0]] = x.split("=")[1]

				return self.client.volumes.create(name=addDetail['newName'], driver=addDetail['newDriver'], driver_opts=newDriverOpt, labels=newLabels)
			elif opt == 'rm_volume':
				for i in json.loads(dicts['rmList']): self.client.volumes.get(i).remove()
				return "true"
		except docker.errors.APIError, e:
			return e


	def network_operation(self, dicts):
		opt = dicts['opt']
		try:
			if opt == 'add_network':
				addDetail = json.loads(dicts['addDetail'])

				ipam_config = {}
				if addDetail['subnet'] and addDetail['gateway']:
					ipam_pool = docker.types.IPAMPool(subnet=addDetail['subnet'], gateway=addDetail['gateway'])
					ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])

				newLabels = {}
				newOptions = {}
				if addDetail['options'][0]:
					for x in addDetail['options']: newOptions[x.split("=")[0]] = x.split("=")[1]
				if addDetail['labels'][0]:
					for x in addDetail['labels']: newLabels[x.split("=")[0]] = x.split("=")[1]

				return self.client.networks.create(labels = newLabels,
				                                   options=newOptions,
				                                   name = addDetail['name'],
				                                   driver = addDetail['driver'],
				                                   internal=eval(addDetail['internal']),
				                                   ipam=ipam_config if ipam_config else None,
				                                   enable_ipv6=eval(addDetail['enable_ipv6']),
				                                   check_duplicate = eval(addDetail['check_duplicate']),)

			elif opt == 'rm_network':
				for i in json.loads(dicts['rmList']): self.client.networks.get(i).remove()
				return "true"
		except docker.errors.APIError, e:
			return e
