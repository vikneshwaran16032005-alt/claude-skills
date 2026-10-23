"""Zero to Closer — hand-drawn diagram kit (matplotlib xkcd, no credits).
Every diagram in the course is composed from these helpers so they all share
one look: wobbly marker lines on a warm cream "napkin" card, dark ink, legible
hand-ish labels. Run with the render venv python:
  /Users/vik/.claude/skills/rioa-pdf/.venv/bin/python <script that imports this>

Usage in a composing script:
  from diagram_kit import fraction, flow, compare, funnel, timeline, ladder, meter, cycle
  fraction("value_equation", left="VALUE",
           top=["DREAM OUTCOME","PERCEIVED LIKELIHOOD"],
           bottom=["TIME DELAY","EFFORT & SACRIFICE"])
Each call writes img/<name>.png and returns the path. Keep names kebab/underscore,
unique per diagram. Then embed in the module markdown as:
  ![caption in plain words](img/<name>.png)
"""
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

INK = "#241f1c"      # marker ink
PAPER = "#f2ece1"    # warm napkin cream (matches Night Ledger "bone")
ACCENT = "#8f1116"   # the one blood-red, used sparingly for emphasis
IMGDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
os.makedirs(IMGDIR, exist_ok=True)

_XKCD = dict(scale=1.05, length=110, randomness=3)

def _fig(w=7.2, h=4.8):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(PAPER); ax.set_facecolor(PAPER)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    return fig, ax

def _save(fig, name):
    p = os.path.join(IMGDIR, f"{name}.png")
    # bbox_inches="tight" crops the PNG to the drawn content (+ a small pad) so
    # there is no wasted blank margin around the sketch.
    fig.savefig(p, dpi=150, facecolor=PAPER, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
    return p

def _box(ax, x, y, w, h, label, fs=12, edge=INK):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle="round,pad=0.12,rounding_size=0.25",
        fill=False, edgecolor=edge, linewidth=2.2))
    ax.text(x, y, label, fontsize=fs, color=INK, ha="center", va="center", wrap=True)

def _arrow(ax, x1, y1, x2, y2, color=INK, lw=2.4):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw))

# ---- composers -------------------------------------------------------------

def fraction(name, top, bottom, left="VALUE"):
    with plt.xkcd(**_XKCD):
        fig, ax = _fig(7.2, 5.0)
        ax.text(0.5, 5, left, fontsize=18, color=INK, va="center", ha="left", weight="bold")
        ax.text(3.1, 5, "=", fontsize=24, color=INK, va="center", ha="center")
        ax.plot([3.8, 9.5], [5, 5], color=INK, lw=3)
        for i, t in enumerate(top):
            ax.text(6.65, 7.9 - i*1.4, t, fontsize=12, color=INK, ha="center")
        for i, b in enumerate(bottom):
            ax.text(6.65, 3.5 - i*1.4, b, fontsize=12, color=INK, ha="center")
        _arrow(ax, 9.35, 6.1, 9.35, 8.6); ax.text(1.5, 8.7, "want big", fontsize=10, color=INK, ha="center")
        _arrow(ax, 9.35, 3.9, 9.35, 1.4); ax.text(1.5, 1.3, "want small", fontsize=10, color=INK, ha="center")
        return _save(fig, name)

def flow(name, steps, direction="lr"):
    with plt.xkcd(**_XKCD):
        n = len(steps)
        if direction == "lr":
            fig, ax = _fig(max(7.2, 2.4*n), 3.2)
            bw = 9.4 / n; y = 5
            for i, s in enumerate(steps):
                cx = bw*(i+0.5) + 0.3
                _box(ax, cx, y, bw*0.82, 2.4, s, fs=11)
                if i < n-1:
                    _arrow(ax, cx+bw*0.42, y, cx+bw*0.58, y)
        else:
            fig, ax = _fig(6.0, max(4.8, 1.7*n))
            bh = 9.2 / n; x = 5
            for i, s in enumerate(steps):
                cy = 9.6 - bh*(i+0.5)
                _box(ax, x, cy, 7.5, bh*0.72, s, fs=11)
                if i < n-1:
                    _arrow(ax, x, cy-bh*0.36, x, cy-bh*0.64)
        return _save(fig, name)

