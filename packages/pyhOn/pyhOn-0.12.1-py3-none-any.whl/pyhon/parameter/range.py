from typing import Dict, Any, List

from pyhon.parameter.base import HonParameter


def str_to_float(string: str | float) -> float:
    try:
        return int(string)
    except ValueError:
        return float(str(string).replace(",", "."))


class HonParameterRange(HonParameter):
    def __init__(self, key: str, attributes: Dict[str, Any], group: str) -> None:
        super().__init__(key, attributes, group)
        self._min: float = str_to_float(attributes["minimumValue"])
        self._max: float = str_to_float(attributes["maximumValue"])
        self._step: float = str_to_float(attributes["incrementValue"])
        self._default: float = str_to_float(attributes.get("defaultValue", self._min))
        self._value: float = self._default

    def __repr__(self):
        return f"{self.__class__} (<{self.key}> [{self._min} - {self._max}])"

    @property
    def min(self) -> float:
        return self._min

    @min.setter
    def min(self, min: float) -> None:
        self._min = min

    @property
    def max(self) -> float:
        return self._max

    @max.setter
    def max(self, max: float) -> None:
        self._max = max

    @property
    def step(self) -> float:
        if not self._step:
            return 1
        return self._step

    @step.setter
    def step(self, step: float) -> None:
        self._step = step

    @property
    def value(self) -> str | float:
        return self._value if self._value is not None else self._min

    @value.setter
    def value(self, value: str | float) -> None:
        value = str_to_float(value)
        if self._min <= value <= self._max and not (value - self._min) % self._step:
            self._value = value
            self.check_trigger(value)
        else:
            raise ValueError(
                f"Allowed: min {self._min} max {self._max} step {self._step}"
            )

    @property
    def values(self) -> List[str]:
        return [str(i) for i in range(int(self.min), int(self.max) + 1, int(self.step))]
