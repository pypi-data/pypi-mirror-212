from dataclasses import dataclass, field
from pprint import pprint

@dataclass
class IdsBaseClass:
    """
        Base class used for all the IDS
    """

    @property
    def print_ids(self) -> object:
        """
            print IDS field values
        """
        pprint(f"current ids : {self}", indent=2)
        return None



