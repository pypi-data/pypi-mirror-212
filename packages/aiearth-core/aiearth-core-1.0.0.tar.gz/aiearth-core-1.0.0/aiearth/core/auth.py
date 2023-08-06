#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from . import g_var
from .client import Endpoints
from .error import AIEError, AIEErrorCode
from datetime import datetime


class Authenticate(object):
    class ClientId(object):
        USER_STD = "user_std"
        ALIYUN_JUPYTER = "aliyun_jupyter"

    @staticmethod
    def getClientEnvironment():
        if os.getenv(g_var.JupyterEnv.TOKEN) is not None:
            return Authenticate.ClientId.ALIYUN_JUPYTER
        else:
            return Authenticate.ClientId.USER_STD

    @staticmethod
    def __displayAuthPromt():
        print("请将以下地址粘贴到Web浏览器中，访问授权页面，并将个人token粘贴到输入框中")
        print("\t", Endpoints.AUTH_PORTAL_PAGE)

    @staticmethod
    def __getTokenFromJupyter():
        token = os.getenv(g_var.JupyterEnv.TOKEN)
        if token is None:
            raise AIEError(AIEErrorCode.ENVIRONMENT_INIT_ERROR,
                           "云平台环境token获取失败")
        return token

    @staticmethod
    def auth(token=None, access_key_id=None, access_key_secret=None):
        client_id = Authenticate.getClientEnvironment()

        cred = {}
        cred["client_id"] = client_id
        if token is not None:
            cred["token"] = token
        elif access_key_id and access_key_secret:
            token = Authenticate.__get_token_by(access_key_id, access_key_secret)
            cred["token"] = token
        else:
            if client_id == Authenticate.ClientId.ALIYUN_JUPYTER:
                token = Authenticate.__getTokenFromJupyter()
                cred["token"] = token
            else:
                Authenticate.__displayAuthPromt()
                token = input("个人token: ")
                cred["token"] = token

        g_var.set_var(g_var.GVarKey.Authenticate.CLIENT_ID, cred["client_id"])
        g_var.set_var(g_var.GVarKey.Authenticate.TOKEN, cred["token"])

    @staticmethod
    def getCurrentUserToken():
        if not g_var.has_var(g_var.GVarKey.Authenticate.CLIENT_ID):
            raise AIEError(AIEErrorCode.ENVIRONMENT_INIT_ERROR,
                           "客户端ID获取失败，请先调用 aie.Authenticate() 进行授权")

        client_id = g_var.get_var(g_var.GVarKey.Authenticate.CLIENT_ID)
        token = ""
        if client_id == Authenticate.ClientId.ALIYUN_JUPYTER:
            token = Authenticate.__getTokenFromJupyter()
        else:
            if not g_var.has_var(g_var.GVarKey.Authenticate.TOKEN):
                raise AIEError(AIEErrorCode.ENVIRONMENT_INIT_ERROR,
                               "个人token获取失败，请先调用 aie.Authenticate() 进行授权")
            token = g_var.get_var(g_var.GVarKey.Authenticate.TOKEN)
        return token

    @staticmethod
    def __get_token_by(access_key_id, access_key_secret, force_create=False, expected_hours_before_expired=24):
        from alibabacloud_tea_openapi import models
        from alibabacloud_aiearth_engine20220609.client import Client
        from alibabacloud_aiearth_engine20220609.models import GetUserTokenRequest
        from alibabacloud_aiearth_engine20220609.models import GetUserTokenResponse
        config = models.Config(
            access_key_id=access_key_id, access_key_secret=access_key_secret,
            region_id=Endpoints.OPENAPI_REGION_ID, endpoint=Endpoints.OPENAPI_ENDPOINT)

        client = Client(config)

        get_user_token = GetUserTokenRequest()
        get_user_token.force_create = force_create
        get_user_token_resp: GetUserTokenResponse = client.get_user_token(get_user_token)
        token = get_user_token_resp.body.token
        expired_at_ts = get_user_token_resp.body.expired_at / 1000.

        current_ts = datetime.now().timestamp()
        if expired_at_ts - current_ts < expected_hours_before_expired * 3600.:
            get_user_token = GetUserTokenRequest()
            get_user_token.force_create = True
            get_user_token_resp: GetUserTokenResponse = client.get_user_token(get_user_token)
            return get_user_token_resp.body.token
        else:
            return token
