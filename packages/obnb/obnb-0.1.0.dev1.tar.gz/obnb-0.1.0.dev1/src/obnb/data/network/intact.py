from obnb.data.network.base import BaseNDExData
from obnb.typing import Converter


class IntAct(BaseNDExData):
    """The IntAct Molecular Interaction network."""

    cx_uuid = "fd15a70a-c7b5-11e4-951c-000c29cb28fb"

    def __init__(
        self,
        root: str,
        *,
        weighted: bool = False,
        directed: bool = False,
        largest_comp: bool = True,
        gene_id_converter: Converter = "HumanEntrez",
        **kwargs,
    ):
        """Initialize the BioGRID network data."""
        super().__init__(
            root,
            weighted=weighted,
            directed=directed,
            largest_comp=largest_comp,
            gene_id_converter=gene_id_converter,
            cx_kwargs={
                "interaction_types": ["interacts-with"],
                "node_id_entry": "n",
            },
            **kwargs,
        )
