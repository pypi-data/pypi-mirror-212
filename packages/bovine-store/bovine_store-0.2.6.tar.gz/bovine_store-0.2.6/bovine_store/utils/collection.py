import logging

from quart import request, g

from .ordered_collection import ordered_collection_responder
from bovine_store.store.collection import collection_count, collection_items

logger = logging.getLogger(__name__)


async def collection_response(endpoint_path):
    arguments = {
        name: request.args.get(name)
        for name in ["first", "last", "min_id", "max_id"]
        if request.args.get(name) is not None
    }

    logger.info("Retrieving %s for %s", endpoint_path, g.retriever)

    async def ccount():
        return await collection_count(g.retriever, endpoint_path)

    async def citems(**kwargs):
        return await collection_items(g.retriever, endpoint_path, **kwargs)

    return await ordered_collection_responder(
        endpoint_path,
        ccount,
        citems,
        **arguments,
    )


def add_sub_collections(obj: dict) -> dict:
    obj_type = obj.get("type")
    obj_id = obj.get("id")
    if obj_type not in ["Note", "Article", "Page"] or not obj_id:
        return obj

    for key in ["replies", "shares", "likes"]:
        obj[key] = f"{obj_id}/{key}"

    return obj
