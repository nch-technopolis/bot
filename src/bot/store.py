import os
import json
import tempfile
from collections import defaultdict
from contextlib import suppress
from pathlib import Path
from threading import Lock

from .config import STORE_PATH

__all__ = [
    'get_vk_access_token',
    'save_vk_access_token',
    'get_chats',
    'add_chat',
    'remove_chat',
    'publish_update',
    'get_update',
]

ROOT = Path(STORE_PATH or tempfile.mkdtemp())
if not ROOT.exists():
    os.makedirs(ROOT, exist_ok=True)

VK_CODE_PATH = ROOT / 'vk.code'

CHATS_PATH = ROOT / 'chats'
CHATS_LOCK = Lock()

QUEUE_POINTER_PATH = ROOT / 'queue.pointer'
QUEUE_PATH = ROOT / 'queue'
QUEUE_LOCK = Lock()


def _save_object(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(obj, f)


def _read_object(path, fallback=None):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return fallback


def save_vk_access_token(token):
    _save_object(VK_CODE_PATH, token)


def get_vk_access_token():
    return _read_object(VK_CODE_PATH, defaultdict(lambda: None))


def add_chat(chat_id):
    with CHATS_LOCK:
        chats = get_chats()
        if chat_id not in chats:
            chats.append(chat_id)
        _save_object(CHATS_PATH, chats)


def get_chats():
    return _read_object(CHATS_PATH, [])


def remove_chat(chat_id):
    with CHATS_LOCK:
        chats = get_chats()
        with suppress(ValueError):
            chats.remove(chat_id)


def _get_queue_pointer():
    return _read_object(QUEUE_POINTER_PATH, 0)


def _set_queue_pointer(pointer):
    _save_object(QUEUE_POINTER_PATH, pointer)


def publish_update(update):
    with QUEUE_LOCK:
        pointer = _get_queue_pointer()
        pointer += 1
        _save_object(QUEUE_PATH / str(pointer), update)
        _set_queue_pointer(pointer)


def get_update():
    pointer = _get_queue_pointer()
    update_path = QUEUE_PATH / str(pointer)
    with QUEUE_LOCK:
        update = _read_object(update_path, None)
        with suppress(FileNotFoundError):
            os.unlink(update_path)
    return update
