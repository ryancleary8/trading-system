from typing import Type

from strategies.base.base_strategy import BaseStrategy


class StrategyRegistry:
    """
    Central registry for all available strategies.
    """

    def __init__(self) -> None:
        self._strategies: dict[str, Type[BaseStrategy]] = {}

    def register(
        self,
        name: str,
        strategy_class: Type[BaseStrategy],
    ) -> None:
        """
        Register a strategy class.
        """
        self._strategies[name] = strategy_class

    def get(
        self,
        name: str,
    ) -> Type[BaseStrategy]:
        """
        Retrieve a strategy class by name.
        """
        if name not in self._strategies:
            raise ValueError(
                f"Strategy '{name}' is not registered."
            )

        return self._strategies[name]

    def list_strategies(
        self,
    ) -> list[str]:
        """
        Return all registered strategy names.
        """
        return sorted(self._strategies.keys())