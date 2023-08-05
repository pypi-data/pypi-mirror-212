# -*- coding: utf-8 -*-
from bkapi_client_core.apigateway import APIGatewayClient, Operation, OperationGroup, bind_property


class Group(OperationGroup):
    # 访问统计：按路径维度查看
    analysis_dimension_path = bind_property(
        Operation, name="analysis_dimension_path", method="GET",
        path="/bkapps/applications/{app_code}/modules/{module}/envs/{env}/analysis/m/{source_type}/metrics/dimension/path",
    )

    # 访问统计：按用户维度查看
    analysis_dimension_user = bind_property(
        Operation, name="analysis_dimension_user", method="GET",
        path="/bkapps/applications/{app_code}/modules/{module}/envs/{env}/analysis/m/{source_type}/metrics/dimension/user",
    )

    # 访问统计: 站点访问总数
    analysis_total = bind_property(
        Operation, name="analysis_total", method="GET",
        path="/bkapps/applications/{app_code}/modules/{module}/envs/{env}/analysis/m/{source_type}/metrics/total",
    )

    batch_create_access_control_strategy = bind_property(
        Operation, name="batch_create_access_control_strategy", method="POST",
        path="/bkapps/applications/{app_code}/access_control/restriction_type/{restriction_type}/strategy/",
    )

    # 创建轻应用
    create_light_applications = bind_property(
        Operation, name="create_light_applications", method="POST",
        path="/system/light-applications",
    )

    # 删除轻应用
    delete_light_applications = bind_property(
        Operation, name="delete_light_applications", method="DELETE",
        path="/system/light-applications",
    )

    # App 部署（支持多模块）
    deploy_with_module = bind_property(
        Operation, name="deploy_with_module", method="POST",
        path="/bkapps/applications/{app_code}/modules/{module}/envs/{env}/deployments/",
    )

    # 获取代表指定应用和用户身份的 AccessToken
    fetch_app_access_token = bind_property(
        Operation, name="fetch_app_access_token", method="GET",
        path="/bkapps/applications/{app_code}/oauth/token/{api_gateway_env}/",
    )

    # 查询部署任务结果
    get_deployment_result = bind_property(
        Operation, name="get_deployment_result", method="GET",
        path="/bkapps/applications/{app_code}/modules/{module}/deployments/{deployment_id}/result/",
    )

    # 获取 App 部署历史
    get_deployments_list = bind_property(
        Operation, name="get_deployments_list", method="GET",
        path="/bkapps/applications/{app_code}/modules/{module}/deployments/lists/",
    )

    # 获取 App 详细信息列表
    get_detailed_app_list = bind_property(
        Operation, name="get_detailed_app_list", method="GET",
        path="/bkapps/applications/lists/detailed",
    )

    # 获取轻应用信息
    get_light_applications = bind_property(
        Operation, name="get_light_applications", method="GET",
        path="/system/light-applications",
    )

    # 获取 App 简明信息列表
    get_minimal_app_list = bind_property(
        Operation, name="get_minimal_app_list", method="GET",
        path="/bkapps/applications/lists/minimal",
    )

    # 查看应用模块信息
    get_module_info = bind_property(
        Operation, name="get_module_info", method="GET",
        path="/bkapps/applications/{app_code}/modules/{module}/",
    )

    # 查询下架任务结果
    get_offline_result = bind_property(
        Operation, name="get_offline_result", method="GET",
        path="/bkapps/applications/{app_code}/modules/{module}/offlines/{offline_operation_id}/result/",
    )

    # 查询可恢复的下架操作
    get_resumable_offline_operations = bind_property(
        Operation, name="get_resumable_offline_operations", method="GET",
        path="/bkapps/applications/{app_code}/modules/{module}/envs/{env}/offlines/resumable/",
    )

    # 查看应用下所有的模块
    list_app_modules = bind_property(
        Operation, name="list_app_modules", method="GET",
        path="/bkapps/applications/{app_code}/modules/",
    )

    # 查询单个蓝鲸插件的日志
    list_bk_plugin_logs = bind_property(
        Operation, name="list_bk_plugin_logs", method="GET",
        path="/system/bk_plugins/{code}/logs/",
    )

    # 查询平台上所有蓝鲸插件信息
    list_bk_plugins = bind_property(
        Operation, name="list_bk_plugins", method="GET",
        path="/system/bk_plugins/",
    )

    # 查询平台上所有蓝鲸插件信息（带详细部署信息）
    list_detailed_bk_plugins = bind_property(
        Operation, name="list_detailed_bk_plugins", method="GET",
        path="/system/bk_plugins/batch/detailed/",
    )

    # 应用日志查询
    log_filters = bind_property(
        Operation, name="log_filters", method="GET",
        path="/bkapps/applications/{code}/modules/{module_name}/log/filters/",
    )

    # 查询应用模块环境部署信息
    module_env_released_info = bind_property(
        Operation, name="module_env_released_info", method="GET",
        path="/bkapps/applications/{code}/modules/{module_name}/envs/{environment}/released_info/",
    )

    # 查询应用模块环境部署信息
    module_env_released_state = bind_property(
        Operation, name="module_env_released_state", method="GET",
        path="/bkapps/applications/{code}/modules/{module_name}/envs/{environment}/released_state/",
    )

    # 应用模块下架
    module_offline = bind_property(
        Operation, name="module_offline", method="POST",
        path="/bkapps/applications/{app_code}/modules/{module}/envs/{env}/offlines/",
    )

    # 修改轻应用
    patch_light_applications = bind_property(
        Operation, name="patch_light_applications", method="PATCH",
        path="/system/light-applications",
    )

    # 刷新代表指定应用和用户身份的 AccessToken
    refresh_app_access_token = bind_property(
        Operation, name="refresh_app_access_token", method="POST",
        path="/bkapps/applications/{app_code}/oauth/token/{api_gateway_env}/refresh",
    )

    # 提交多个应用的访问申请单据和Tencent版平台的访问权限申请
    request_apps_access_permission = bind_property(
        Operation, name="request_apps_access_permission", method="POST",
        path="/bkapps/access_control/multi_apply_record/",
    )

    # 查询单个蓝鲸插件详细信息
    retrieve_bk_plugin = bind_property(
        Operation, name="retrieve_bk_plugin", method="GET",
        path="/system/bk_plugins/{code}/",
    )

    # 获取部署日志流
    streams_history_events = bind_property(
        Operation, name="streams_history_events", method="GET",
        path="/streams/{channel_id}/history_events",
    )

    # 尝试绑定数据库增强服务
    sys__api__lesscode__bind_db_service = bind_property(
        Operation, name="sys__api__lesscode__bind_db_service", method="POST",
        path="/system/bkapps/applications/{app_code}/modules/{module}/lesscode/bind_db_service",
    )

    # 查询数据库增强服务的 credential 信息
    sys__api__lesscode__query_db_credentials = bind_property(
        Operation, name="sys__api__lesscode__query_db_credentials", method="GET",
        path="/system/bkapps/applications/{app_code}/modules/{module}/envs/{env}/lesscode/query_db_credentials",
    )

    # 根据应用 ID（Code）查询多平台应用信息
    uni_apps_query_by_id = bind_property(
        Operation, name="uni_apps_query_by_id", method="GET",
        path="/system/uni_applications/query/by_id/",
    )

    # 上传源码包
    upload_source_package = bind_property(
        Operation, name="upload_source_package", method="POST",
        path="/bkapps/applications/{app_code}/modules/{module}/source_package/",
    )

    # 通过链接上传源码包
    upload_source_package_via_link = bind_property(
        Operation, name="upload_source_package_via_link", method="POST",
        path="/bkapps/applications/{app_code}/modules/{module}/source_package/link/",
    )


class Client(APIGatewayClient):
    """paasv3
    蓝鲸 PaaS 平台 - 开发者中心
    """
    _api_name = "paasv3"

    api = bind_property(Group, name="api")
