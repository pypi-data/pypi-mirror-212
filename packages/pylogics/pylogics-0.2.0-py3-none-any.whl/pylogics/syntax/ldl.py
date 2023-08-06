# -*- coding: utf-8 -*-
#
# Copyright 2021 WhiteMech
#
# ------------------------------
#
# This file is part of pylogics.
#
# pylogics is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pylogics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pylogics.  If not, see <https://www.gnu.org/licenses/>.
#

"""Classes for linear dynamic logic."""
from abc import ABC
from functools import partial
from typing import Set

from pylogics.helpers.misc import enforce
from pylogics.syntax.base import (
    FalseFormula,
    Formula,
    Logic,
    TrueFormula,
    _BinaryOp,
    _CommutativeBinaryOp,
    _UnaryOp,
)


class _LDL(Formula, ABC):
    """Interface for LDL formulae."""

    @property
    def logic(self) -> Logic:
        """Get the logic formalism."""
        return Logic.LDL

    def __hash__(self):
        """Delegate the computation of the hash to the superclass."""
        return super(Formula, self).__hash__()


class _RegularExpression(Formula):
    """Regular expression."""

    @property
    def logic(self) -> Logic:
        """Get the logic formalism."""
        return Logic.RE


class Seq(_BinaryOp, _RegularExpression):
    """Sequence of regular expressions."""

    SYMBOL = "seq"
    ALLOWED_LOGICS: Set[Logic] = {Logic.RE}

    def __post_init__(self):
        """Check consistency after initialization."""
        enforce(
            all(op.logic == Logic.RE for op in self.operands),
            "not all the operands are regular expressions.",
        )


class Union(_CommutativeBinaryOp, _RegularExpression):
    """Union of regular expressions."""

    SYMBOL = "union"
    ALLOWED_LOGICS: Set[Logic] = {Logic.RE}

    def __post_init__(self):
        """Check consistency after initialization."""
        enforce(
            all(op.logic == Logic.RE for op in self.operands),
            "not all the operands are regular expressions.",
        )


class Test(_UnaryOp, _RegularExpression):
    """Test of an LDL formula."""

    SYMBOL = "test"
    ALLOWED_LOGICS: Set[Logic] = {Logic.RE}


class Star(_UnaryOp, _RegularExpression):
    """Kleene star of regular expressions."""

    SYMBOL = "star"


class Prop(_UnaryOp, _RegularExpression):
    """The propositional regular expression."""

    SYMBOL = "prop"
    ALLOWED_LOGICS: Set[Logic] = {Logic.PL}


class _TemporalFormula(_LDL, ABC):
    """LDL Temporal formula."""

    def __init__(self, regular_expression: Formula, tail_formula: Formula):
        """
        Initialize the formula.

        :param regular_expression:
        :param tail_formula:
        """
        enforce(regular_expression.logic == Logic.RE, "regular expression not valid")
        enforce(tail_formula.logic == Logic.LDL, "tail formula not valid")
        self._regular_expression = regular_expression
        self._tail_formula = tail_formula

    @property
    def regular_expression(self) -> Formula:
        """Get the regular expression."""
        return self._regular_expression

    @property
    def tail_formula(self) -> Formula:
        """Get the tail expression."""
        return self._tail_formula

    def __eq__(self, other):
        """Test equality."""
        return (
            type(self) == type(other)
            and self.regular_expression == other.regular_expression
            and self.tail_formula == other.tail_formula
        )

    def __hash__(self) -> int:
        """Compute the hash."""
        return hash((type(self), self.regular_expression, self.tail_formula))


class Diamond(_TemporalFormula):
    """Diamond formula."""


class Box(_TemporalFormula):
    """Box formula."""


End = partial(Box, Prop(TrueFormula()), FalseFormula(logic=Logic.LDL))
Last = partial(Diamond, Prop(TrueFormula()), End())
