import arrow
import humanize
import typing

from hmr.models import ProjectWithMRs

DAY = 24 * 3600


def format_project_header(project) -> str:
    return f'*{project.name}*'


def format_project(project, mrs) -> str:
    return f'{format_project_header(project)}\n\n{format_mrs(mrs)}\n' if mrs else ''


def format_mrs(mrs) -> str:
    return ''.join(format_mr(mr) for mr in mrs)


def link(url, text) -> str:
    return f'<{url}|*{text}*>'


def is_girl(name: str) -> bool:
    return len(name.split()) > 1 and name.split()[0].lower().endswith('a')


def votes_emoji(mr) -> str:
    if mr.downvotes:
        emoji = ':thumbsdown: '
    elif mr.upvotes:
        emoji = ':thumbsup: '
    else:
        emoji = ''
    return emoji


def discussion_emoji(mr) -> str:
    return ':thought_balloon: ' if mr.user_notes_count else ''


def merge_emoji(mr) -> str:
    if mr.merge_status == 'can_be_merged':
        emoji = ':white_check_mark:'
    elif mr.merge_status == 'cannot_be_merged':
        emoji = ':no_entry:'
    else:
        emoji = mr.merge_status
    return emoji


def pipeline_emoji(mr) -> str:
    pipelines = mr.pipelines()
    emoji = ''
    if pipelines:
        pipeline = pipelines[0]
        if pipeline['status'] == 'success':
            emoji = ':green_heart:'
        elif pipeline['status'] == 'failed':
            emoji = link(pipeline['web_url'], 'failed :broken_heart:')
        else:
            emoji = pipeline['status']
    return emoji


def zombie_emoji(mr) -> str:
    last_activity = arrow.get(mr.updated_at or mr.created_at)
    emoji = ':female_zombie: ' if is_girl(mr.author['name']) else ':male_zombie: '
    emoji = emoji if (arrow.get() - last_activity).total_seconds() > 10 * DAY else ''
    return emoji


def shipit_emoji(mr) -> str:
    return ':ship: ' if all((
        mr.upvotes > mr.downvotes,
        pipeline_emoji(mr) in (':green_heart:', ),
        merge_emoji(mr) in (':green_heart:', ),
    )) else ''


def format_mr(mr) -> str:
    lnk = link(mr.web_url, f'!{mr.iid} {mr.title}')
    last_activity = arrow.get(mr.updated_at or mr.created_at)
    return f'- {lnk} {shipit_emoji(mr)}{votes_emoji(mr)}{discussion_emoji(mr)}{zombie_emoji(mr)}(Merge status: {merge_emoji(mr)}; Tests: {pipeline_emoji(mr)}) by {mr.author["name"]} updated {last_activity.humanize()}\n'


def format_payload(projects: typing.List[ProjectWithMRs]) -> str:
    payload = ''
    deltas = []
    now = arrow.get()
    projects_count = 0
    for project_container in projects:
        project_payload = format_project(project_container.project, project_container.merge_requests)
        payload += project_payload

        if project_container.merge_requests:
            projects_count += 1

        for mr in project_container.merge_requests:
            deltas.append((now - arrow.get(mr.updated_at or mr.created_at)).total_seconds())

    if deltas:
        avg_time = sum(deltas) / len(deltas)
        payload += '\n'
        payload += f':stopwatch: {len(deltas)} MRs in {projects_count} projects; Average age {humanize.naturaldelta(avg_time)}. The oldest MR: {humanize.naturaldelta(max(deltas))}'

    return payload
