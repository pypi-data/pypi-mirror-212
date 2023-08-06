from typing import Any, List, Optional
from rekuest.postmans.utils import RPCContract
from fluss.api.schema import LocalNodeFragment
from reaktion.atoms.generic import MapAtom, MergeMapAtom
from reaktion.events import Returns
import logging

logger = logging.getLogger(__name__)


class LocalMapAtom(MapAtom):
    node: LocalNodeFragment
    contract: RPCContract

    async def map(self, args: Returns) -> Optional[List[Any]]:
        defaults = self.node.defaults or {}

        stream_one = self.node.instream[0]
        for arg, item in zip(args, stream_one):
            defaults[item.key] = arg

        returns = await self.contract.aassign_retry(
            kwargs={**defaults, **self.globals}, parent=self.assignment
        )

        out = []
        stream_one = self.node.outstream[0]
        for arg in stream_one:
            out.append(returns[arg.key])
        return out
        # return await self.contract.aassign(*args)


class LocalMergeMapAtom(MergeMapAtom):
    node: LocalNodeFragment
    contract: RPCContract

    async def merge_map(self, args: Returns) -> Optional[List[Any]]:
        defaults = self.node.defaults or {}

        stream_one = self.node.instream[0]
        for arg, item in zip(args, stream_one):
            defaults[item.key] = arg

        async for returns in self.contract.astream_retry(
            kwargs={**defaults, **self.globals}, parent=self.assignment
        ):
            out = []
            stream_one = self.node.outstream[0]
            for arg in stream_one:
                out.append(returns[arg.key])
            yield out
