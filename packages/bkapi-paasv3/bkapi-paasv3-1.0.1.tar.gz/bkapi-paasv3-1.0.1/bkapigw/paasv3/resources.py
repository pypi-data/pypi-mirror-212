# -*- coding: utf-8 -*-
from .base import RequestAPI


class CollectionsAPI(object):
    def __init__(self, client):
        from . import conf

        self.client = client
        self.host = "" or conf.HOST.format(api_name="paasv3")

        self.get_detailed_app_list = RequestAPI(client=self.client, method="GET", host=self.host, path="/bkapps/applications/lists/detailed")

        self.get_minimal_app_list = RequestAPI(client=self.client, method="GET", host=self.host, path="/bkapps/applications/lists/minimal")

        self.request_apps_access_permission = RequestAPI(client=self.client, method="POST", host=self.host, path="/bkapps/access_control/multi_apply_record/")

        self.batch_create_access_control_strategy = RequestAPI(client=self.client, method="POST", host=self.host, path="/bkapps/applications/{app_code}/access_control/restriction_type/{restriction_type}/strategy/")

        self.get_light_applications = RequestAPI(client=self.client, method="GET", host=self.host, path="/system/light-applications")

        self.create_light_applications = RequestAPI(client=self.client, method="POST", host=self.host, path="/system/light-applications")

        self.delete_light_applications = RequestAPI(client=self.client, method="DELETE", host=self.host, path="/system/light-applications")

        self.patch_light_applications = RequestAPI(client=self.client, method="PATCH", host=self.host, path="/system/light-applications")

        self.uni_apps_query_by_id = RequestAPI(client=self.client, method="GET", host=self.host, path="/system/uni_applications/query/by_id/")

        self.analysis_dimension_path = RequestAPI(client=self.client, method="GET", host=self.host, path="/bkapps/applications/{app_code}/modules/{module}/envs/{env}/analysis/m/{source_type}/metrics/dimension/path")

        self.deploy_with_module = RequestAPI(client=self.client, method="POST", host=self.host, path="/bkapps/applications/{app_code}/modules/{module}/envs/{env}/deployments/")

        self.get_deployment_result = RequestAPI(client=self.client, method="GET", host=self.host, path="/bkapps/applications/{app_code}/modules/{module}/deployments/{deployment_id}/result/")

        self.get_deployments_list = RequestAPI(client=self.client, method="GET", host=self.host, path="/bkapps/applications/{app_code}/modules/{module}/deployments/lists/")

        self.streams_history_events = RequestAPI(client=self.client, method="GET", host=self.host, path="/streams/{channel_id}/history_events")

        self.upload_source_package_via_link = RequestAPI(client=self.client, method="POST", host=self.host, path="/bkapps/applications/{app_code}/modules/{module}/source_package/link/")

        self.upload_source_package = RequestAPI(client=self.client, method="POST", host=self.host, path="/bkapps/applications/{app_code}/modules/{module}/source_package/")

        self.list_app_modules = RequestAPI(client=self.client, method="GET", host=self.host, path="/bkapps/applications/{app_code}/modules/")

        self.module_env_released_info = RequestAPI(client=self.client, method="GET", host=self.host, path="/bkapps/applications/{code}/modules/{module_name}/envs/{environment}/released_info/")

        self.module_offline = RequestAPI(client=self.client, method="POST", host=self.host, path="/bkapps/applications/{app_code}/modules/{module}/envs/{env}/offlines/")

        self.get_offline_result = RequestAPI(client=self.client, method="GET", host=self.host, path="/bkapps/applications/{app_code}/modules/{module}/offlines/{offline_operation_id}/result/")

        self.get_module_info = RequestAPI(client=self.client, method="GET", host=self.host, path="/bkapps/applications/{app_code}/modules/{module}/")

        self.get_resumable_offline_operations = RequestAPI(client=self.client, method="GET", host=self.host, path="/bkapps/applications/{app_code}/modules/{module}/envs/{env}/offlines/resumable/")

        self.fetch_app_access_token = RequestAPI(client=self.client, method="GET", host=self.host, path="/bkapps/applications/{app_code}/oauth/token/{api_gateway_env}/")

        self.module_env_released_state = RequestAPI(client=self.client, method="GET", host=self.host, path="/bkapps/applications/{code}/modules/{module_name}/envs/{environment}/released_state/")

        self.refresh_app_access_token = RequestAPI(client=self.client, method="POST", host=self.host, path="/bkapps/applications/{app_code}/oauth/token/{api_gateway_env}/refresh")

        self.analysis_dimension_user = RequestAPI(client=self.client, method="GET", host=self.host, path="/bkapps/applications/{app_code}/modules/{module}/envs/{env}/analysis/m/{source_type}/metrics/dimension/user")

        self.analysis_total = RequestAPI(client=self.client, method="GET", host=self.host, path="/bkapps/applications/{app_code}/modules/{module}/envs/{env}/analysis/m/{source_type}/metrics/total")

        self.list_bk_plugins = RequestAPI(client=self.client, method="GET", host=self.host, path="/system/bk_plugins/")

        self.retrieve_bk_plugin = RequestAPI(client=self.client, method="GET", host=self.host, path="/system/bk_plugins/{code}/")

        self.list_bk_plugin_logs = RequestAPI(client=self.client, method="GET", host=self.host, path="/system/bk_plugins/{code}/logs/")

        self.sys__api__lesscode__query_db_credentials = RequestAPI(client=self.client, method="GET", host=self.host, path="/system/bkapps/applications/{app_code}/modules/{module}/envs/{env}/lesscode/query_db_credentials")

        self.sys__api__lesscode__bind_db_service = RequestAPI(client=self.client, method="POST", host=self.host, path="/system/bkapps/applications/{app_code}/modules/{module}/lesscode/bind_db_service")

        self.list_detailed_bk_plugins = RequestAPI(client=self.client, method="GET", host=self.host, path="/system/bk_plugins/batch/detailed/")

        self.log_filters = RequestAPI(client=self.client, method="GET", host=self.host, path="/bkapps/applications/{code}/modules/{module_name}/log/filters/")
