# -*- coding: utf-8 -*-
from bkapi_client_core.apigateway import APIGatewayClient, Operation, OperationGroup, bind_property


class Group(OperationGroup):
    # bkapi resource create_web_console_sessions
    create_web_console_sessions = bind_property(
        Operation,
        name="create_web_console_sessions",
        method="POST",
        path="/{version}/webconsole/api/portal/projects/{project_id_or_code}/clusters/{cluster_id}/web_console/sessions/",
    )

    # bkapi resource delete_chart
    # 删除 chart
    delete_chart = bind_property(
        Operation,
        name="delete_chart",
        method="DELETE",
        path="/helmmanager/v1/projects/{projectCode}/repos/{repoName}/charts/{name}",
    )

    # bkapi resource delete_chart_version
    # 删除 chart version
    delete_chart_version = bind_property(
        Operation,
        name="delete_chart_version",
        method="DELETE",
        path="/helmmanager/v1/projects/{projectCode}/repos/{repoName}/charts/{name}/versions/{version}",
    )

    # bkapi resource get_chart_detail
    # 获取 chart 详情
    get_chart_detail = bind_property(
        Operation,
        name="get_chart_detail",
        method="GET",
        path="/helmmanager/v1/projects/{projectCode}/repos/{repoName}/charts/{name}",
    )

    # bkapi resource get_chart_version_detail
    # 获取 chart version 详情
    get_chart_version_detail = bind_property(
        Operation,
        name="get_chart_version_detail",
        method="GET",
        path="/helmmanager/v1/projects/{projectCode}/repos/{repoName}/charts/{name}/versions/{version}",
    )

    # bkapi resource get_chart_versions
    # 获取 chart versions 列表
    get_chart_versions = bind_property(
        Operation,
        name="get_chart_versions",
        method="GET",
        path="/helmmanager/v1/projects/{projectCode}/repos/{repoName}/charts/{name}/versions",
    )

    # bkapi resource get_project
    # 获取项目详情
    get_project = bind_property(
        Operation,
        name="get_project",
        method="GET",
        path="/bcsproject/v1/projects/{projectIDOrCode}",
    )

    # bkapi resource get_release_detail
    # 查询 release 详细信息
    get_release_detail = bind_property(
        Operation,
        name="get_release_detail",
        method="GET",
        path="/helmmanager/v1/projects/{projectCode}/clusters/{clusterID}/namespaces/{namespace}/releases/{name}",
    )

    # bkapi resource get_release_history
    # 获取 release 历史记录
    get_release_history = bind_property(
        Operation,
        name="get_release_history",
        method="GET",
        path="/helmmanager/v1/projects/{projectCode}/clusters/{clusterID}/namespaces/{namespace}/releases/{name}/history",
    )

    # bkapi resource get_repo
    # 获取仓库列表
    get_repo = bind_property(
        Operation,
        name="get_repo",
        method="GET",
        path="/helmmanager/v1/projects/{projectCode}/repos/{name}",
    )

    # bkapi resource install_release
    # 安装 release
    install_release = bind_property(
        Operation,
        name="install_release",
        method="POST",
        path="/helmmanager/v1/projects/{projectCode}/clusters/{clusterID}/namespaces/{namespace}/releases/{name}",
    )

    # bkapi resource label_values
    # 查询label对应的values
    label_values = bind_property(
        Operation,
        name="label_values",
        method="GET",
        path="/{version}/monitor/query/api/v1/label/{name}/values",
    )

    # bkapi resource labels
    # 查询labels
    labels = bind_property(
        Operation,
        name="labels",
        method="GET",
        path="/{version}/monitor/query/api/v1/labels",
    )

    # bkapi resource labels_by_post
    # 查询labels
    labels_by_post = bind_property(
        Operation,
        name="labels_by_post",
        method="POST",
        path="/{version}/monitor/query/api/v1/labels",
    )

    # bkapi resource list_auth_projects
    # 查询用户有权限的项目
    list_auth_projects = bind_property(
        Operation,
        name="list_auth_projects",
        method="GET",
        path="/{version}/bcsproject/v1/authorized_projects",
    )

    # bkapi resource list_charts
    # 获取 charts 列表
    list_charts = bind_property(
        Operation,
        name="list_charts",
        method="GET",
        path="/helmmanager/v1/projects/{projectCode}/repos/{repoName}/charts",
    )

    # bkapi resource list_project_clusters
    # 查询项目下的集群列表
    list_project_clusters = bind_property(
        Operation,
        name="list_project_clusters",
        method="GET",
        path="/{version}/clustermanager/v1/cluster",
    )

    # bkapi resource list_releases
    # 获取 release 列表
    list_releases = bind_property(
        Operation,
        name="list_releases",
        method="GET",
        path="/helmmanager/v1/projects/{projectCode}/clusters/{clusterID}/releases",
    )

    # bkapi resource list_repos
    # 获取仓库列表
    list_repos = bind_property(
        Operation,
        name="list_repos",
        method="GET",
        path="/helmmanager/v1/projects/{projectCode}/repos",
    )

    # bkapi resource list_resource
    # 通过资源池ID查询资源列表
    list_resource = bind_property(
        Operation,
        name="list_resource",
        method="GET",
        path="/v4/resourcemanager/v1/resource_pools/{resource_pool_id}/resources",
    )

    # bkapi resource list_resource_pool
    # 获取资源池列表
    list_resource_pool = bind_property(
        Operation,
        name="list_resource_pool",
        method="GET",
        path="/v4/resourcemanager/v1/resource_pools",
    )

    # bkapi resource query
    # 查询最新的时序数据
    query = bind_property(
        Operation,
        name="query",
        method="GET",
        path="/{version}/monitor/query/api/v1/query",
    )

    # bkapi resource query_by_post
    # 查询最新的时序数据
    query_by_post = bind_property(
        Operation,
        name="query_by_post",
        method="POST",
        path="/{version}/monitor/query/api/v1/query",
    )

    # bkapi resource query_range
    # 查询时间段的时序数据
    query_range = bind_property(
        Operation,
        name="query_range",
        method="GET",
        path="/{version}/monitor/query/api/v1/query_range",
    )

    # bkapi resource query_range_by_post
    # 查询时间段的时序数据
    query_range_by_post = bind_property(
        Operation,
        name="query_range_by_post",
        method="POST",
        path="/{version}/monitor/query/api/v1/query_range",
    )

    # bkapi resource release_preview
    # 安装、升级、回滚时预览 release yaml
    release_preview = bind_property(
        Operation,
        name="release_preview",
        method="POST",
        path="/helmmanager/v1/projects/{projectCode}/clusters/{clusterID}/namespaces/{namespace}/releases/{name}/preview",
    )

    # bkapi resource rollback_release
    # 回滚 release
    rollback_release = bind_property(
        Operation,
        name="rollback_release",
        method="PUT",
        path="/helmmanager/v1/projects/{projectCode}/clusters/{clusterID}/namespaces/{namespace}/releases/{name}/rollback",
    )

    # bkapi resource series
    # 查询series
    series = bind_property(
        Operation,
        name="series",
        method="GET",
        path="/{version}/monitor/query/api/v1/series",
    )

    # bkapi resource series_by_post
    # 查询series
    series_by_post = bind_property(
        Operation,
        name="series_by_post",
        method="POST",
        path="/{version}/monitor/query/api/v1/series",
    )

    # bkapi resource uninstall_release
    # 删除 release
    uninstall_release = bind_property(
        Operation,
        name="uninstall_release",
        method="DELETE",
        path="/helmmanager/v1/projects/{projectCode}/clusters/{clusterID}/namespaces/{namespace}/releases/{name}",
    )

    # bkapi resource upgrade_release
    # 升级 release
    upgrade_release = bind_property(
        Operation,
        name="upgrade_release",
        method="PUT",
        path="/helmmanager/v1/projects/{projectCode}/clusters/{clusterID}/namespaces/{namespace}/releases/{name}",
    )


class Client(APIGatewayClient):
    """Bkapi bcs_api_gateway client"""
    _api_name = "bcs-api-gateway"

    api = bind_property(Group, name="api")
