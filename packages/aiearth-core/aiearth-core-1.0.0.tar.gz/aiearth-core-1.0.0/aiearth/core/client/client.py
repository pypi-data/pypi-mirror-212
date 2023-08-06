#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

import requests
from ..error import AIEError, AIEErrorCode
from .. import g_var
from .. import auth
from .. import env

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BaseClient(object):
    @staticmethod
    def __append_extra_hdrs(hdrs):
        hdrs["x-aie-auth-token"] = auth.Authenticate.getCurrentUserToken()

        project_id = os.getenv(g_var.JupyterEnv.PROJECT_ID, "local")
        hdrs['x-aie-client-name'] = f"aie-sdk@Project-{project_id}"
        return hdrs

    @staticmethod
    def post(url, hdrs, data, append_extra_hdrs=True):
        if append_extra_hdrs:
            hdrs = BaseClient.__append_extra_hdrs(hdrs)

        if env.get_log_level() ==  g_var.LogLevel.DEBUG_LEVEL:
            print(
                f"BaseClient::post request. url: {url}, headers: {json.dumps(hdrs)}, data: {json.dumps(data)}")

        resp = requests.post(url=url, headers=hdrs, timeout=(600, 600),
                             json=data, verify=False)

        if resp.status_code != 200:
            if "401 Authorization Required" in resp.text:
                raise AIEError(AIEErrorCode.ENVIRONMENT_INIT_ERROR,
                               f"未授权或者个人token失效，请先调用 aie.Authenticate() 进行授权")
            else:
                raise AIEError(AIEErrorCode.DEFAULT_INTERNAL_ERROR,
                               "", f"http请求错误: {resp.text}")

        if env.get_log_level() ==  g_var.LogLevel.DEBUG_LEVEL:
            print(
                f"BaseClient::post response. url: {url}, response: {resp.json()}")

        return resp

    @staticmethod
    def get(url, hdrs, append_extra_hdrs=True):
        if append_extra_hdrs:
            hdrs = BaseClient.__append_extra_hdrs(hdrs)

        if env.get_log_level() ==  g_var.LogLevel.DEBUG_LEVEL:
            print(
                f"BaseClient::get request. url: {url}, headers: {json.dumps(hdrs)}")

        resp = requests.get(url=url, headers=hdrs,
                            timeout=(600, 600), verify=False)

        if resp.status_code != 200:
            if "401 Authorization Required" in resp.text:
                raise AIEError(AIEErrorCode.ENVIRONMENT_INIT_ERROR,
                               f"未授权或者个人token失效，请先调用 aie.Authenticate() 进行授权")
            else:
                raise AIEError(AIEErrorCode.DEFAULT_INTERNAL_ERROR,
                               "", f"http请求错误: {resp.text}")

        if env.get_log_level() ==  g_var.LogLevel.DEBUG_LEVEL:
            print(
                f"BaseClient::get response. url: {url}, response: {resp.json()}")

        return resp

    @staticmethod
    def delete(url, hdrs, append_extra_hdrs=True):
        if append_extra_hdrs:
            hdrs = BaseClient.__append_extra_hdrs(hdrs)

        if env.get_log_level() ==  g_var.LogLevel.DEBUG_LEVEL:
            print(
                f"BaseClient::delete request. url: {url}, headers: {json.dumps(hdrs)}")

        resp = requests.delete(url=url, headers=hdrs,
                               timeout=(600, 600), verify=False)

        if resp.status_code != 200:
            if "401 Authorization Required" in resp.text:
                raise AIEError(AIEErrorCode.ENVIRONMENT_INIT_ERROR,
                               f"未授权或者个人token失效，请先调用 aie.Authenticate() 进行授权")
            else:
                raise AIEError(AIEErrorCode.DEFAULT_INTERNAL_ERROR,
                               "", f"http请求错误: {resp.text}")

        if env.get_log_level() ==  g_var.LogLevel.DEBUG_LEVEL:
            print(
                f"BaseClient::delete response. url: {url}, response: {resp.json()}")

        return resp
