import re
from collections import Counter
from dataclasses import dataclass, field
from enum import IntEnum, auto
from functools import reduce
from itertools import count
from math import lcm, prod
from operator import add
from sys import stdin
from typing import Callable, Optional

RE_MODULE_DEFINITION = re.compile(r"^([%&]?\w+) -> (.*)$")


def main() -> None:
    machinery = Machinery.from_string(stdin.read())
    machinery.button_mash(1000)
    print("Part 1:", machinery.pulse_score())
    print("Part 2:", fewest_pushes_for_rx_low(machinery))


def fewest_pushes_for_rx_low(machinery: "Machinery") -> int:
    machinery.reset()

    # rx module should have only one conjunction module connected to it. We'll
    # call it the "rm" module because that's what its name is in my data :-)
    rm_module = next(m for m in machinery.modules.values() if "rx" in m.outputs)
    assert isinstance(rm_module, ConjunctionModule)

    # When all the inputs for the "rm" module are high, it sends a low pulse to rx
    want_high_from = set(rm_module.memory.keys())
    # Keep track of received high pulses
    high_pulses: set[str] = set()

    # Set a gnarly callback hack to let us know if rm received a high signal any time
    # during button press processing. Note that viewing the memory after the button
    # press is completed is not enough, as the states change multiple times during
    # one turn, and the final state of the memory tends to be all low.
    def cb_received_pulse(pulse: Pulse, source: str) -> None:
        if pulse == Pulse.High:
            high_pulses.add(source)

    rm_module.cb_received_pulse = cb_received_pulse

    # Find the button press counts where each of the inputs of rm is set high. Then
    # assume that the high pulse recurs at the same interval. Then take LCM of all
    # the input cycles, which gives the final result. A lot of assumptions have to be
    # met for this to work, but luckily the input seems to be crafted in such a way
    # that it does work.
    result: int = 1
    for n in count(start=1):
        if not want_high_from:
            break
        machinery.button()
        for src in want_high_from.copy():
            if src in high_pulses:
                result = lcm(result, n)
                want_high_from.remove(src)

    return result


class Pulse(IntEnum):
    Low: int = auto()
    High: int = auto()


@dataclass
class PulseMessage:
    source: str
    target: str
    pulse: Pulse


class FlipflopState(IntEnum):
    Off = auto()
    On = auto()

    def flip(self) -> "FlipflopState":
        return FlipflopState.On if self == FlipflopState.Off else FlipflopState.Off


@dataclass
class Module:
    label: str
    outputs: list[str]
    pulse_counter: Counter = field(
        default_factory=lambda: Counter({Pulse.Low: 0, Pulse.High: 0})
    )

    def pulse_in(self, pulse: Pulse, source: str) -> list[PulseMessage]:
        self.pulse_counter.update([pulse])
        return []

    def reset(self) -> None:
        self.pulse_counter = Counter({Pulse.Low: 0, Pulse.High: 0})


@dataclass
class BroadcastModule(Module):
    def pulse_in(self, pulse: Pulse, source: str) -> list[PulseMessage]:
        super().pulse_in(pulse, source)

        return [
            PulseMessage(source=self.label, target=target, pulse=pulse)
            for target in self.outputs
        ]


@dataclass
class FlipflopModule(Module):
    state: FlipflopState = FlipflopState.Off

    def pulse_in(self, pulse: Pulse, source: str) -> list[PulseMessage]:
        super().pulse_in(pulse, source)

        if pulse == Pulse.High:
            return []

        self.state = self.state.flip()
        pulse_out: Pulse = Pulse(self.state)
        return [
            PulseMessage(source=self.label, target=target, pulse=pulse_out)
            for target in self.outputs
        ]

    def reset(self) -> None:
        super().reset()
        self.state = FlipflopState.Off


@dataclass
class ConjunctionModule(Module):
    memory: dict[str, Pulse] = field(default_factory=dict)
    track: bool = False
    # gnarly hack for part 2 -- let someone know if we receive a high signal
    cb_received_pulse: Optional[Callable[[Pulse, str], None]] = None

    def pulse_in(self, pulse: Pulse, source: str) -> list[PulseMessage]:
        super().pulse_in(pulse, source)

        self.memory[source] = pulse

        if self.cb_received_pulse:
            self.cb_received_pulse(pulse, source)

        pulse_out: Pulse = (
            Pulse.Low
            if all(p == Pulse.High for p in self.memory.values())
            else Pulse.High
        )
        return [
            PulseMessage(source=self.label, target=target, pulse=pulse_out)
            for target in self.outputs
        ]

    def reset(self) -> None:
        super().reset()
        self.memory = {k: Pulse.Low for k in self.memory.keys()}


@dataclass
class OutputModule(Module):
    pass


@dataclass
class Machinery:
    modules: dict[str, Module]

    def button(self) -> None:
        msgqueue: list[PulseMessage] = [
            PulseMessage(source="button", target="broadcaster", pulse=Pulse.Low)
        ]
        while msgqueue:
            msg = msgqueue.pop(0)
            msgqueue.extend(self.modules[msg.target].pulse_in(msg.pulse, msg.source))

    def button_mash(self, n: int) -> None:
        for _ in range(n):
            self.button()

    def pulse_score(self) -> int:
        counts = reduce(add, (m.pulse_counter for m in self.modules.values()))
        return prod(counts.values())

    def reset(self) -> None:
        for module in self.modules.values():
            module.reset()

    @staticmethod
    def from_string(data: str) -> "Machinery":
        machinery: Machinery = Machinery(modules={})

        for line in data.split("\n"):
            if not line:
                continue
            mo = RE_MODULE_DEFINITION.match(line)
            assert mo, f"Invalid module definition: '{line}'"

            label, outputs = mo.groups()
            outputs = outputs.split(", ")

            if label == "broadcaster":
                machinery.modules[label] = BroadcastModule(label=label, outputs=outputs)
            elif label.startswith("%"):
                label = label[1:]
                machinery.modules[label] = FlipflopModule(label=label, outputs=outputs)
            elif label.startswith("&"):
                label = label[1:]
                machinery.modules[label] = ConjunctionModule(
                    label=label, outputs=outputs
                )

        # Add output modules
        for module in list(machinery.modules.values()):
            for tgt in module.outputs:
                if tgt not in machinery.modules:
                    machinery.modules[tgt] = OutputModule(label=tgt, outputs=[])

        # Add ConjunctionModule sources
        for target in machinery.modules.values():
            if isinstance(target, ConjunctionModule):
                target.memory = {
                    source.label: Pulse.Low
                    for source in machinery.modules.values()
                    if target.label in source.outputs
                }

        return machinery


if __name__ == "__main__":
    main()
