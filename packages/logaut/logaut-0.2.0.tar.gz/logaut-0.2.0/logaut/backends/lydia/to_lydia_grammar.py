# -*- coding: utf-8 -*-
#
# Copyright 2021 WhiteMech
#
# ------------------------------
#
# This file is part of logaut.
#
# logaut is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# logaut is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with logaut.  If not, see <https://www.gnu.org/licenses/>.
#

"""Transform a formula to a Lydia grammar."""

import functools
from typing import Sequence

from pylogics.syntax.base import (
    AbstractAtomic,
    And,
    Equivalence,
    FalseFormula,
    Formula,
    Implies,
    Logic,
    Not,
    Or,
    TrueFormula,
)
from pylogics.syntax.ldl import Box, Diamond, Prop, Seq, Star, Test, Union
from pylogics.syntax.ltl import (
    Always,
    Eventually,
    Next,
    Release,
    StrongRelease,
    Until,
    WeakNext,
    WeakUntil,
)
from pylogics.syntax.pltl import Before, Historically, Once, Since


@functools.singledispatch
def to_string(_formula: Formula):
    """
    Convert a formula to a Lydia-compliant formula.

    By default, use the Pylogics' 'to_string' function.
    """
    raise ValueError("formula not supported")


def _map_operands_to_string(operands: Sequence[Formula]):
    """Map a list of operands to a list of strings (with brackets)."""
    return map(lambda sub_formula: f"({to_string(sub_formula)})", operands)


@to_string.register(And)
def to_string_and(formula: And) -> str:
    """Transform an And into string."""
    return " & ".join(_map_operands_to_string(formula.operands))


@to_string.register(Or)
def to_string_or(formula: Or) -> str:
    """Transform an Or into string."""
    return " | ".join(_map_operands_to_string(formula.operands))


@to_string.register(Not)
def to_string_not(formula: Not) -> str:
    """Transform a Not into string."""
    return f"~({to_string(formula.argument)})"


@to_string.register(Implies)
def to_string_implies(formula: Implies) -> str:
    """Transform an Implies into string."""
    return " -> ".join(_map_operands_to_string(formula.operands))


@to_string.register(Equivalence)
def to_string_equivalence(formula: Equivalence) -> str:
    """Transform an Equivalence into string."""
    return " <-> ".join(_map_operands_to_string(formula.operands))


@to_string.register(AbstractAtomic)
def to_string_atomic(formula: AbstractAtomic) -> str:
    """Transform an atomic formula into string."""
    return formula.name


@to_string.register(Next)
def to_string_next(formula: Next) -> str:
    """Transform a next formula into string."""
    return f"X[!]({to_string(formula.argument)})"


@to_string.register(WeakNext)
def to_string_weak_next(formula: WeakNext):
    """Transform the weak next formula."""
    return f"X({to_string(formula.argument)})"


@to_string.register(Until)
def to_string_until(formula: Until) -> str:
    """Transform a until formula into string."""
    return " U ".join(_map_operands_to_string(formula.operands))


@to_string.register(WeakUntil)
def to_string_weak_until(formula: WeakUntil):
    """Transform the 'weak until' formula."""

    def _translate_weak_until(left: Formula, right: Formula):
        return Or(Until(left, right), Always(right))

    result = _translate_weak_until(formula.operands[-1], formula.operands[-2])
    for sub_formula in reversed(formula.operands[:-2]):
        result = _translate_weak_until(sub_formula, result)
    return to_string(result)


@to_string.register(Release)
def to_string_release(formula: Release) -> str:
    """Transform a release formula into string."""
    return " R ".join(_map_operands_to_string(formula.operands))


@to_string.register(StrongRelease)
def to_string_strong_release(formula: StrongRelease) -> str:
    """
    Transform a strong release formula into string.

    Note that the strong release is not supported (yet) by LTLf2DFA.
    We reduce it to weak until by duality.
    """
    result = to_string(WeakUntil(*map(Not, formula.operands)))
    return f"!({result})"


@to_string.register(Eventually)
def to_string_eventually(formula: Eventually) -> str:
    """Transform a eventually formula into string."""
    return f"F({to_string(formula.argument)})"


@to_string.register(Always)
def to_string_always(formula: Always) -> str:
    """Transform a always formula into string."""
    return f"G({to_string(formula.argument)})"


@to_string.register(Before)
def to_string_pltl_before(formula: Before) -> str:
    """Transform a 'before' formula into string."""
    return f"Y({to_string(formula.argument)})"


@to_string.register(Since)
def to_string_pltl_since(formula: Since) -> str:
    """Transform a 'since' formula into string."""
    return " S ".join(_map_operands_to_string(formula.operands))


@to_string.register(Once)
def to_string_pltl_once(formula: Once) -> str:
    """Transform a 'once' formula into string."""
    return f"O({to_string(formula.argument)})"


@to_string.register(Historically)
def to_string_pltl_historically(formula: Historically) -> str:
    """Transform a 'historically' formula into string."""
    return f"H({to_string(formula.argument)})"


@to_string.register(TrueFormula)
def to_string_ldl_true(formula: TrueFormula) -> str:
    """Transform a true into string."""
    return "tt" if formula.logic != Logic.PL else "true"


@to_string.register(FalseFormula)
def to_string_ldl_false(formula: FalseFormula) -> str:
    """Transform a false into string."""
    return "ff" if formula.logic != Logic.PL else "false"


@to_string.register(Diamond)
def to_string_ldl_diamond(formula: Diamond) -> str:
    """Transform an LDL diamond formula into string."""
    return f"<({to_string(formula.regular_expression)})>({to_string(formula.tail_formula)})"


@to_string.register(Box)
def to_string_ldl_box(formula: Box) -> str:
    """Transform an LDL box formula into string."""
    return f"[({to_string(formula.regular_expression)})]({to_string(formula.tail_formula)})"


@to_string.register(Seq)
def to_string_re_seq(formula: Seq) -> str:
    """Transform a sequence regular expression into string."""
    return ";".join(_map_operands_to_string(formula.operands))


@to_string.register(Union)
def to_string_re_union(formula: Union) -> str:
    """Transform a union regular expression into string."""
    return "+".join(_map_operands_to_string(formula.operands))


@to_string.register(Star)
def to_string_re_star(formula: Star) -> str:
    """Transform a star regular expression into string."""
    return f"({to_string(formula.argument)})*"


@to_string.register(Test)
def to_string_test(regex: Test):
    """
    Convert a test expression to a Lydia-compliant formula.

    It moves the question mark *after* the regular expression.
    """
    return f"({to_string(regex)})?"


@to_string.register(Prop)
def to_string_re_prop(formula: Prop) -> str:
    """Transform a propositional regular expression into string."""
    return f"({to_string(formula.argument)})"
