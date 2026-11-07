"""Read-only static card serving; renderers run only in an explicit batch build."""
from contextlib import contextmanager
from contextvars import ContextVar
from functools import wraps
import inspect
import hashlib
import json
import os
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
_BUILDING = ContextVar('building_cards', default=False)


class CardUnavailableError(RuntimeError):
    pass


def store_root():
    return Path(os.environ.get('HUNGER_CARD_STORE', ROOT / 'generated_cards')).resolve()


def normalize(value):
    if isinstance(value, str):
        value = unicodedata.normalize('NFKD', value.casefold())
        return re.sub(r'[^a-z0-9]', '', value)
    if isinstance(value, dict):
        # Some source skin records share a name/target but have different artwork
        # or ingredients. Preserve their full identity rather than serving the wrong card.
        variant = hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True).encode()).hexdigest()
        return [normalize(value.get('name', '')), normalize(value.get('target', '')), variant]
    if isinstance(value, (tuple, list)):
        return [normalize(v) for v in value]
    return value


def card_key(renderer, arguments):
    return json.dumps([renderer, normalize(list(arguments))], separators=(',', ':'), ensure_ascii=True)


@contextmanager
def building_cards():
    """Explicit, context-local bypass used by the offline batch generator only."""
    token = _BUILDING.set(True)
    try:
        yield
    finally:
        _BUILDING.reset(token)


def lookup(key):
    root = store_root()
    try:
        manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
        if manifest['version'] != 1:
            raise ValueError('unsupported manifest version')
        relative = manifest['cards'][key]
        path = (root / relative).resolve()
        if not path.is_relative_to(root) or not path.is_file() or path.stat().st_size == 0:
            raise ValueError('missing or invalid card file')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise CardUnavailableError(
            'This pre-generated card is unavailable. Ask the bot operator to run '
            '`python generate_cards.py` and deploy the generated_cards folder.'
        ) from exc
    return str(path)


def stored_card(*fields):
    """Keep the public renderer API, but serve only prebuilt files at runtime."""
    def decorate(fn):
        signature = inspect.signature(fn)
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if _BUILDING.get():
                return fn(*args, **kwargs)
            bound = signature.bind(*args, **kwargs)
            bound.apply_defaults()
            return lookup(card_key(fn.__name__, [bound.arguments[f] for f in fields]))
        wrapped.card_fields = fields
        wrapped.card_signature = signature
        return wrapped
    return decorate


def handle_missing_card(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except CardUnavailableError as exc:
            return {'spoken_text': 'That pre-generated card is not available yet.',
                    'display_text': str(exc), 'image_attachment': None}
    return wrapped