def compare(name, left_title, left_items, right_title, right_items):
    with plt.xkcd(**_XKCD):
        n = max(len(left_items), len(right_items))
        top = 8.2; rowh = 1.05
        bottom = top - (n - 1) * rowh          # y of the last item row
        # figure height tracks the number of rows so short lists aren't tall + empty
        fig, ax = _fig(7.6, 1.5 + 0.62 * n)
        # divider spans only from just above the titles to just below the last row
        ax.plot([5, 5], [bottom - 0.5, 9.2], color=INK, lw=1.8)
        ax.text(2.6, 9.4, left_title, fontsize=13, color=ACCENT, ha="center", weight="bold")
        ax.text(7.4, 9.4, right_title, fontsize=13, color=INK, ha="center", weight="bold")
        for i, it in enumerate(left_items):
            y = top - i*rowh
            ax.text(0.5, y, "X", fontsize=12, color=ACCENT, ha="left", va="center", weight="bold")
            ax.text(1.2, y, it, fontsize=10.5, color=INK, ha="left", va="center")
        for i, it in enumerate(right_items):
            y = top - i*rowh
            # hand-drawn check mark (two marker strokes) instead of the word "check"
            ax.plot([5.30, 5.52], [y+0.03, y-0.24], color=INK, lw=2.6, solid_capstyle="round")
            ax.plot([5.52, 5.98], [y-0.24, y+0.36], color=INK, lw=2.6, solid_capstyle="round")
            ax.text(6.3, y, it, fontsize=10.5, color=INK, ha="left", va="center")
        # crop the view to the content so bbox_inches trims the blank below
        ax.set_ylim(bottom - 1.1, 10.0)
        return _save(fig, name)

def funnel(name, stages):
    with plt.xkcd(**_XKCD):
        fig, ax = _fig(6.6, 5.2); n = len(stages)
        top_w, bot_w = 8.4, 2.6; H = 8.2; y0 = 9.0
        for i, s in enumerate(stages):
            wt = top_w + (bot_w-top_w)*(i/n)
            wb = top_w + (bot_w-top_w)*((i+1)/n)
            yt = y0 - H*(i/n); yb = y0 - H*((i+1)/n)
            ax.plot([5-wt/2,5-wb/2],[yt,yb], color=INK, lw=2.2)
            ax.plot([5+wt/2,5+wb/2],[yt,yb], color=INK, lw=2.2)
            ax.plot([5-wt/2,5+wt/2],[yt,yt], color=INK, lw=1.6)
            ax.text(5, (yt+yb)/2, s, fontsize=11, color=INK, ha="center", va="center")
        ax.plot([5-bot_w/2,5+bot_w/2],[y0-H,y0-H], color=INK, lw=1.6)
        return _save(fig, name)

def timeline(name, points):
    # points: list of (tick_label, note)
    with plt.xkcd(**_XKCD):
        fig, ax = _fig(max(7.6, 2.2*len(points)), 3.6)
        ax.plot([0.5,9.5],[5,5], color=INK, lw=2.6)
        n = len(points); step = 9.0/max(1,n-1) if n>1 else 0
        for i,(tick,note) in enumerate(points):
            x = 0.5 + step*i if n>1 else 5
            ax.plot([x,x],[4.7,5.3], color=INK, lw=2.2)
            ax.text(x, 5.9, tick, fontsize=11, color=ACCENT if i==0 else INK, ha="center", weight="bold")
            ax.text(x, 3.9, note, fontsize=9.5, color=INK, ha="center", va="top", wrap=True)
        return _save(fig, name)

