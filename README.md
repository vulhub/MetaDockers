# MetaDockers

> Docker与vulhub可视化，build ing...
> [vulhub](https://github.com/vulhub/vulhub) - Some Docker-Compose files for vulnerabilities environment

![](http://shields.hust.cc/Python-v2.7-blue.svg)
![](http://progressed.io/bar/80?scale=100&title=build)
![](http://shields.hust.cc/Django-1.10-blue.svg)

## setting：
> 配置vulhub path和docker api开关，docker若启动且加入环境变量那么默认即可docker.from_env()：
MetaDockers/controller/lib/config.conf

sudo pip install -r requirements.txt

cd MetaDockers/

python manage.py runserver 8000

## Index:
![](http://7xiw31.com1.z0.glb.clouddn.com/gerggf.png)
## Vulhubs:
> 这个启动项没写，后期会直接拆分docker-compose包融合进去，还有各个靶场的README未分配。

![](http://7xiw31.com1.z0.glb.clouddn.com/dsfwqe221.png)
## Images:
![](http://7xiw31.com1.z0.glb.clouddn.com/regregeh.png)
> 还有这个images的启动参数有50多个。。。挨个测试心态炸了，好心人可以按[api文档](http://docker-py.readthedocs.io/en/stable/containers.html)加下哈哈（涉及controller/lib/dockerOperation.py的image_operation函数和templates/images.html的$(".btn-run").click），没人的话有空我也会加上：

![](http://7xiw31.com1.z0.glb.clouddn.com/3rvyjar.png)
## Networks:
![](http://7xiw31.com1.z0.glb.clouddn.com/43tyo8dsf.png)

> 可增加删除Networks：

![](http://7xiw31.com1.z0.glb.clouddn.com/thth.png)

![](http://7xiw31.com1.z0.glb.clouddn.com/ewtewr.png)
## Volumes:
![](http://7xiw31.com1.z0.glb.clouddn.com/32r32r3r2.png)

> 可增加删除volumes：

![](http://7xiw31.com1.z0.glb.clouddn.com/rwiubsdf.png)
## Containers:

> 这个Containers才是重点，解决了在使用Container时的几个常见问题，比如因child导致kill不掉等。

![](http://7xiw31.com1.z0.glb.clouddn.com/dsfwwefrew4.png)

> 正经的功能都有，还可直接跳转到映射的端口地址，其他功能可以摸索下：

![](http://7xiw31.com1.z0.glb.clouddn.com/sadbkyuasd.png)

> 该Container的Log：

![](http://7xiw31.com1.z0.glb.clouddn.com/wg7vyksdf.png)

> 该Container的Info：

![](http://7xiw31.com1.z0.glb.clouddn.com/3qrg7iqw.png)
## Docker Info:

> 层叠太多了，直接用的json view，浏览器ctrl+f吧2333.

![](http://7xiw31.com1.z0.glb.clouddn.com/3rb78sdfk.png)


