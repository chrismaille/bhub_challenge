from core.helpers.convert_keys import convert_keys
from core.helpers.only_numbers import only_numbers

SNAKE_CASE_DICT = {
    "user_id": "123",
    "last_access": None,
    "profile": {
        "email": "foo@bar.com",
        "last_update": "2021-10-12",
        "main_device": {"device_id": "1234"},
    },
    "device_list": [{"device_id": "1234", "device_info": [{"model_name": "Pixel 2"}]}],
    "tags": ["camel_case", "snake_case", None],
}
CAMEL_CASE_DICT = {
    "userId": "123",
    "lastAccess": None,
    "profile": {
        "email": "foo@bar.com",
        "lastUpdate": "2021-10-12",
        "mainDevice": {"deviceId": "1234"},
    },
    "deviceList": [{"deviceId": "1234", "deviceInfo": [{"modelName": "Pixel 2"}]}],
    "tags": ["camel_case", "snake_case", None],
}


def test_convert_keys():
    # Arrange

    # Act
    converted_camel_dict = convert_keys(
        SNAKE_CASE_DICT,
        to_case="camelcase",
        show_none=True,
    )
    converted_case_dict = convert_keys(
        CAMEL_CASE_DICT,
        to_case="snakecase",
        show_none=True,
    )

    # Assert
    assert converted_camel_dict == CAMEL_CASE_DICT
    assert converted_case_dict == SNAKE_CASE_DICT


def test_remove_nullable_keys():
    # Arrange
    snake_case_dict = {
        "user_id": "123",
        "profile": {
            "email": None,
            "last_update": "2021-10-12",
            "device": {"device_id": None},
        },
        "device_list": [{"device_id": None, "device_name": "foo"}, None],
    }
    camel_case_dict = {
        "userId": "123",
        "profile": {
            "lastUpdate": "2021-10-12",
            "device": {},
        },
        "deviceList": [{"deviceName": "foo"}, None],
    }

    # Act
    converted_camel_dict = convert_keys(
        snake_case_dict,
        to_case="camelcase",
        show_none=False,
    )

    # Assert
    assert converted_camel_dict == camel_case_dict


def test_only_numbers():
    # Act
    number = only_numbers("012.345.678-90")

    # Assert
    assert number == "01234567890"
