import datetime
import logging
import re
import subprocess
import time

log = logging.getLogger(__file__)

LOG_REGEX = [
    r'^(?P<event>ClientConnect): (?P<client_id>\d+)$',
    # ClientUserinfoChanged: 4 n\Visor\t\0\model\visor\hmodel\visor\c1\4\c2\5\hc\70\w\0\l\0\skill\    2.00\tt\0\tl\0
    r'^(?P<event>ClientUserinfoChanged): (?P<client_id>\d+) n\\(?P<name>.*)\\t\\(?P<team>\d+)\\model\\(?P<model>.*)\\hmodel\\(?P<head_model>.*)\\c1\\(?P<color1>\d+)\\c2\\(?P<color2>\d+)\\hc\\(?P<max_health>\d+)\\w\\(?P<wins>\d+)\\l\\(?P<losses>\d+)\\skill\\\s*(?P<skill>\d+\.\d+)\\tt\\(?P<team_task>\d+)\\tl\\(?P<team_leader>\d+)$',
    # ClientUserinfoChanged: 4 n\marco\t\0\model\doom/default\hmodel\doom/default\g_redteam\\g_blueteam\\c1\2\c2\5\hc\100\w\0\l\0\tt\0\tl\0
    r'^(?P<event>ClientUserinfoChanged): (?P<client_id>\d+) n\\(?P<name>.*)\\t\\(?P<team>\d+)\\model\\(?P<model>.*)\\hmodel\\(?P<head_model>.*)\\g_redteam\\(?P<red_team>.*)\\g_blueteam\\(?P<blue_team>.*)\\c1\\(?P<color1>\d+)\\c2\\(?P<color2>\d+)\\hc\\(?P<max_health>\d+)\\w\\(?P<wins>\d+)\\l\\(?P<losses>\d+)\\tt\\(?P<team_task>\d+)\\tl\\(?P<team_leader>\d+)$',
    r'^(?P<event>broadcast): (?P<broadcast_action>print) (?P<broadcast_message>.*)$',
    r'^(?P<event>Item): (?P<item_whatever>\d+) (?P<item>\w+)$',
    r'^(?P<event>Kill): (?P<actor_id>\d+) (?P<target_id>\d+) (?P<weapon_id>\d+): (?P<actor_name>\w+) killed (?P<target_name>\w+) by (?P<weapon_name>\w+)$',
    r'^(?P<event>Exit): (?P<msg>.*)$',
    r'^(?P<event>tell): (?P<actor_name>\w+) to (?P<target_name>\w+): (?P<msg>.*)$',
    r'^(?P<event>sayteam): (?P<actor_name>\w+): (?P<msg>.*)$',
    r'^(?P<event>say): (?P<actor_name>\w+): (?P<msg>.*)$',
    r'^(?P<event>voice): (?P<actor_name>\w+) (?P<voice>.*)$',
]

RUN = True


def run_command(command: list):
    log.debug("runnng command: %s", command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while RUN:
        line = process.stdout.readline().strip().decode('UTF-8')
        if line:
            yield line
        elif process.poll() is not None:
            return process.poll()
        else:
            time.sleep(0.1)

    process.terminate()


def log_line2blob(line: str):
    blob = {'timestamp': datetime.datetime.now().isoformat()}
    for r in LOG_REGEX:
        match = re.match(r, line)
        if match:
            blob.update(match.groupdict())
            return blob

    return None