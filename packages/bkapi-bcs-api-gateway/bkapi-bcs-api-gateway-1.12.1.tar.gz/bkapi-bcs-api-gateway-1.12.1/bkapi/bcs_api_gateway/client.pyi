# -*- coding: utf-8 -*-
from bkapi_client_core.apigateway import APIGatewayClient, Operation, OperationGroup


class Group(OperationGroup):

    @property
    def create_web_console_sessions(self) -> Operation:
        """
        bkapi resource create_web_console_sessions
        """

    @property
    def delete_chart(self) -> Operation:
        """
        bkapi resource delete_chart
        删除 chart
        """

    @property
    def delete_chart_version(self) -> Operation:
        """
        bkapi resource delete_chart_version
        删除 chart version
        """

    @property
    def get_chart_detail(self) -> Operation:
        """
        bkapi resource get_chart_detail
        获取 chart 详情
        """

    @property
    def get_chart_version_detail(self) -> Operation:
        """
        bkapi resource get_chart_version_detail
        获取 chart version 详情
        """

    @property
    def get_chart_versions(self) -> Operation:
        """
        bkapi resource get_chart_versions
        获取 chart versions 列表
        """

    @property
    def get_project(self) -> Operation:
        """
        bkapi resource get_project
        获取项目详情
        """

    @property
    def get_release_detail(self) -> Operation:
        """
        bkapi resource get_release_detail
        查询 release 详细信息
        """

    @property
    def get_release_history(self) -> Operation:
        """
        bkapi resource get_release_history
        获取 release 历史记录
        """

    @property
    def get_repo(self) -> Operation:
        """
        bkapi resource get_repo
        获取仓库列表
        """

    @property
    def install_release(self) -> Operation:
        """
        bkapi resource install_release
        安装 release
        """

    @property
    def label_values(self) -> Operation:
        """
        bkapi resource label_values
        查询label对应的values
        """

    @property
    def labels(self) -> Operation:
        """
        bkapi resource labels
        查询labels
        """

    @property
    def labels_by_post(self) -> Operation:
        """
        bkapi resource labels_by_post
        查询labels
        """

    @property
    def list_auth_projects(self) -> Operation:
        """
        bkapi resource list_auth_projects
        查询用户有权限的项目
        """

    @property
    def list_charts(self) -> Operation:
        """
        bkapi resource list_charts
        获取 charts 列表
        """

    @property
    def list_project_clusters(self) -> Operation:
        """
        bkapi resource list_project_clusters
        查询项目下的集群列表
        """

    @property
    def list_releases(self) -> Operation:
        """
        bkapi resource list_releases
        获取 release 列表
        """

    @property
    def list_repos(self) -> Operation:
        """
        bkapi resource list_repos
        获取仓库列表
        """

    @property
    def list_resource(self) -> Operation:
        """
        bkapi resource list_resource
        通过资源池ID查询资源列表
        """

    @property
    def list_resource_pool(self) -> Operation:
        """
        bkapi resource list_resource_pool
        获取资源池列表
        """

    @property
    def query(self) -> Operation:
        """
        bkapi resource query
        查询最新的时序数据
        """

    @property
    def query_by_post(self) -> Operation:
        """
        bkapi resource query_by_post
        查询最新的时序数据
        """

    @property
    def query_range(self) -> Operation:
        """
        bkapi resource query_range
        查询时间段的时序数据
        """

    @property
    def query_range_by_post(self) -> Operation:
        """
        bkapi resource query_range_by_post
        查询时间段的时序数据
        """

    @property
    def release_preview(self) -> Operation:
        """
        bkapi resource release_preview
        安装、升级、回滚时预览 release yaml
        """

    @property
    def rollback_release(self) -> Operation:
        """
        bkapi resource rollback_release
        回滚 release
        """

    @property
    def series(self) -> Operation:
        """
        bkapi resource series
        查询series
        """

    @property
    def series_by_post(self) -> Operation:
        """
        bkapi resource series_by_post
        查询series
        """

    @property
    def uninstall_release(self) -> Operation:
        """
        bkapi resource uninstall_release
        删除 release
        """

    @property
    def upgrade_release(self) -> Operation:
        """
        bkapi resource upgrade_release
        升级 release
        """


class Client(APIGatewayClient):
    """Bkapi bcs_api_gateway client"""

    @property
    def api(self) -> Group:
        """api resources"""
