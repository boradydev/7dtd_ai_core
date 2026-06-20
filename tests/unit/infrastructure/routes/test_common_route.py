from src.infrastructure.routes.common import Route
from tests.unit.infrastructure.routes.conftest import FakeDTO


async def test_common_route(
    mock_parser_type,
    mock_first_case,
    mock_second_case,
    mock_logger,
) -> None:
    route = Route[FakeDTO](
        dto_type=FakeDTO,
        parser=mock_parser_type,
        logger=mock_logger,
    )
    route.add_case(mock_first_case)
    route.add_case(mock_second_case)
    assert len(route._cases) == 2

    fields = {
        "value1": "value1",
        "value2": "value2",
        "value3": "value3",
        "value4": "value4",
        "value5": "value5",
    }
    mock_parser_type.extract_fields.return_value = fields

    raw_line = "value1$value2$value3$value4$value5"
    data = route.extract(raw_line)
    assert data is not None
    assert data == fields

    await route.run(data)

    mock_first_case.execute.assert_called_once()
    mock_logger.error.assert_not_called()
    mock_second_case.execute.assert_called_once()

    called_dto = mock_first_case.execute.call_args[0][0]
    assert isinstance(called_dto, FakeDTO)
    assert called_dto.value1 == "value1"

    invalid_data = {"value1": "value1", "value2": "value2"}
    await route.run(invalid_data)
    mock_logger.error.assert_called_once()
