"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0
"""

from cfnlint.schema.resolver import RefResolver


def test_resolve_fragment_by_id():
    resolver = RefResolver.from_schema({})
    document = {
        "definitions": {
            "a": {"id": "#a", "type": "string"},
            "b": {"$id": "#b", "type": "number"},
        }
    }

    assert resolver.resolve_fragment(document, "a") == {"id": "#a", "type": "string"}
    assert resolver.resolve_fragment(document, "b") == {
        "$id": "#b",
        "type": "number",
    }


def test_resolve_fragment_short_lived_documents():
    # Each document is freed before the next one is built, and the outer
    # dict is allocated first, so CPython hands every new document the
    # id() of the freed one. Results must still come from the document
    # passed in.
    resolver = RefResolver.from_schema({})
    for i in range(100):
        document = {}
        document["definitions"] = {"a": {"id": "#a", "value": i}}
        assert resolver.resolve_fragment(document, "a")["value"] == i
        del document
