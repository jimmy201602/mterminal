#!/usr/bin/env python3
"""Pixelate sensitive regions (internal IPs / hostnames) in README screenshots.
Box coords are given in 1568x910 preview units and scaled to the real image size."""
import sys
from PIL import Image

S = 3726 / 1568.0  # preview -> actual scale

def pixelate(im, box, factor=0.06):
    x0, y0, x1, y1 = [int(c * S) for c in box]
    x0 = max(0, x0); y0 = max(0, y0)
    x1 = min(im.width, x1); y1 = min(im.height, y1)
    if x1 <= x0 or y1 <= y0:
        return
    region = im.crop((x0, y0, x1, y1))
    small = region.resize((max(4, int(region.width * factor)),
                           max(4, int(region.height * factor))), Image.BILINEAR)
    im.paste(small.resize(region.size, Image.NEAREST), (x0, y0))

SIDEBAR = (30, 158, 250, 312)          # session list names/IPs
TITLE   = (268, 30, 1560, 56)          # "— user@host" in title bar
PILL    = (295, 62, 480, 86)           # connection pill "host:port (proto)"
STAT_L  = (255, 856, 585, 884)         # status bar "Host: ip | Protocol | User"
STAT_R  = (1335, 856, 1480, 884)       # status bar right-side endpoint

def tabs(x1):
    return (260, 92, x1, 122)

REGIONS = {
    "01-main-window.png":       [SIDEBAR],
    "02-new-session-ssh.png":   [SIDEBAR],
    "03-new-session-rdp.png":   [SIDEBAR],
    "04-new-session-vnc.png":   [SIDEBAR],
    "09-main-window-zh.png":    [SIDEBAR],
    "10-new-session-ssh-zh.png":[SIDEBAR],
    "05-ssh-terminal.png": [
        SIDEBAR, TITLE, PILL, tabs(415), STAT_L, STAT_R,
        (262, 262, 895, 285),   # IPv4 line: LAN + WAN addresses
        (250, 488, 400, 508),   # shell prompt user@server1
    ],
    "06-sftp-browser.png": [
        SIDEBAR, TITLE, PILL, tabs(585), STAT_L, STAT_R,
        (256, 126, 470, 148),   # "Connected · user@host:22"
        (900, 148, 1075, 172),  # REMOTE header endpoint
    ],
    "07-rdp-session.png": [SIDEBAR, TITLE, PILL, tabs(750), STAT_L, STAT_R],
    "08-vnc-session.png": [SIDEBAR, TITLE, PILL, tabs(915), STAT_L, STAT_R],
}

for name, boxes in REGIONS.items():
    p = f"images/{name}"
    im = Image.open(p).convert("RGB")
    for b in boxes:
        pixelate(im, b)
    im.save(p)
    print("redacted", name, len(boxes), "regions")
