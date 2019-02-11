import argparse
from hmr.main import get_repo
from hmr import config
from hmr.main import notify_about_hanging_merge_requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-path', required=True)
    parser.add_argument('--gitlab-url', required=True)
    parser.add_argument('--gitlab-private-token', required=True)
    parser.add_argument('--slack-hook-url', required=True)
    parser.add_argument('--team', nargs='+', required=False)
    args = parser.parse_args()

    repo = get_repo(args.gitlab_url, args.gitlab_private_token)
    cfg = config.read(args.config_path)
    teams = cfg.keys()

    if args.team:
        teams = list(set(args.team) & set(teams))

    print(f'Teams to be notified: {", ".join(teams)}')

    for team in teams:
        try:
            notify_about_hanging_merge_requests(cfg[team], repo, args.slack_hook_url)
        except Exception as e:
            print(f'{team} - {e}')
