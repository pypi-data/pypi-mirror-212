from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

from antlr4 import CommonTokenStream, InputStream

from .generated.QueryExprLexer import QueryExprLexer
from .generated.QueryExprParser import QueryExprParser
from .generated.QueryExprParserVisitor import QueryExprParserVisitor


@dataclass(frozen=True, eq=True)
class Filter:
    """Represents a filter construct.

    Filters are immutable, and supports equality checks, eg.
    >>> Filter("foo", "=", "bar") == Filter("foo", "=", "bar")
    True

    """

    identifier: str
    operator: str = "="
    value: Any = ""
    label: Optional[str] = None

    @property
    def value_str(self) -> str:
        """Returns the string representation of `value`.
        * None   : "NULL"
        * boolean: "true" or "false"
        * number : "123" or "1.23"
        * string : as-is
        """
        if isinstance(self.value, str):
            return self.value
        elif isinstance(self.value, bool):
            return "true" if self.value else "false"
        elif self.value is None:
            return "NULL"
        else:
            return str(self.value)

    def __repr__(self) -> str:
        return f"<Filter {self.to_string()}>"

    def __str__(self) -> str:
        return self.to_string()

    def to_string(self) -> str:
        """Return a filter expression.

        >>> f = Filter("foo", "=", "bar")
        >>> f.to_string()
        "foo=bar"
        """
        parts = [self.identifier or "", self.operator or ""]
        parts.append(safe_string(self.value_str))
        if self.label:
            parts.append(f"[{safe_string(self.label)}]")
        return "".join(parts)

    def to_json(self) -> Dict:
        """Returns a dictionary representation.
        >>> f = Filter("foo", "=", "bar")
        >>> f.to_json()
        {
            "identifier": "foo",
            "operator": "=",
            "value": "bar"
        }
        """
        obj = {
            "identifier": self.identifier,
            "operator": self.operator,
            "value": self.value,
        }
        if self.label:
            obj["label"] = self.label
        return obj


class Query:
    """Query class parses and generates query expression."""

    @classmethod
    def parse(cls: Any, query: str) -> Query:
        """Return a `Query` by parsing the `query` expression.

        >>> q = Query.parse("foo=bar foo=baz")
        >>> q.filters
        [<Filter foo=bar>, <Filter foo=baz>]

        """
        lexer = QueryExprLexer(InputStream(query))
        parser = QueryExprParser(CommonTokenStream(lexer))
        filters = _Visitor().visitExprs(parser.exprs())
        return cls(filters)

    @property
    def filters(self) -> Sequence[Filter]:
        """A list of `Filter` instance."""
        return self._filters

    def __init__(self, filters: Optional[Sequence[Filter]] = None):
        self._filters = []
        if filters:
            for filter_ in filters:
                self.add_filter(filter_)
        assert isinstance(self._filters, Sequence)

    def __repr__(self) -> str:
        return f"<Query '{self.to_string()}'>"

    def __str__(self) -> str:
        return self.to_string()

    def add_filter(self, filter_: Filter):
        """Adds a `Filter` to the query.

        If a Filter with identical value exists in the Query, the operation
        is ignored. This guarantees that the Query has no identical Filter.
        """
        assert isinstance(
            filter_, Filter
        ), f"Expects `Filter` instance, but got {filter_}"
        self.remove_filter(filter_)
        self._filters.append(filter_)

    def remove_filter(self, filter_: Filter):
        """Removes a `Filter` to the query.

        If no Filter with identical value exists in the Query, the operation
        is ignored.
        """
        self._filters = list(filter(lambda x: x != filter_, self._filters))

    def to_string(self) -> str:
        """Return a query expression.

        >>> q = Query.parse("foo=bar foo=baz")
        >>> q.to_string()
        "foo=bar foo=baz"
        """
        return " ".join(f.to_string() for f in self.filters)

    def to_json(self) -> List[Dict]:
        """Return a list of filter dictionaries."""
        return [f.to_json() for f in self.filters]


class _Visitor(QueryExprParserVisitor):
    """Private implementation of the visitor pattern.

    Walks the parser tree and generate the filters.
    """

    def visitExprs(self, ctx: QueryExprParser.ExprsContext):
        filters = []
        self._filters = filters
        self.visitChildren(ctx)
        self._filters = None
        return filters

    def visitExpr(self, ctx: QueryExprParser.ExprContext):
        identifier = ctx.IDENTIFIER().getText()
        operator = ctx.OPERATOR().getText()
        value: Any = ""
        if ctx.NULL() is not None:
            value = None
        elif ctx.STRING() is not None:
            value = ctx.STRING().getText()
            if is_quoted_string(value):
                # Edge case where value is quoted but has no spaces
                # this gets pass the parser. eg '"NULL"'
                value = trim(value, '"', '"')
        elif ctx.STRING_QUOTED() is not None:
            value = json.loads(ctx.STRING_QUOTED().getText())
        elif ctx.BOOL() is not None:
            value = json.loads(ctx.BOOL().getText())
        elif ctx.NUMBER() is not None:
            value = ctx.NUMBER().getText()
            value = int(value) if value.lstrip("-+").isdigit() else float(value)
        label = None
        if ctx.LABEL() is not None:
            label = ctx.LABEL().getText()
            label = trim(label, "[", "]")
            if label.startswith('"') and label.endswith('"'):
                label = json.loads(label)
        self._filters.append(Filter(identifier, operator, value, label))


def trim(value: str, left: Optional[str], right: Optional[str]) -> str:
    """Removes `left` and `right` characters from `value` if they exists."""
    if not value:
        return value
    if value.startswith(left):
        value = value[len(left) :]
    if value.endswith(right):
        value = value[0 : -len(right)]
    return value


def quote_string(value: str) -> str:
    """Wrap `value` in double quotes, escaping any double quotes
    in `value` if required.
    """
    return json.dumps(value)


def unquote_string(value: str) -> str:
    """Unwrap `value` from double quotes, unescaping any double quotes
    in `value` if required.
    """
    try:
        return json.loads(value)
    except Exception:
        return value


def is_quoted_string(value: str) -> bool:
    """Returns True if `value` is wrapped in double quotes."""
    return isinstance(value, str) and value.startswith('"') and value.endswith('"')


def safe_string(value: str) -> str:
    """Wraps a string in double quotes if required, so that it can be safely
    embeded in a query expression string.
    """
    # We wrap `value if:
    # - it contains spaces, for `Filter.value`
    # - it contains square brackets, for `Filter.label`
    if isinstance(value, str) and any(c in value for c in " []"):
        return quote_string(value)
    return value
