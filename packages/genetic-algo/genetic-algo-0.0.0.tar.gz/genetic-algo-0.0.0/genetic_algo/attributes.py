# attributes.py

from typing import (
    Self, Iterable, Any, Optional, Type, Union
)
import string
import random
from abc import ABCMeta

from represent import BaseModel

__all__ = [
    "Arguments",
    "Attribute",
    "NumericAttribute",
    "StringAttribute",
    "IntegerAttribute",
    "FloatAttribute"
]

class Arguments(BaseModel):
    """A class to represent a fitness function."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Calls the fitness function on the solution.

        :param args: Any positional arguments.
        :param kwargs: Any keyword arguments.
        """

        self.args = args or ()
        self.kwargs = kwargs or {}

        self.update(*args, **kwargs)
    # end __init__

    def update(self, *args: Any, **kwargs: Any) -> None:
        """
        Calls the fitness function on the solution.

        :param args: Any positional arguments.
        :param kwargs: Any keyword arguments.
        """

        self.args = args or self.args
        self.kwargs = kwargs or self.kwargs
    # end update

    def copy(self) -> Self:
        """
        Returns a copy of the definition object.

        :return: The new definition object.
        """

        return Arguments(*self.args, **self.kwargs)
    # end copy
# end Arguments

class Attribute(BaseModel, metaclass=ABCMeta):
    """A class to represent an attribute of a solution."""

    NAME: Optional[str] = None

    EXCLUDED: Iterable[Any] = []

    arguments = Arguments()

    def __init__(self, value: Any, name: Optional[str] = None) -> None:
        """
        Defines the class attributes.

        :param value: The value of the attribute.
        :param name: The name of the attribute.
        """

        self.name = name or self.NAME

        self.value = value
    # end __init__

    def __hash__(self) -> int:
        """
        Returns the hash of the object.

        :return: The hash of the object.
        """

        return id(self)
    # end __hash__

    def __eq__(self, other: Self) -> bool:
        """
        Checks if the solutions are equal.

        :param other: The other solution.

        :return: The equality value.
        """

        return (
            (type(self) is type(other)) and
            (self.name == other.name) and
            (self.value == other.value)
        )
    # end __eq__

    @classmethod
    def build(cls, *args: Any, **kwargs: Any) -> Self:
        """
        Generates the random attribute.

        :param args: Any positional arguments.
        :param kwargs: Any keyword arguments.

        :return: The attribute object.
        """

        while (value := cls.generate(*args, **kwargs)) in cls.EXCLUDED:
            pass
        # end while

        return cls(value=value)
    # end build

    @classmethod
    def generate(cls, *args: Any, **kwargs: Any) -> Any:
        """
        Generates the random attribute value.

        :param args: Any positional arguments.
        :param kwargs: Any keyword arguments.

        :return: The attribute value.
        """
    # end generate
# end Attribute

Number = Union[int, float]

class NumericAttribute(Attribute):
    """A class to represent an attribute of a solution."""

    BASE: Type[Number] = float

    FLOOR: Number = None
    ROOF: Number = None
    STEP: Optional[Number] = None

    @classmethod
    def generate(
            cls,
            base: Optional[Type[Number]] = None,
            floor: Optional[Number] = None,
            roof: Optional[Number] = None,
            step: Optional[Number] = None
    ) -> Number:
        """
        Generates the random attribute value.

        :param base: The type of the number.
        :param floor: The floor limit value.
        :param roof: The roof limit value.
        :param step: The step size.

        :return: The attribute value.
        """

        if base is None:
            base = cls.BASE
        # end if

        if floor is None:
            floor = cls.FLOOR
        # end if

        if roof is None:
            roof = cls.ROOF
        # end if

        if step is None:
            step = cls.STEP
        # end if

        if issubclass(base, int):
            floor = int(floor)
            roof = int(roof)

            if step is None:
                return random.randint(floor, roof)

            elif isinstance(step, int):
                return random.choice(range(floor, roof, step))

            else:
                raise ValueError(
                    f"{cls} 'step' must be an int when "
                    f"'base' is an int, not {step}."
                )
            # end if

        elif issubclass(base, float):
            if step is None:
                return random.uniform(floor, roof)

            elif isinstance(step, (int, float)):
                values = [floor]

                while values[-1] <= roof:
                    values.append(values[-1] + step)
                # end while

                return random.choice(values)

            else:
                raise ValueError(
                    f"{cls} 'step' must be an int or a float when "
                    f"'base' is an int, not {step}."
                )
            # end if

        else:
            raise ValueError(
                f"{cls} 'base' must be an int "
                f"or a float when , not {base}."
            )
        # end if
    # end generate
# end NumericAttribute

class IntegerAttribute(NumericAttribute):
    """A class to represent an attribute of a solution."""

    BASE = int

    FLOOR = 0
    ROOF = 100
    STEP = 1
# end IntegerAttribute

class FloatAttribute(NumericAttribute):
    """A class to represent an attribute of a solution."""

    BASE = float

    FLOOR = 0.0
    ROOF = 1.0
    STEP = 0.01
# end FloatAttribute

class StringAttribute(Attribute):
    """A class to represent an attribute of a solution."""

    SOURCE: Iterable[str] = string.ascii_lowercase
    SEPARATOR: str = ""

    LENGTH: int = 10

    @classmethod
    def generate(
            cls,
            source: Optional[Iterable[str]] = None,
            separator: Optional[str] = None,
            length: Optional[int] = None
    ) -> str:
        """
        Generates the random attribute value.

        :param source: The source string.
        :param separator: The separator string.
        :param length: The length of the string.

        :return: The attribute value.
        """

        if source is None:
            source = cls.SOURCE
        # end if

        if separator is None:
            separator = cls.SEPARATOR
        # end if

        if length is None:
            length = cls.LENGTH
        # end if

        try:
            if not all(isinstance(s, str) for s in source):
                raise ValueError
            # end if

        except ValueError:
            raise ValueError(
                f"{cls} 'source' must be an iterable "
                f"of string type values, not {source}."
            )
        # end try

        if not isinstance(length, int):
            raise ValueError(
                f"{cls} 'length' must be an int, not {length}."
            )
        # end if

        if not isinstance(separator, str):
            raise ValueError(
                f"{cls} 'separator' must be a string, not {separator}."
            )
        # end if

        return separator.join(random.choices(list(source), k=length))
    # end generate
# end StringAttribute

class BooleanAttribute(Attribute):
    """A class to represent an attribute of a solution."""

    @classmethod
    def generate(cls) -> str:
        """
        Generates the random attribute value.

        :return: The attribute value.
        """

        return random.choice([True, False])
    # end generate
# end BooleanAttribute