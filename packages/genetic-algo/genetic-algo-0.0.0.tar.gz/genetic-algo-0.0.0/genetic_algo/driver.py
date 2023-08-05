# driver.py

from typing import Self, Optional, List
from collections.abc import Iterator

from represent import BaseModel

from genetic_algo.environment import scale, Environment, Generation

__all__ = [
    "Driver",
    "DriverDefinition"
]

class DriverDefinition(BaseModel):
    """A class to contain the definition values of a driver object."""

    def __init__(
            self,
            fitness_limit: float,
            max_generations: int,
            min_improvement: float,
            min_count: Optional[int] = None
    ) -> None:
        """
        Defines the class attributes.

        :param fitness_limit: The maximum fitness to stop at.
        :param max_generations: The maximum amount of generations to stop at.
        :param min_improvement: The minimum improvement to stop at.
        :param min_count: The minimum count of solutions before stopping.
        """

        if min_count is None:
            min_count = 1
        # end if

        self.fitness_limit = fitness_limit
        self.max_generations = max_generations
        self.count_limit = min_count

        self.min_improvement = scale(
            min_improvement, size=1, name="minimum improvement"
        )
    # end __init__

    def copy(self) -> Self:
        """
        Returns a copy of the definition object.

        :return: The new definition object.
        """

        return DriverDefinition(
            fitness_limit=self.fitness_limit,
            max_generations=self.max_generations,
            min_improvement=self.min_improvement
        )
    # end copy
# end DriverDefinition

class Driver(BaseModel):
    """A class to represent a driver for genetic algorithm environments."""

    def __init__(
            self,
            definition: DriverDefinition,
            environment: Environment
    ) -> None:
        """
        Defines the class attributes.

        :param definition: The definition object.
        :param environment: The environment object.
        """

        self.definition = definition
        self.environment = environment
    # end __init__

    def next(self, generation: Optional[Generation] = None) -> Generation:
        """
        Generates the next generation of solutions based on the given one.

        :param generation: The base generation of solutions.

        :return: The next generation.
        """

        if not generation.solutions:
            return generation
        # end if

        generation = self.environment.next(generation=generation)

        return generation
    # end next

    def generate(self, generation: Optional[Generation] = None) -> Iterator[Generation]:
        """
        Generates the next generation of solutions based on the given one.

        :param generation: The base generation of solutions.

        :return: The next generation.
        """

        previous = None
        generation = generation or self.environment.generation

        for _ in range(self.definition.max_generations):
            if self.finish(generation=generation):
                break
            # end if

            before = previous
            previous = generation
            generation = self.next(generation=generation)

            if (
                self.finish(generation=generation) or
                self.stop(generation=previous, previous=before)
            ):
                break
            # end if

            yield generation
        # end while

        yield generation if generation.solutions else previous
    # end generate

    def run(self, generation: Optional[Generation] = None) -> List[Generation]:
        """
        Generates the next generation of solutions based on the given one.

        :param generation: The base generation of solutions.

        :return: The next generation.
        """

        return list(self.generate(generation=generation))
    # end run

    def finish(self, generation: Generation) -> bool:
        """
        Checks the value to stop the process.

        :param generation: The current generation.

        :return: The value to stop the process.
        """

        return (
            (not generation.solutions) or
            (
                isinstance(self.definition.count_limit, int) and
                (self.definition.count_limit >= len(generation.solutions))
            )
        )
    # end finish

    def stop(self, generation: Generation, previous: Optional[Generation] = None) -> bool:
        """
        Checks the value to stop the process.

        :param generation: The current generation.
        :param previous: The previous generation.

        :return: The value to stop the process.
        """

        order = max if self.environment.definition.ascending else min

        limited = all(
            (
                (fitness < self.definition.fitness_limit)
                if self.environment.definition.ascending else
                (fitness > self.definition.fitness_limit)
            ) for fitness in generation.fitness.values()
        )

        improved = True

        if (
            isinstance(generation, Generation) and
            isinstance(previous, Generation) and
            generation.fitness and
            previous.fitness
        ):
            base = order(previous.fitness.values())
            change = (order(generation.fitness.values()) - base) / base

            improved = (
                change >= self.definition.min_improvement
                if self.environment.definition.ascending else
                change <= self.definition.min_improvement
            )
        # end if

        return not (
            (len(generation.solutions) > 0) and limited and improved
        )
    # end stop
# end Driver