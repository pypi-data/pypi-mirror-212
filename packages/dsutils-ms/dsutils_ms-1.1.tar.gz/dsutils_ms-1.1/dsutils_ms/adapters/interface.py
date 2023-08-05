from abc import ABCMeta, abstractmethod
from typing import Any, Dict

from pyspark.sql import DataFrame


class ConnectorAdapterInterface(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        """Creates a new instance of Connector to load / save data.

        Args:
            name1: description1
            name2: description2
        """

        raise NotImplementedError("Should have implemented __init__ method!")

    @abstractmethod
    def load(self) -> DataFrame:
        """Loads data from somewhere.

        Returns:
            PySpark DataFrame.
        """

        raise NotImplementedError("Should have implemented _load method!")

    @abstractmethod
    def save(self, data: DataFrame) -> None:
        """Saves PySpark DataFrame to somewhere.

        Args:
            data: PySpark DataFrame to write.
        """

        raise NotImplementedError("Should have implemented _save method!")

    @abstractmethod
    def describe(self) -> Dict[str, Any]:
        """Returns a dict that describes the attributes of the dataset.

        Returns:
            Dictionary with all parameters.
        """

        return NotImplementedError("Should have implemented _describe method!")
