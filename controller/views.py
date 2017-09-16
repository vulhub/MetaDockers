#coding:utf-8

import json
from controller.lib import localDetect
from django.views.decorators.csrf import csrf_exempt
from controller.lib.vulhubs import vulhubOperation as vo
from controller.lib.dockerOperation import dockerOperation as dco
from django.shortcuts import render, HttpResponse, render_to_response


def not_found():
	return render_to_response('404.html')


def server_error():
	return render_to_response('500.html')


def detectConf(func):
	def detechild(request):
		if dco().docker_switch_init() == False:
			return HttpResponse("/MetaDockers/controller/lib/config.conf error!")
		else:
			return func(request)
	return detechild


@detectConf
def indexRouting(request):
	index_attrs = {'images_num': "{}/{}".format(dco().get_docker_images_num('sum'), dco().get_docker_info('all')['Images']),
	               'images_size': dco().get_docker_images_num('size'),
	               'networks_sum': dco().get_docker_networks('sum'),
	               'volumes_sum': dco().get_docker_volumes('sum'),
	               'base_info': dco().get_docker_info('base')}
	return render(request, 'index.html', index_attrs)


@detectConf
def vulhubRouting(request):
	return render(request, 'vulhubs.html', {'vulhubs': vo().detection_local_vulhub_struct()})


@csrf_exempt
@detectConf
def imageRouting(request):
	if request.method == 'POST':
		images_oper = dco().image_operation(request.POST)
		return HttpResponse(images_oper)
	else:
		return render(request, 'images.html', {'images': json.dumps(dco().get_docker_images())})


@csrf_exempt
@detectConf
def volumeRouting(request):
	if request.method == 'POST':
		volume_oper = dco().volume_operation(request.POST)
		return HttpResponse(volume_oper)
	else:
		return render(request, 'volumes.html', {'volumes': json.dumps(dco().get_docker_volumes('detail'))})


@csrf_exempt
@detectConf
def containerRouting(request):
	req_path = request.path_info[1:]

	if req_path == 'containers/':
		return render(request, 'containers.html', )

	elif req_path == 'containerDetail/':
		if request.method == 'POST':
			cs_oper = dco().container_operation(request.POST)
			return HttpResponse(cs_oper)
		else:
			return render(request, 'containerDetail.html', {'csDetail': json.dumps(dco().get_containers(csId=request.GET['csId']))})

	elif req_path == 'containerList/':
		return render(request, 'containerList.html', {'csList': json.dumps(dco().get_containers())})


@csrf_exempt
@detectConf
def networkRouting(request):
	req_path = request.path_info[1:]

	if req_path == 'networkDetail/':
		if request.method == 'POST':
			network_oper = dco().network_operation(request.POST)
			return HttpResponse(network_oper)
		else:
			return render(request, 'networkDetail.html', {'nwDetail': json.dumps(dco().get_docker_networks(nwId=request.GET['nwId']))})

	elif req_path == 'networkList/':
		if request.method == 'POST':
			network_oper = dco().network_operation(request.POST)
			return HttpResponse(network_oper)
		else:
			return render(request, 'networkList.html', {'networks': json.dumps(dco().get_docker_networks('all'))})

	elif req_path == 'networks/':
		return render(request, 'networks.html')


@detectConf
def infoRouting(request):
	return render(request, 'info.html', {'dc_info': json.dumps(dco().get_docker_info('all'))})


def aboutRouting(request):
	return render(request, 'about.html', {'vh_version': localDetect.get_vulhub_version()})


def testRouting(request):
	return render(request, 'test.html')