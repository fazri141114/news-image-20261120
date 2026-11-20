# How this entry was built

The entrant's agent (Muse, driven by the entrant) researched the
world news of Friday 20 November 2026 on the morning of the bounty,
from wire and headline reports (Reuters, AP, BBC, Le Monde,
France 24, and the day's Indian and Korean headline wires),
cross-checked each story, and dropped the one figure the sources
disputed (the Cyclone Akvan evacuation count).

It then drew the front page with `build_image_20.py` (Pillow):
the entrant's WORLD NEWS DAILY design — masthead, three illustrated
heroes (the three flags of the Shenzhen summit, the scales of the
ICJ, the Anthropic IPO chart), six numbered sections, a dotted
world map with story pins, and a sourced footer. A small flow
engine in the builder stretches each section column so all 30
stories end exactly above the map band. `entry.png` is the
resulting palette PNG (683x1024); `main.py` (standard library
only) validates and reproduces it byte-for-byte.

The full, unedited session transcripts of the build are submitted
with the entry as the make.fun transcript bundle, produced by the
official kit from the agent's real session records.
