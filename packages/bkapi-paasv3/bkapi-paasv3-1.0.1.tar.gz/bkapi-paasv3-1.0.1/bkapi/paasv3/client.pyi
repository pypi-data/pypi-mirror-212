# -*- coding: utf-8 -*-
from bkapi_client_core.apigateway import APIGatewayClient, Operation, OperationGroup


class Group(OperationGroup):

    @property
    def analysis_dimension_path(self) -> Operation:
        """
        访问统计：按路径维度查看
        """

    @property
    def analysis_dimension_user(self) -> Operation:
        """
        访问统计：按用户维度查看
        """

    @property
    def analysis_total(self) -> Operation:
        """
        访问统计: 站点访问总数
        """

    @property
    def batch_create_access_control_strategy(self) -> Operation:
        """
        
        """

    @property
    def create_light_applications(self) -> Operation:
        """
        创建轻应用
        """

    @property
    def delete_light_applications(self) -> Operation:
        """
        删除轻应用
        """

    @property
    def deploy_with_module(self) -> Operation:
        """
        App 部署（支持多模块）
        """

    @property
    def fetch_app_access_token(self) -> Operation:
        """
        获取代表指定应用和用户身份的 AccessToken
        """

    @property
    def get_deployment_result(self) -> Operation:
        """
        查询部署任务结果
        """

    @property
    def get_deployments_list(self) -> Operation:
        """
        获取 App 部署历史
        """

    @property
    def get_detailed_app_list(self) -> Operation:
        """
        获取 App 详细信息列表
        """

    @property
    def get_light_applications(self) -> Operation:
        """
        获取轻应用信息
        """

    @property
    def get_minimal_app_list(self) -> Operation:
        """
        获取 App 简明信息列表
        """

    @property
    def get_module_info(self) -> Operation:
        """
        查看应用模块信息
        """

    @property
    def get_offline_result(self) -> Operation:
        """
        查询下架任务结果
        """

    @property
    def get_resumable_offline_operations(self) -> Operation:
        """
        查询可恢复的下架操作
        """

    @property
    def list_app_modules(self) -> Operation:
        """
        查看应用下所有的模块
        """

    @property
    def list_bk_plugin_logs(self) -> Operation:
        """
        查询单个蓝鲸插件的日志
        """

    @property
    def list_bk_plugins(self) -> Operation:
        """
        查询平台上所有蓝鲸插件信息
        """

    @property
    def list_detailed_bk_plugins(self) -> Operation:
        """
        查询平台上所有蓝鲸插件信息（带详细部署信息）
        """

    @property
    def log_filters(self) -> Operation:
        """
        应用日志查询
        """

    @property
    def module_env_released_info(self) -> Operation:
        """
        查询应用模块环境部署信息
        """

    @property
    def module_env_released_state(self) -> Operation:
        """
        查询应用模块环境部署信息
        """

    @property
    def module_offline(self) -> Operation:
        """
        应用模块下架
        """

    @property
    def patch_light_applications(self) -> Operation:
        """
        修改轻应用
        """

    @property
    def refresh_app_access_token(self) -> Operation:
        """
        刷新代表指定应用和用户身份的 AccessToken
        """

    @property
    def request_apps_access_permission(self) -> Operation:
        """
        提交多个应用的访问申请单据和Tencent版平台的访问权限申请
        """

    @property
    def retrieve_bk_plugin(self) -> Operation:
        """
        查询单个蓝鲸插件详细信息
        """

    @property
    def streams_history_events(self) -> Operation:
        """
        获取部署日志流
        """

    @property
    def sys__api__lesscode__bind_db_service(self) -> Operation:
        """
        尝试绑定数据库增强服务
        """

    @property
    def sys__api__lesscode__query_db_credentials(self) -> Operation:
        """
        查询数据库增强服务的 credential 信息
        """

    @property
    def uni_apps_query_by_id(self) -> Operation:
        """
        根据应用 ID（Code）查询多平台应用信息
        """

    @property
    def upload_source_package(self) -> Operation:
        """
        上传源码包
        """

    @property
    def upload_source_package_via_link(self) -> Operation:
        """
        通过链接上传源码包
        """


class Client(APIGatewayClient):
    """paasv3
    蓝鲸 PaaS 平台 - 开发者中心
    """

    @property
    def api(self) -> Group:
        """api resources"""
