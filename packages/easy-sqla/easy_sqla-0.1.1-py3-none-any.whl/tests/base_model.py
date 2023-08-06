from __future__ import annotations

from easy_sqla.db.settings import DBSettings
from easy_sqla.db.settings import DriverEnum
from easy_sqla.manager import Manager

test_settings = DBSettings(
    driver=DriverEnum.SQLITE,
)

base_model = Manager.as_base_model(test_settings)
