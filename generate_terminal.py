import subprocess
import os

# Get token from gh CLI
token = subprocess.check_output(['gh', 'auth', 'token']).decode().strip()
os.environ['GITHUB_TOKEN'] = token

import gifos

t = gifos.Terminal(width=900, height=440, xpad=20, ypad=20)
github_stats = gifos.utils.fetch_github_stats(user_name="IndraTensei")

lines = [
    "",
    "  ___       _            _            _                ",
    " |_ _|_ __ | |_ __ _  __| | ___  __ _| |_ ___  ___ ___ ",
    "  | || '_ \\| __/ _` |/ _` |/ _ \\/ _` | __/ _ \\/ __/ __|",
    "  | || | | | || (_| | (_| |  __/ (_| | ||  __/\\__ \\__ \\",
    " |___|_| |_|\\__\\__,_|\\__,_|\\___|\\__,_|\\__\\___||___/___/",
    "",
    "  indratensei@github",
    "  ----------------------------------------------",
    "  OS:          Linux (Ubuntu) x86_64",
    "  Shell:       bash 5.1.16",
    "  Location:    Mumbai, India",
    "  Languages:   JS, TS, Python, C, C++",
    "  Focus:       Full-Stack + DevOps + Cloud",
    "  Status:      Building and Shipping",
    f"  Followers:   {github_stats.total_followers}",
    f"  Stars:       {github_stats.total_stargazers}",
    f"  Commits:     {github_stats.total_commits_all_time}",
    f"  PRs Merged:  {github_stats.total_pull_requests_merged}",
    "",
    "  > Online",
    "",
]

for i, line in enumerate(lines, start=1):
    t.gen_text(text=line, row_num=i, contin=True)

t.gen_gif()
print("GIF generated")
