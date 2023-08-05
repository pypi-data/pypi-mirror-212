# -*- coding: utf-8 -*-
from .base import RequestAPI


class CollectionsAPI(object):
    def __init__(self, client):
        from . import conf

        self.client = client
        self.host = conf.HOST.format(api_name="bcs-api-gateway")

        self.get_release_detail = RequestAPI(client=self.client, method="GET", host=self.host, path="/helmmanager/v1/projects/{projectCode}/clusters/{clusterID}/namespaces/{namespace}/releases/{name}")

        self.list_auth_projects = RequestAPI(client=self.client, method="GET", host=self.host, path="/{version}/bcsproject/v1/authorized_projects")

        self.list_project_clusters = RequestAPI(client=self.client, method="GET", host=self.host, path="/{version}/clustermanager/v1/cluster")

        self.create_web_console_sessions = RequestAPI(client=self.client, method="POST", host=self.host, path="/{version}/webconsole/api/portal/projects/{project_id_or_code}/clusters/{cluster_id}/web_console/sessions/")

        self.list_resource_pool = RequestAPI(client=self.client, method="GET", host=self.host, path="/v4/resourcemanager/v1/resource_pools")

        self.list_resource = RequestAPI(client=self.client, method="GET", host=self.host, path="/v4/resourcemanager/v1/resource_pools/{resource_pool_id}/resources")

        self.label_values = RequestAPI(client=self.client, method="GET", host=self.host, path="/{version}/monitor/query/api/v1/label/{name}/values")

        self.labels = RequestAPI(client=self.client, method="GET", host=self.host, path="/{version}/monitor/query/api/v1/labels")

        self.labels_by_post = RequestAPI(client=self.client, method="POST", host=self.host, path="/{version}/monitor/query/api/v1/labels")

        self.query = RequestAPI(client=self.client, method="GET", host=self.host, path="/{version}/monitor/query/api/v1/query")

        self.query_by_post = RequestAPI(client=self.client, method="POST", host=self.host, path="/{version}/monitor/query/api/v1/query")

        self.query_range = RequestAPI(client=self.client, method="GET", host=self.host, path="/{version}/monitor/query/api/v1/query_range")

        self.query_range_by_post = RequestAPI(client=self.client, method="POST", host=self.host, path="/{version}/monitor/query/api/v1/query_range")

        self.series = RequestAPI(client=self.client, method="GET", host=self.host, path="/{version}/monitor/query/api/v1/series")

        self.series_by_post = RequestAPI(client=self.client, method="POST", host=self.host, path="/{version}/monitor/query/api/v1/series")

        self.uninstall_release = RequestAPI(client=self.client, method="DELETE", host=self.host, path="/helmmanager/v1/projects/{projectCode}/clusters/{clusterID}/namespaces/{namespace}/releases/{name}")

        self.install_release = RequestAPI(client=self.client, method="POST", host=self.host, path="/helmmanager/v1/projects/{projectCode}/clusters/{clusterID}/namespaces/{namespace}/releases/{name}")

        self.upgrade_release = RequestAPI(client=self.client, method="PUT", host=self.host, path="/helmmanager/v1/projects/{projectCode}/clusters/{clusterID}/namespaces/{namespace}/releases/{name}")

        self.get_release_history = RequestAPI(client=self.client, method="GET", host=self.host, path="/helmmanager/v1/projects/{projectCode}/clusters/{clusterID}/namespaces/{namespace}/releases/{name}/history")

        self.release_preview = RequestAPI(client=self.client, method="POST", host=self.host, path="/helmmanager/v1/projects/{projectCode}/clusters/{clusterID}/namespaces/{namespace}/releases/{name}/preview")

        self.rollback_release = RequestAPI(client=self.client, method="PUT", host=self.host, path="/helmmanager/v1/projects/{projectCode}/clusters/{clusterID}/namespaces/{namespace}/releases/{name}/rollback")

        self.list_releases = RequestAPI(client=self.client, method="GET", host=self.host, path="/helmmanager/v1/projects/{projectCode}/clusters/{clusterID}/releases")

        self.list_repos = RequestAPI(client=self.client, method="GET", host=self.host, path="/helmmanager/v1/projects/{projectCode}/repos")

        self.list_charts = RequestAPI(client=self.client, method="GET", host=self.host, path="/helmmanager/v1/projects/{projectCode}/repos/{repoName}/charts")

        self.get_chart_detail = RequestAPI(client=self.client, method="GET", host=self.host, path="/helmmanager/v1/projects/{projectCode}/repos/{repoName}/charts/{name}")

        self.delete_chart = RequestAPI(client=self.client, method="DELETE", host=self.host, path="/helmmanager/v1/projects/{projectCode}/repos/{repoName}/charts/{name}")

        self.get_chart_versions = RequestAPI(client=self.client, method="GET", host=self.host, path="/helmmanager/v1/projects/{projectCode}/repos/{repoName}/charts/{name}/versions")

        self.get_chart_version_detail = RequestAPI(client=self.client, method="GET", host=self.host, path="/helmmanager/v1/projects/{projectCode}/repos/{repoName}/charts/{name}/versions/{version}")

        self.delete_chart_version = RequestAPI(client=self.client, method="DELETE", host=self.host, path="/helmmanager/v1/projects/{projectCode}/repos/{repoName}/charts/{name}/versions/{version}")

        self.get_project = RequestAPI(client=self.client, method="GET", host=self.host, path="/bcsproject/v1/projects/{projectIDOrCode}")

        self.get_repo = RequestAPI(client=self.client, method="GET", host=self.host, path="/helmmanager/v1/projects/{projectCode}/repos/{name}")
