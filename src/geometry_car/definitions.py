"""Dagster entrypoint. The code server and `dagster dev` both load this module.

Assets land here as they are written; the object exists from the scaffold on so
the image, the code server and the local UI all have something to load.
"""

from dagster import Definitions

defs = Definitions(assets=[])
