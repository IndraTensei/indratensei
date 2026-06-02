import subprocess, os

token = subprocess.check_output(['gh', 'auth', 'token']).decode().strip()
os.environ['GITHUB_TOKEN'] = token

import gifos

t = gifos.Terminal(width=900, height=460, xpad=20, ypad=20)
s = gifos.utils.fetch_github_stats(user_name="IndraTensei")

L = [
    "",
    "  ___       _            _            _                ",
    " |_ _|_ __ | |_ __ _  __| | ___  __ _| |_ ___  ___ ___ ",
    "  | || '_ \\| __/ ` |/ _` |/ _ \\/ _` | __/ _ \\/ __/ __|",
    "  | || | | | || (_| | (_| |  __/ (_| | ||  __/\\__ \\__ \\",
    " |___|_| |_|\\__\\__,_|\\__,_|\\___|\\__,_|\\__\\___||___/___/",
    "",
    "  indratensei@github",
    "  -----------------------------------------------",
    "  OS:          Linux (Ubuntu) x86_64",
    "  Shell:       bash 5.1.16",
    "  Location:    Mumbai, India",
    "  Languages:   JS  TS  Python  C  C++",
    "  Focus:       Full-Stack + DevOps + Cloud",
    f"  Followers:   {s.total_followers}",
    f"  Stars:       {s.total_stargazers}",
    f"  Commits:     {s.total_commits_all_time}",
    f"  PRs Merged:  {s.total_pull_requests_merged}",
    "",
    "  > Online",
    "",
]

for i, line in enumerate(L, 1):
    t.gen_text(text=line, row_num=i, contin=True)

t.gen_gif()
print("Done")
