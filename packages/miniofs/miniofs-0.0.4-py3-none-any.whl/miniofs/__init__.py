from miniofs.functional import *
from minio import Minio

__version__ = "0.0.4"
cfg = load_config()
if cfg.host == "auto":
    try:
        cfg.host = f"{get_ip()}:9000"
    except:
        cfg.host = "127.0.0.1:9000"
client = Minio(
    cfg.host,
    secure=False,
    access_key=cfg.username,
    secret_key=cfg.password,
)
