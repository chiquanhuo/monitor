#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from apps.monitor.models import Monitor, MonitorForm
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from utils.apps.base import cover_device_lower
from config.settings import *
from utils.db.mongo import *
from utils.pagehelper import list_by_page
from django.contrib.auth.decorators import permission_required
import sys
from json import *

reload(sys)
sys.setdefaultencoding("utf-8")

@permission_required('monitor.change_monitor')
def index(request):
    "monitor list"
    data = {}
    debug_data = ""
    monitors = Monitor.objects.all().order_by("-create_at")
    data["monitors"] = monitors

    mongodb = GenMongo(MONGO_HOST, MONGO_PORT)
    if not mongodb:
        data["debug_data"] = debug_data

    collection = mongodb.get_collection(MONGO_DBNAME, MONGO_COLLECTION)
    if not collection:
        data["debug_data"] = ""

    search_dict = {}
    product = request.GET.get("product", None)
    if product:
        search_dict["product"] = product

    aid = request.GET.get("aid", None)
    if aid:
        search_dict["aid"] = aid
        data['aid'] = aid

    ifa = request.GET.get("ifa", None)
    if ifa:
        ifa = cover_device_lower(ifa)
        search_dict["ifa"] = ifa
        data['ifa'] = ifa

    ei = request.GET.get("ei", None)
    if ei:
        search_dict["ei"] = ei
        data['ei'] = ei


    if not search_dict:
        search_dict["product"] = 2
        if len(monitors) > 0:
            try:
                params = eval(monitors[0].params)
            except:
                params = {}
            data["params"] = params
            search_dict.update(params)

    debug_data = collection.find(search_dict)
    debug_list = []

    # 判断spotid不为空
    spotid = request.GET.get('spotid', None)
    if spotid:
        data['spotid'] = spotid
        for item in debug_data:
            if spotid in str(item):
                debug_list.append(item)
    else:
        for item in debug_data:
            debug_list.append(item)

    debug_data = list_by_page(request, debug_list)

    data["debug_data"] = debug_data
    data["search_dict"] = search_dict

    return render_to_response(
        "monitor/index.html",
        data,
        context_instance=RequestContext(request)
    )


@permission_required('monitor.change_monitor')
def edit(request):
    data = {}
    id = request.GET.get("id", None)
    monitors = Monitor.objects.all().order_by('create_at')
    data['count'] = len(monitors)
    print monitors
    data['monitors'] = monitors
    monitor = None
    params = {}
    if id:
        id = int(id)
        monitor = get_object_or_404(Monitor, id=id)
        params = eval(monitor.params)
        data["params"] = params
        if "ifa" in params:
            data["ifa"] = ifa

        if "ei" in params:
            data["ei"] = ei

        if "aid" in params:
            data["aid"] = aid

        data["id"] = id

    if request.method == "POST":
        post = request.POST.copy()
        create_time = datetime.now()

        if monitor:
            create_time = monitor.create_time
            params = eval(monitor.params)

        product = post.get("product", None)
        if int(product) != 2:
            form = MonitorForm(post)
            data["form"] = form
            return render_to_response(
                "monitor/edit.html",
                data,
                context_instance=RequestContext(request)
            )

        ## 判断params字段的值 
        params = {}
        ifa = post.get("ifa", None)
        if ifa:
            ifa = cover_device_lower(ifa)
            if ifa:
                params["ifa"] = str(ifa)

        ei = post.get("ei", None)
        if ei:
            params["ei"] = str(ei)

        aid = post.get("aid", None)
        if aid:
            params["aid"] = str(aid)

        if not params:
            form = MonitorForm(post)
            data["form"] = form
            return render_to_response(
                "monitor/edit.html",
                data,
                context_instance=RequestContext(request)
            )

        params = JSONEncoder().encode(params)
        params = str(params)
        if not monitor:
            monitor = Monitor()
        monitor.params = params
        monitor.product = product
        monitor.create_time = create_time

        ## 判断是否已经存在数据
        is_monitors = Monitor.objects.filter(params=params).filter(product=product)
        if not is_monitors:
            monitor.save()
        return HttpResponseRedirect(
            '/monitor/'
        )

    else:
        form = MonitorForm()
        data['form'] = form
        return render_to_response(
            'monitor/edit.html',
            data,
            context_instance=RequestContext(request)
        )
