from pathlib import Path
from typing import Any
from xml.etree import ElementTree

from src.infrastructure.xml_parser.common.excs import XmlParserError


class UniversalXmlParser:
    """
    Универсальный декларативный парсер XML-файлов на основе мета-шаблона.

    Этот класс позволяет преобразовывать динамические и сложные XML-структуры
    в плоские или вложенные словари по заранее заданному шаблону (карте маппинга).
    Парсер полностью изолирует структуру итогового JSON/словаря от оригинальных имен
    тегов и атрибутов в XML-файле.

    Как строится шаблон (Словарь инструкций):
    Шаблон представляет собой словарь, где ключи — это желаемые названия ключей,
    а значения — специальные конфигурационные словари (метаданные),
    управляющие поиском в XML.

    Пример соответствия:
        <recipes>
            <recipe name="meleeToolRepairT0StoneAxe" count="1">
                <ingredient name="resourceWood" count="2"/>
                <ingredient name="resourceRockSmall" count="2"/>
            </recipe>
        </recipes>

        pattern = {
            "recipes": {
                "$xml_tag": "recipe",
                "$pattern": [
                    {
                        "item_id": {"$xml_attr": "name"},
                        "count_items": {"$xml_attr": "count"},
                        "required_materials": {
                            "$xml_tag": "ingredient",
                            "$pattern": [
                                {
                                    "material_id": {"$xml_attr": "name"},
                                    "quantity": {"$xml_attr": "count"},
                                }
                            ],
                        },
                    }
                ],
            }
        }
    """

    _ERROR_MESSAGE = (
        "Invalid pattern structure for key '{target_key}': {pattern_value}. "
        "Expected dict with '$xml_tag' or '$xml_attr'."
    )

    def __init__(
        self,
        file_path: str,
        pattern: dict[str, Any],
    ) -> None:
        self._file_path = Path(file_path)
        self._pattern = pattern

    def _parse_node(
        self,
        element: ElementTree.Element,
        pattern_node: dict[str, Any],
    ) -> dict[str, Any]:
        result = {}
        for target_key, pattern_value in pattern_node.items():
            if "$xml_tag" in pattern_value:
                xml_tag = pattern_value["$xml_tag"]
                sub_template = pattern_value["$pattern"]

                if isinstance(sub_template, list):
                    result[target_key] = [
                        self._parse_node(child, sub_template[0])
                        for child in element.findall(xml_tag)
                    ]

                else:
                    child = element.find(xml_tag)
                    result[target_key] = (
                        self._parse_node(child, sub_template)
                        if child is not None
                        else None
                    )

            elif "$xml_attr" in pattern_value:
                result[target_key] = element.get(pattern_value["$xml_attr"])

            else:
                raise XmlParserError(
                    self._ERROR_MESSAGE.format(
                        target_key=target_key,
                        pattern_value=pattern_value,
                    )
                )

        return result

    def run(self) -> dict[str, Any]:
        tree = ElementTree.parse(self._file_path)
        root = tree.getroot()
        return self._parse_node(root, self._pattern)
