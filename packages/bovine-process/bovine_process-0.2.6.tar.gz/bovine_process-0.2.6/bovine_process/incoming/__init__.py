from bovine.jsonld import with_external_context

from bovine_process.add_to_queue import add_to_queue
from bovine_process.utils.processor_list import ProcessorList

from .follow_accept import follow_accept
from .handle_update import handle_update
from .incoming_delete import incoming_delete
from .interactions import (
    announce_handler,
    delete_reply_handler,
    like_handler,
    reply_handler,
    undo_handler,
)
from .store_incoming import add_incoming_to_inbox, store_incoming


async def sanitize(item, actor):
    item.data = with_external_context(item.data)
    return item


default_inbox_process = (
    ProcessorList()
    .add(sanitize)
    .add_for_types(
        Create=store_incoming,
        Update=handle_update,
        Delete=incoming_delete,
        Accept=follow_accept,
    )
    .add(store_incoming)
    .add(add_incoming_to_inbox)
    .add_for_types(
        Announce=announce_handler,
        Create=reply_handler,
        Delete=delete_reply_handler,
        Dislike=like_handler,
        Like=like_handler,
        Undo=undo_handler,
        **{"http://litepub.social/ns#EmojiReact": like_handler}
    )
    .add(add_to_queue)
    .apply
)