def ladder(name, rungs):
    # rungs: bottom-to-top list; drawn climbing up
    with plt.xkcd(**_XKCD):
        fig, ax = _fig(6.4, max(4.8, 1.3*len(rungs)+1)); n=len(rungs)
        for i,r in enumerate(rungs):
            y = 1.2 + (8.0/max(1,n))*i
            _box(ax, 5, y, 8.2, 7.4/max(1,n)*0.78, r, fs=11)
            if i < n-1:
                _arrow(ax, 8.6, y+0.2, 8.6, y+(8.0/max(1,n))-0.2, lw=2)
        ax.text(1.0, 9.3, "up", fontsize=10, color=INK, ha="center")
        return _save(fig, name)

def meter(name, label, left_end, right_end, marker_frac, marker_label=""):
    with plt.xkcd(**_XKCD):
        fig, ax = _fig(7.2, 3.0)
        ax.plot([1,9],[5,5], color=INK, lw=3)
        ax.plot([1,1],[4.6,5.4], color=INK, lw=2); ax.plot([9,9],[4.6,5.4], color=INK, lw=2)
        mx = 1 + 8*max(0,min(1,marker_frac))
        _arrow(ax, mx, 7.0, mx, 5.4, color=ACCENT)
        if marker_label: ax.text(mx, 7.4, marker_label, fontsize=10.5, color=ACCENT, ha="center")
        ax.text(1, 4.0, left_end, fontsize=10.5, color=INK, ha="center", va="top")
        ax.text(9, 4.0, right_end, fontsize=10.5, color=INK, ha="center", va="top")
        ax.text(5, 8.6, label, fontsize=13, color=INK, ha="center", weight="bold")
        return _save(fig, name)

def cycle(name, steps):
    # a loop of steps (e.g. agree -> answer -> ask again -> ...)
    import math
    with plt.xkcd(**_XKCD):
        fig, ax = _fig(6.0, 5.6); n=len(steps); R=3.1; cx,cy=5,5
        pts=[]
        for i in range(n):
            a = math.pi/2 - 2*math.pi*i/n
            pts.append((cx+R*math.cos(a), cy+R*math.sin(a)))
        for i,(x,y) in enumerate(pts):
            _box(ax, x, y, 3.0, 1.4, steps[i], fs=10.5)
        for i in range(n):
            x1,y1=pts[i]; x2,y2=pts[(i+1)%n]
            dx,dy=x2-x1,y2-y1; L=(dx*dx+dy*dy)**0.5
            ux,uy=dx/L,dy/L
            _arrow(ax, x1+ux*1.7, y1+uy*0.9, x2-ux*1.7, y2-uy*0.9, lw=2)
        return _save(fig, name)

if __name__ == "__main__":
    # self-test: one of each shape
    fraction("test_fraction", ["DREAM OUTCOME","PERCEIVED LIKELIHOOD"], ["TIME DELAY","EFFORT & SACRIFICE"])
    flow("test_flow_lr", ["Dial","Reveal","Text link","Close"], "lr")
    flow("test_flow_td", ["No pickup","Bump text","Voicemail","Move on"], "td")
    compare("test_compare", "PUSHY", ["convince","argue","talk over"], "A CLOSER", ["show","ask","go quiet"])
    funnel("test_funnel", ["Dials","Pickups","Owner","Pitched","Closed"])
    timeline("test_timeline", [("Day 1","dial x2"),("Day 2","voicemail"),("Day 7","dial again"),("Day 14","last try")])
    ladder("test_ladder", ["Website $750","Care plan $99/mo","Checkup","Ops retainer"])
    meter("test_meter", "HOW FAST YOU TALK", "slow + clear", "fast = noise", 0.28, "here")
    cycle("test_cycle", ["Agree","Answer","Ask again"])
    print("self-test wrote 9 diagrams to img/")
