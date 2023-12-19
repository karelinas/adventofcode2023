import re
from dataclasses import dataclass
from enum import IntEnum, auto
from math import prod
from operator import gt, lt
from sys import stdin
from typing import Callable, Iterable, Optional

RE_WORKFLOW = re.compile(r"^(\w+){([^}]+)}$")
RE_RULE = re.compile(r"^(\w+)([<>])(\d+):(\w+)")
RE_PART = re.compile(r"^{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}")
OP: dict[str, Callable] = {"<": lt, ">": gt}


def main() -> None:
    workflows: WorkflowMap
    parts: PartList
    workflows, parts = parse_input(stdin.read())

    print("Part 1:", accepted_rating(workflows, parts))
    print("Part 2:", count_distinct_combinations(workflows))


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


@dataclass
class Rule:
    fn: Callable[[Part], Optional[str]]
    jmp: str
    attr: Optional[str] = None
    oper: Optional[str] = None
    val: Optional[int] = None

    def __call__(self, part: Part) -> Optional[str]:
        return self.fn(part)

    def inverted(self) -> "Rule":
        """Make an inverted version of the rule

        For example the rule "a>1716:R" would turn to "a<1717:R".
        """

        def invert_oper(oper: Optional[str]) -> Optional[str]:
            if oper == ">":
                return "<"
            elif oper == "<":
                return ">"
            return oper

        def invert_val(oper: Optional[str], val: Optional[int]) -> Optional[int]:
            if val is None or oper is None:
                return None
            # We don't support <= and >=, so increment/decrement the value as a
            # workaround for the same effect.
            if oper == ">":  # changes to <=
                return val + 1
            elif oper == "<":  # changes to >=
                return val - 1
            assert None, f"Invalid operator '{oper}'"

        # inverted fn is never needed in this program, so just pass the old one...
        return Rule(
            fn=self.fn,
            jmp=self.jmp,
            attr=self.attr,
            oper=invert_oper(self.oper),
            val=invert_val(self.oper, self.val),
        )


def create_rule(jmp: str, attr: str, oper: str, val: str) -> Rule:
    return Rule(
        fn=lambda part: jmp if OP[oper](getattr(part, attr), int(val)) else None,
        jmp=jmp,
        attr=attr,
        oper=oper,
        val=int(val),
    )


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
                attr, oper, val, jmp = rule_mo.groups()
                wf_rules.append(create_rule(jmp, attr, oper, val))
            else:
                wf_rules.append(Rule(fn=lambda _: rule, jmp=rule))

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


def inverted_rules(rules: list[Rule]) -> list[Rule]:
    return [rule.inverted() for rule in rules]


def all_accepted_paths(
    workflows: WorkflowMap, start: str = "in"
) -> Iterable[Iterable[Rule]]:
    """Yields a list of all distinct rule-paths from in to A."""
    if start in workflows:
        rules = workflows[start].rules
        for idx in range(len(rules)):
            rule = rules[idx]

            if rule.jmp == "A":
                yield inverted_rules(rules[:idx]) + [rule]
                continue

            for right in all_accepted_paths(workflows, rule.jmp):
                right_l: list[Rule] = list(right)
                if right_l and right_l[-1].jmp == "A":
                    yield inverted_rules(rules[:idx]) + [rule] + right_l


def count_distinct_combinations(workflows: WorkflowMap) -> int:
    combinations: int = 0

    for path in all_accepted_paths(workflows):
        vars: dict[str, tuple[int, int]] = {
            "x": (1, 4000),
            "m": (1, 4000),
            "a": (1, 4000),
            "s": (1, 4000),
        }
        for rule in path:
            if rule.oper is None or rule.attr is None or rule.val is None:
                continue
            if rule.oper == "<":
                vars[rule.attr] = (min(vars[rule.attr][0], rule.val - 1), rule.val - 1)
            elif rule.oper == ">":
                vars[rule.attr] = (rule.val + 1, max(vars[rule.attr][1], rule.val + 1))
        combinations += prod(stop - start + 1 for start, stop in vars.values())
    return combinations


if __name__ == "__main__":
    main()
