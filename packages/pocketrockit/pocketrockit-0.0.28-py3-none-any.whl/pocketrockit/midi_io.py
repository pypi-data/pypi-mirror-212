#!/usr/bin/env python3

"""Stuff needed to communicate with MIDI devices
"""

import asyncio
import logging
import os
import threading
import time
from collections.abc import Iterable, Iterator, Sequence, MutableMapping
from contextlib import contextmanager, suppress
from typing import ContextManager

import fluidsynth

# pylint: disable=wrong-import-position
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame.midi

from .commons import MidiConfig, MidiEvent, SfContent


def logger() -> logging.Logger:
    """Named logger"""
    return logging.getLogger("pr.midi_io")


def choose(choices: Iterable[str], *wishlist: str) -> str:
    """Choose from a list of strings until we found someting matching"""
    for wish in wishlist:
        with suppress(StopIteration):
            return next(name for name in choices if wish in name)
    raise KeyError(f"{wishlist}")


# def read_midi(loop, event_queue, terminator):
# logger().debug(">> read_midi")

# try:
# available_input_ports = set(mido.get_input_names())
# logger().info("Available MIDI input ports: \n%s", "  \n".join(available_input_ports))

# chosen_input = choose(
# available_input_ports, "OP-1", "Sylphyo", "USB MIDI Interface", "Midi Through"
# )
# logger().info("Chosen: %r", chosen_input)

# with mido.open_input(chosen_input) as inport:
# while not terminator.is_set():
# if (event := inport.receive()).type == "clock":
# continue
# asyncio.run_coroutine_threadsafe(event_queue.put(event), loop=loop)
# logger().debug("read_midi: got termination signal")

# except Exception as exc:
# logger().error("Unhandled exception in read_midi thread: %s", exc)

# logger().debug("<< read_midi")


@contextmanager
def midi_output_pygame() -> Iterator[pygame.midi.Output]:
    """
    fluidsynth -vv -a pipewire -z 256 -g 2 FluidR3_GM.sf2
    """
    try:
        pygame.midi.init()
        for i in range(pygame.midi.get_count()):
            logger().debug("found MIDI device: %d: %s", i, pygame.midi.get_device_info(i))
        player = pygame.midi.Output(2)
        player.set_instrument(0)
        yield player
    finally:
        del player
        pygame.midi.quit()


class MidiOutputFluidsynth:
    """Wrapps Fluidsynth to create a configurable MIDI player"""

    def __init__(self, config: MidiConfig):
        def raise_on_error(result: int) -> int:
            if result < 0:
                raise RuntimeError("Call to FluidSynth function returned error")
            return result

        self.midi_out = fluidsynth.Synth(gain=2.0, samplerate=44100.0, channels=256)
        for key, value in config.audio.items():
            self.midi_out.setting(f"audio.{key}", value)
        if config.reverb:
            raise_on_error(self.midi_out.set_reverb(**config.reverb))
        if config.chorus:
            raise_on_error(self.midi_out.set_chorus(**config.chorus))

        self.instruments: MutableMapping[int|str, int] = {}

        for sf_load in config.sf_load or []:
            # sf_content = SfContent(sf_load.filepath)

            sf2 = raise_on_error(self.midi_out.sfload(sf_load.filepath.as_posix()))
            for instrument in sf_load.instruments:
                channel = next(i for i in range(256) if i not in self.instruments)
                if instrument.name in self.instruments:
                    raise RuntimeError(f"Name for instrument already taken: {instrument.name}")
                self.instruments[instrument.name] = channel
                if instrument.short:
                    if instrument.short in self.instruments:
                        raise RuntimeError(
                            f"Short name for instrument already taken: {instrument.short}")
                    self.instruments[instrument.short] = channel
                if channel in self.instruments:
                    raise RuntimeError(f"Channel index for instrument already taken: {channel}")
                self.instruments[channel] = channel
                print(
                    f"ch {channel}: {sf_load.filepath.stem}"
                    f", {instrument.bank}:{instrument.preset} {instrument.name}"
                )
                raise_on_error(
                    self.midi_out.program_select(channel, sf2, instrument.bank, instrument.preset)
                )

        raise_on_error(self.midi_out.start())

    def noteon(self, channel: int, note: int, velocity: int) -> None:
        """noteon wrapper"""
        ch =  self.instruments[channel]
        self.midi_out.noteon(ch, note, velocity)

    def noteoff(self, channel: int, note: int) -> None:
        """noteoff wrapper"""
        self.midi_out.noteoff(self.instruments[channel], note)

    def __enter__(self) -> "MidiOutputFluidsynth":
        return self

    def __exit__(self, *args: object) -> bool:
        self.midi_out.delete()
        return True


def midi_output_device(config: MidiConfig) -> ContextManager[MidiOutputFluidsynth]:
    """Implementation agnostic wrapper for synthesizer context manager"""
    if config.backend == "fluidsynth":
        return MidiOutputFluidsynth(config)
    raise RuntimeError(f"Don't know MIDI backend {config.backend}")


def device_id(choices: Iterable[str]) -> int:
    """Select a pygame midi device id given a list of substring choices"""
    raw_input_devices = tuple(
        (i, pygame.midi.get_device_info(i)) for i in range(pygame.midi.get_count())
    )
    input_devices = {
        i: bname.decode()
        for i, (_, bname, is_input, *_) in raw_input_devices
        if is_input
        if any(c.lower() in bname.decode().lower() for c in choices)
    }
    logger().info("input devices: %s", input_devices)

    for choice in choices:
        for dev_id, dev_name in input_devices.items():
            if choice.lower() in dev_name.lower():
                return dev_id
    raise RuntimeError("Didn't find a device name matching any of the provided conditions")


def midi_input_pygame(
    choices: Iterable[str],
    loop: asyncio.BaseEventLoop,
    event_queue: asyncio.Queue[MidiEvent],
    terminator: threading.Event,
) -> None:
    """Read MIDI input via pygame"""
    if not event_queue:
        return None
    try:
        pygame.midi.init()

        if (input_device_id := device_id(choices)) is None:
            logger().info("No MIDI devices attached")
            return None

        input_device = pygame.midi.Input(input_device_id)
        while not terminator.is_set():
            if not input_device.poll():
                time.sleep(0.01)
                continue
            for status, data1, data2, data3, tick in (
                (_data[0], _data[1], _data[2], _data[3], _tick)
                for _data, _tick in input_device.read(100)
                if isinstance(_data, list)
                if _data != [248, 0, 0, 0]
            ):
                assert isinstance(tick, int)
                asyncio.run_coroutine_threadsafe(
                    event_queue.put(MidiEvent(status, data1, data2, data3, tick)),
                    loop=loop,
                )
    finally:
        pygame.midi.quit()
    return None


def midi_input_device(
    name: str,
    choices: Sequence[str],
    loop: asyncio.BaseEventLoop,
    event_queue: asyncio.Queue[MidiEvent],
    terminator: threading.Event,
) -> None:
    """Implementation agnostic wrapper for MIDI input context manager"""
    try:
        if name:
            return midi_input_pygame(
                choices=choices, loop=loop, event_queue=event_queue, terminator=terminator
            )
    except RuntimeError as exc:
        logger().warning("Could not attach MIDI input device: '%s'", exc)
    return None
