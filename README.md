Hanging Merge Requests
======================

![Languages](https://img.shields.io/github/languages/top/Webinterpret/hanging-merge-requests.svg)

Emojiful daily summaries of open merge requests directly in your Slack.

![Example summary](docs/demo.png?raw=true "Example summary")

Create you own configuration file with your team, channel and projects as shown in [example_config.json](example_config.json).

- :thumbsup: / :thumbsdown: - Has upvotes / downvotes
- :male_zombie: / :female_zombie: - MR is old
- :thought_balloon: - Has an ongoing discussion
- :ship: - Has more upvotes than downvotes, tests pass and is ready to be merged
- :white_check_mark: / :no_entry: - Can be merged / Cannot be merged
- :green_heart: / :broken_heart: - Tests pass / fails

Installation
------------

    git clone https://github.com/Webinterpret/hanging-merge-requests.git
    cd hanging-merge-requests && pip install -e .
  
Usage
-----

    send-notifications --config-path ../config.json --slack-hook-url $SLACK_HOOK_URL --gitlab-url $GITLAB_URL --gitlab-private-token $GITLAB_PRIVATE_TOKEN --team $TEAM
