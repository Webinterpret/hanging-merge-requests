import json
import requests

import gitlab

from gitlab.exceptions import GitlabHttpError, GitlabListError

from hmr.formatters import format_payload
from hmr.models import ProjectWithMRs


class Repo:

    def __init__(self, gitlab_client: gitlab.Gitlab):
        self._gl = gitlab_client
        self._projects = None

    def projects_list(self):
        if self._projects is not None:
            return self._projects

        self._projects = []
        for project in self._gl.projects.list(all=True):
            self._projects.append(project)

        return self._projects

    def reset_projects(self):
        self._projects = None

    def get_project(self, project_path_with_namespace: str):
        for p in self.projects_list():
            if p.path_with_namespace == project_path_with_namespace:
                return p

    def get_pending_merge_requests(self, project_path_with_namespace: str):
        project = self.get_project(project_path_with_namespace)
        try:
            mrs = project.mergerequests.list(state='opened', order_by='updated_at', sort='desc', list=True)
        except (GitlabHttpError, GitlabListError):
            print(f'Insufficient privileges: {project.name}')
            mrs = []
        return mrs


def get_repo(gitlab_url: str, gitlab_private_token: str):
    if not hasattr(get_repo, '__client__'):
        # gl = gitlab.Gitlab.from_config('somewhere', ['/tmp/gl.cfg'])
        # https://python-gitlab.readthedocs.io/en/stable/cli.html#cli-configuration
        gl = gitlab.Gitlab(gitlab_url, private_token=gitlab_private_token)
        get_repo.__client__ = Repo(gl)
    return get_repo.__client__


def notify_about_hanging_merge_requests(config: dict, repo: Repo, slack_hook_url: str):
    channel = config.get('channel', None)
    if not channel:
        return

    team_projects_names = config.get('projects', ())

    projects = []
    for project in repo.projects_list():
        if project.path_with_namespace in team_projects_names:
            mrs = repo.get_pending_merge_requests(project.path_with_namespace)
            projects.append(ProjectWithMRs(project, mrs))

    payload = {
        'text': format_payload(projects),
        'username': 'Pending merge requests',
        'icon_emoji': ':gitlab:',
        'channel': channel,

    }

    if len(payload['text']) == 0:
        print(f'Payload for {channel} has zero-length')
        return

    print(f'Sending notification to {channel}:\n\n{payload}\n\n')
    requests.post(slack_hook_url, data={'payload': json.dumps(payload)})
