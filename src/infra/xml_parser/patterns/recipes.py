PATTERN = {
    "recipes": {
        "$xml_tag": "recipe",
        "$pattern": [
            {
                "key": {"$xml_attr": "name"},
                "output_count": {"$xml_attr": "count"},
                "craft_station": {"$xml_attr": "craft_area"},
                "required_ingredients": {
                    "$xml_tag": "ingredient",
                    "$pattern": [
                        {
                            "name": {"$xml_attr": "name"},
                            "quantity": {"$xml_attr": "count"},
                        }
                    ],
                },
            }
        ],
    }
}
