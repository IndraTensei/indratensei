import gifos
import dotenv

dotenv.load_dotenv()

t = gifos.Terminal(width=800, height=380, xpad=15, ypad=15)

github_stats = gifos.utils.fetch_github_stats(user_name="IndraTensei")

t.gen_text(text="", row_num=1)
t.gen_text(text="  ___       _            _            _                ", row_num=2, contin=True)
t.gen_text(text=" |_ _|_ __ | |_ __ _  __| | ___  __ _| |_ ___  ___ ___ ", row_num=3, contin=True)
t.gen_text(text="  | || '_ \\| __/ _` |/ _` |/ _ \\/ _` | __/ _ \\/ __/ __|", row_num=4, contin=True)
t.gen_text(text="  | || | | | || (_| | (_| |  __/ (_| | ||  __/\\__ \\__ \\", row_num=5, contin=True)
t.gen_text(text=" |___|_| |_|\\__\\__,_|\\__,_|\\___|\\__,_|\\__\\___||___/___/", row_num=6, contin=True)
t.gen_text(text="", row_num=7)
t.gen_text(text="  indratensei@github", row_num=8, contin=True)
t.gen_text(text="  ----------------------------------------------", row_num=9, contin=True)
t.gen_text(text="  OS:          Linux (Ubuntu) x86_64", row_num=10, contin=True)
t.gen_text(text="  Shell:       bash 5.1.16", row_num=11, contin=True)
t.gen_text(text="  Location:    Mumbai, India", row_num=12, contin=True)
t.gen_text(text="  Languages:   JS, TS, Python, C, C++", row_num=13, contin=True)
t.gen_text(text="  Focus:       Full-Stack + DevOps + Cloud", row_num=14, contin=True)
t.gen_text(text="  Status:      Building and Shipping", row_num=15, contin=True)
t.gen_text(text=f"  Followers:   {github_stats.total_followers}", row_num=16, contin=True)
t.gen_text(text=f"  Stars:       {github_stats.total_stargazers}", row_num=17, contin=True)
t.gen_text(text=f"  Commits:     {github_stats.total_commits_all_time}", row_num=18, contin=True)
t.gen_text(text=f"  PRs Merged:  {github_stats.total_pull_requests_merged}", row_num=19, contin=True)
t.gen_text(text="", row_num=20)
t.gen_text(text="  > Online", row_num=21, contin=True)

t.gen_gif()
print("GIF generated at output.gif")
