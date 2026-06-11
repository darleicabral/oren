"""Upload site files to Hostinger via FTP. Reads credentials from .env."""
import ftplib
import os

HERE = os.path.dirname(__file__)

def load_env():
    env = {}
    with open(os.path.join(HERE, ".env")) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k] = v
    return env

env = load_env()

FILES = [
    "index.html",
    "termos.html",
    "assets/bateia-logo.png",
    "assets/bts-logo-new.png",
    "assets/oren-full-poster.png",
    "assets/oren-full.webm",
    "assets/oren-logo-full.png",
    "assets/uaipay-logo.png",
    "video2-final.mp4",
]

ftp = ftplib.FTP()
ftp.connect(env["FTP_HOST"], 21, timeout=60)
ftp.login(env["FTP_USER"], env["FTP_PASS"])
ftp.set_pasv(True)

REMOTE_BASE = env["FTP_REMOTE_BASE"]

def ensure_dir(path):
    parts = path.split("/")
    cur = REMOTE_BASE
    try:
        ftp.cwd(cur)
    except ftplib.error_perm:
        ftp.mkd(cur)
        ftp.cwd(cur)
    for p in parts[:-1]:
        try:
            ftp.cwd(p)
        except ftplib.error_perm:
            ftp.mkd(p)
            ftp.cwd(p)
    ftp.cwd("/")

for f in FILES:
    ensure_dir(f)
    remote_path = f"{REMOTE_BASE}/{f}"
    local_path = os.path.join(HERE, f)
    size = os.path.getsize(local_path)
    with open(local_path, "rb") as fh:
        print(f"Uploading {f} ({size} bytes) -> {remote_path}")
        ftp.storbinary(f"STOR {remote_path}", fh)

ftp.quit()
print("Done.")
