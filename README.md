# MetaDockers

> Vulhub Team做为以收集/制作docker漏洞靶场为基础，并发展Docker相关的开发，MetaDockers用于管理vulhub以及自实现的Docker可视化。build ing...

> [vulhub](https://github.com/vulhub/vulhub) - Some Docker-Compose files for vulnerabilities environment

![](https://img.shields.io/badge/python-2.7-green.svg)
![](https://img.shields.io/badge/django-1.1-blue.svg)

## setting：
> 配置vulhub path和docker api开关，docker若启动且加入环境变量那么默认即可docker.from_env()：
MetaDockers/controller/lib/config.conf

sudo pip install -r requirements.txt

cd MetaDockers/

python manage.py runserver 8000

## Index:
![](https://blog-1252048719.cos.ap-shanghai.myqcloud.com/gerggf.png)
## Vulhubs:
> 可以加个启动项，并把每个靶场分配README。

![](https://blog-1252048719.cos.ap-shanghai.myqcloud.com/dsfwqe221.png)
## Images:
![](https://blog-1252048719.cos.ap-shanghai.myqcloud.com/regregeh.png)
> 完整的images启动参数有50多个，可以按需添加：[api文档](http://docker-py.readthedocs.io/en/stable/containers.html)（涉及controller/lib/dockerOperation.py的image_operation函数和templates/images.html的$(".btn-run").click）。

![](https://blog-1252048719.cos.ap-shanghai.myqcloud.com/3rvyjar.png)
## Networks:
![](https://blog-1252048719.cos.ap-shanghai.myqcloud.com/43tyo8dsf.png)

> 可增加/删除Networks：

![](https://blog-1252048719.cos.ap-shanghai.myqcloud.com/thth.png)

![](https://blog-1252048719.cos.ap-shanghai.myqcloud.com/ewtewr.png)
## Volumes:
![](https://blog-1252048719.cos.ap-shanghai.myqcloud.com/32r32r3r2.png)

> 可增加/删除volumes：

![](https://blog-1252048719.cos.ap-shanghai.myqcloud.com/rwiubsdf.png)
## Containers:

> 这个Containers才是重点，解决了在使用Container时的几个常见问题，比如因child导致kill不掉等。

![](https://blog-1252048719.cos.ap-shanghai.myqcloud.com/dsfwwefrew4.png)

> 正经的功能都有，还可直接跳转到映射的端口地址，其他功能可以摸索下：

![](https://blog-1252048719.cos.ap-shanghai.myqcloud.com/sadbkyuasd.png)

> 该Container的Log：

![](https://blog-1252048719.cos.ap-shanghai.myqcloud.com/wg7vyksdf.png)

> 该Container的Info：

![](https://blog-1252048719.cos.ap-shanghai.myqcloud.com/3qrg7iqw.png)
## Docker Info:

> 层叠太多，直接用的json view，可以浏览器ctrl+f。

![](https://blog-1252048719.cos.ap-shanghai.myqcloud.com/3rb78sdfk.png)


