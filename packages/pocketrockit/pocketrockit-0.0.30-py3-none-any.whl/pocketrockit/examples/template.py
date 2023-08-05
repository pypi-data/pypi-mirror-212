#!/usr/bin/env python3
"""You can write some lines here in case you're more into writing than into music"""

# feel free to import any other modules
import random

# you can also write from `pocketrockit import *` - but this is more pythonic
from pocketrockit import Env, midiseq, player, track

# tell formaters not to destroy your ASCII art
# fmt: off


@track
def track_name(env: Env):
    """Put a little poem here, if you want. I'll describe the currently available syntax for
    sequencer pattern used for midiseq():
        - 'C', 'D', 'E'.. 'E3'.. 'fis', 'ges'.. specify notes
        - 'I' .. 'VIII' specify steps relative to a key
        - ' ' (space) separates notes
        - '|' separates 'measures'
        - ,: separate notes in a chord, e.g. 'C,E,F'
        - paranthesis divide rythm
        - +/-: shift half tones
        - ><: shift octaves
    """

    # @env object contains some global stuff - currently: only bpm and step_size
    env.bpm = 100

    key = "A3,A3,A3-"

    # The @player decorator defines one instrumental part played along others
    # Choose any valid function name - functions with same name overwrite each other
    @player
    def metronome():
        # use MIDI numbers directly for percussion
        yield from midiseq("76 77 77 77 | 77 77 77 77", channel="Standard")

    @player
    def percussion():
        # note there is no '|' on the second line, this will expand to a 8-element-line
        yield from midiseq(
            "| 44  42  46  42"
            "  44  42  46  42", channel="Standard", velocity=50)

    BD = 36 # 38 base drum
    SD = 24 # snare
    ST = 31 # 37 stick
    CH = 42 # 44 closed hat
    OH = 46 # open hat

    @player
    def drums():
        yield from midiseq(
            f"| ({BD},{CH}  .  {OH} .  {SD},{CH} . {OH}  . ) "
            f"  ({BD},{CH}  .  {CH} .  {SD},{OH} . {CH}  . ) "
            , channel="Standard", velocity=60)

    @player
    def xylophone1():
        # Paranthesis can be used to sub-divide one element in a pattern
        yield from midiseq(
            "| I>          (I> . V . ) (. . VII- .)  V "
            "| (I> . . I>) (I> . V . ) (. . VII- .)  V ",
            key=key,
            channel="Xylophone",
            velocity=40,
        )

    @player
    def xylophone2():
        yield from midiseq(
            # &se random pattern if you know how
            " ".join(
                random.choice([
                    "I>", "II>", "III>", "V>", "VI>", ".", "."
                    ]) for i in range(16)
            ),
            key=key,
            channel="Xylophone",
            velocity=40,
        )
