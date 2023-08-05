# solution.py

from typing import (
    Self, Iterable, Optional, Type, List
)

from represent import BaseModel

from genetic_algo.attributes import Attribute

__all__ = [
    "Solution",
    "Template",
    "eliminate_repetitions",
    "same_solution"
]

class Solution(BaseModel):
    """A class to represent a solution of a problem."""

    def __init__(self, attributes: Iterable[Attribute]) -> None:
        """
        Defines the class attributes.

        :param attributes: The attributes of the solution.
        """

        self.attributes = list(attributes)

        self.fitness: Optional[float] = None
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

        return (type(self) is type(other)) and all(
            attr1 == attr2 for attr1, attr2 in
            zip(self.attributes, other.attributes)
        )
    # end __eq__

    @classmethod
    def build(cls, attributes: Iterable[Attribute]) -> Self:
        """
        Builds the solution from the class.

        :param attributes: The attributes of the solution.

        :return: The solution object.
        """

        return Solution(attributes=attributes)
    # end build
# end Solution

def same_solution(*solutions: Solution) -> bool:
    """
    Checks if all the given solutions are the same.

    :param solutions: The solutions to check.

    :return: The value of equality.
    """

    for sol1, sol2 in zip(solutions[:-1], solutions[1:]):
        if sol1 == sol2:
            return False
        # end if
    # end for

    return True
# end same_solution

def eliminate_repetitions(solutions: Iterable[Solution]) -> List[Solution]:
    """
    Removes the repeated solutions.

    :param solutions: The solutions to filter.

    :return: The unique solutions.
    """

    unique: List[Solution] = []

    for slo1 in solutions:
        for sol2 in unique:
            if slo1 == sol2:
                break
            # end if

        else:
            unique.append(slo1)
        # end if
    # end for

    return unique
# end eliminate_repetitions

class Template(BaseModel):
    """A class to represent a template for solution attributes."""

    SOLUTION = Solution
    ATTRIBUTES: List[Attribute] = []

    def __init__(
            self,
            solution: Optional[Type[Solution]] = None,
            attributes: Optional[Iterable[Type[Attribute]]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param solution: The type of the solution object.
        :param attributes: The attributes of the solution.
        """

        self.solution = solution or self.SOLUTION

        self.attributes = list(attributes or []) or self.ATTRIBUTES
    # end __init__

    def build(self) -> Solution:
        """
        Generates the random attribute.

        :return: The attribute object.
        """

        return self.solution.build(
            attribute.build(
                *attribute.arguments.args,
                **attribute.arguments.kwargs
            )
            for attribute in self.attributes
        )
    # end build
# end Template