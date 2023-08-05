#!/usr/bin/env python3

"""Shared stuff"""
# pylint: disable=too-many-arguments

from collections.abc import Mapping, Sequence
from contextlib import suppress
from dataclasses import dataclass, field
from pathlib import Path

import toml
from sf2utils.sf2parse import Sf2File

NestedConfig = Mapping[str, object]


@dataclass
class MidiEvent:
    """An internal application event"""

    status: int
    data1: int
    data2: int
    data3: int
    timestamp: int


@dataclass
class SfPreset:
    """Configuration structure a SoundFont preset"""

    # channel: None | int = None
    name: str
    short: None | str = None
    bank: None | int = None
    preset: None | int = None


@dataclass
class SfConfig:
    """Stores meta info about SoundFont files"""

    filepath: Path
    instruments: Sequence[SfPreset]
    info: None | Mapping[str, str] = None

    def __init__(self, filepath: str | Path, instruments: None | Sequence[NestedConfig] = None):
        self.filepath = Path(filepath)
        if instruments:
            self.instruments = [SfPreset(**element) for element in instruments]
        else:
            with open(filepath, "rb") as sf2_file:
                sf2 = Sf2File(sf2_file)
                self.info = {
                    key.decode(): value.decode().strip("\0") if isinstance(value, bytes) else value
                    for key, value in sf2.raw.info.items()
                }
                self.instruments = [
                    SfPreset(
                        # channel=None,
                        name=preset.name,
                        short=None,
                        bank=preset.bank,
                        preset=preset.preset,
                    )
                    for preset in sorted(
                        (_p for _p in sf2.presets if _p.name != "EOP"),
                        key=lambda p: (p.bank, p.preset),
                    )
                ]

    @staticmethod
    def fromMap(args: Mapping[str, object]) -> "SfConfig":
        """Factory function"""
        if args.keys() != {"filepath", "instruments"}:
            raise RuntimeError(f"Bad SoundFont mapping keys: {set(args.keys())}")
        return SfConfig(args["filepath"], args["instruments"])


@dataclass
class MidiConfig:
    """Configuration structure for a MIDI backend"""

    backend: str = "fluidsynth"
    audio: NestedConfig = field(default_factory=dict)
    reverb: None | object = None
    chorus: None | object = None
    sf_load: None | Sequence[SfConfig] = None

    def __init__(
        self,
        backend: None | str = None,
        sf_load: None | Sequence[NestedConfig] = None,
        audio: None | NestedConfig = None,
        reverb: None | object = None,
        chorus: None | object = None,
    ) -> None:
        if backend:
            self.backend = backend
        if sf_load is not None:
            self.sf_load = [SfConfig.fromMap(element) for element in sf_load]
        self.audio = {**{"period-size": 256}, **(audio or {})}
        if reverb:
            self.reverb = reverb
        if chorus:
            self.chorus = chorus


@dataclass
class PriConfig:
    """Stores pocketrockit configuration"""

    midi: MidiConfig = field(default_factory=MidiConfig)

    def __init__(self, data: Path):
        with suppress(FileNotFoundError):
            with open(data, encoding="utf-8") as toml_file:
                # TomlDecodeError
                raw = toml.load(toml_file)
                self.midi = MidiConfig(**(raw.get("pocketrockit") or {}).get("midi") or {})
                return
        self.midi = MidiConfig()
