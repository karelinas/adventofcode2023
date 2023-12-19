import re
from dataclasses import dataclass
from enum import IntEnum, auto
from operator import gt, lt
from sys import stdin
from typing import Callable, Optional

RE_WORKFLOW = re.compile(r"^(\w+){([^}]+)}$")
RE_RULE = re.compile(r"^(\w+)([<>])(\d+):(\w+)")
RE_PART = re.compile(r"^{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}")
OP: dict[str, Callable] = {"<": lt, ">": gt}


def main() -> None:
    workflows: WorkflowMap
    parts: PartList
    workflows, parts = parse_input(stdin.read())

    print("Part 1:", accepted_rating(workflows, parts))


class WorkflowResult(IntEnum):
    Accepted: int = auto()
    Rejected: int = auto()


@dataclass(frozen=True, eq=True)
class Part:
    x: int
    m: int
    a: int
    s: int

    @staticmethod
    def from_string(data: str) -> "Part":
        mo = RE_PART.match(data)
        assert mo, f"Invalid part data: '{data}'"
        x, m, a, s = mo.groups()
        return Part(x=int(x), m=int(m), a=int(a), s=int(s))


Rule = Callable[[Part], Optional[str]]


def create_rule(attr: str, oper: str, val: str, tgt: str) -> Rule:
    return lambda part: tgt if OP[oper](getattr(part, attr), int(val)) else None


@dataclass(frozen=True, eq=True)
class Workflow:
    name: str
    rules: list[Rule]

    def apply(self, part: Part) -> str:
        for rule in self.rules:
            next_wf = rule(part)
            if next_wf:
                return next_wf
        assert None, "No rule matched"

    @staticmethod
    def from_string(data: str) -> "Workflow":
        wf_mo = RE_WORKFLOW.match(data)
        assert wf_mo, f"Invalid workflow data: '{data[:50]}'"

        wf_name, ruledata = wf_mo.groups()

        wf_rules: list[Rule] = []
        for rule in ruledata.split(","):
            if rule_mo := RE_RULE.match(rule):
                attr, oper, val, tgt = rule_mo.groups()
                wf_rules.append(create_rule(attr, oper, val, tgt))
            else:
                wf_rules.append(lambda _: rule)

        return Workflow(name=wf_name, rules=wf_rules)


WorkflowMap = dict[str, Workflow]
PartList = list[Part]


def parse_input(data: str) -> tuple[WorkflowMap, PartList]:
    workflowdata, partdata = data.split("\n\n")

    # parse and structure workflows
    workflows: list[Workflow] = [
        Workflow.from_string(line) for line in workflowdata.split("\n") if line
    ]
    workflowmap: dict[str, Workflow] = {wf.name: wf for wf in workflows}

    # parse parts
    parts: list[Part] = [
        Part.from_string(line) for line in partdata.split("\n") if line
    ]

    return workflowmap, parts


def apply_workflows(workflows: WorkflowMap, part: Part) -> WorkflowResult:
    current = workflows["in"]
    while current:
        next_wf = current.apply(part)

        if next_wf == "A":
            return WorkflowResult.Accepted
        elif next_wf == "R":
            return WorkflowResult.Rejected

        current = workflows[next_wf]
    assert None, "End of workflows reached"


def accepted_rating(workflows: WorkflowMap, parts: list[Part]) -> int:
    return sum(
        p.x + p.m + p.a + p.s
        for p in parts
        if apply_workflows(workflows, p) == WorkflowResult.Accepted
    )


if __name__ == "__main__":
    main()
