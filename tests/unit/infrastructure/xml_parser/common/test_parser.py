from pathlib import Path

import pytest

from src.infrastructure.xml_parser.common.parser import UniversalXmlParser


current_dir = Path(__file__).resolve().parent

test_cases = [
    (
        current_dir / "simple_nesting.xml",
        {
            "books": {
                "$xml_tag": "book",
                "$pattern": [
                    {
                        "book_id": {"$xml_attr": "id"},
                        "book_title": {"$xml_attr": "title"},
                        "authors": {
                            "$xml_tag": "author",
                            "$pattern": [
                                {
                                    "author_name": {"$xml_attr": "name"},
                                }
                            ],
                        },
                    }
                ],
            }
        },
        {
            "books": [
                {
                    "book_id": "1",
                    "book_title": "Python",
                    "authors": [
                        {"author_name": "Alex"},
                        {"author_name": "Ivan"},
                    ],
                },
                {
                    "book_id": "2",
                    "book_title": "FastAPI",
                    "authors": [
                        {"author_name": "John"},
                    ],
                },
            ]
        },
    ),
    (
        current_dir / "deep_nesting.xml",
        {
            "players": {
                "$xml_tag": "player",
                "$pattern": [
                    {
                        "id": {"$xml_attr": "id"},
                        "inventory": {
                            "$xml_tag": "inventory",
                            "$pattern": {
                                "items": {
                                    "$xml_tag": "item",
                                    "$pattern": [
                                        {
                                            "name": {"$xml_attr": "name"},
                                            "modifiers": {
                                                "$xml_tag": "modifier",
                                                "$pattern": [
                                                    {
                                                        "type": {"$xml_attr": "type"},
                                                        "value": {"$xml_attr": "value"},
                                                    }
                                                ],
                                            },
                                        }
                                    ],
                                }
                            },
                        },
                    }
                ],
            }
        },
        {
            "players": [
                {
                    "id": "1",
                    "inventory": {
                        "items": [
                            {
                                "name": "Sword",
                                "modifiers": [
                                    {
                                        "type": "fire",
                                        "value": "10",
                                    },
                                    {
                                        "type": "speed",
                                        "value": "2",
                                    },
                                ],
                            },
                            {
                                "name": "Bow",
                                "modifiers": [
                                    {
                                        "type": "ice",
                                        "value": "5",
                                    }
                                ],
                            },
                        ]
                    },
                }
            ]
        },
    ),
    (
        current_dir / "missing_tag.xml",
        {"inventory": {"$xml_tag": "inventory", "$pattern": {}}},
        {"inventory": None},
    ),
]


@pytest.mark.parametrize(
    ("xml_file", "pattern", "expected"),
    test_cases,
)
def test_xml_parser(
    xml_file,
    pattern,
    expected,
) -> None:
    parser = UniversalXmlParser(
        file_path=str(xml_file),
        pattern=pattern,
    )

    result = parser.run()

    assert result == expected
