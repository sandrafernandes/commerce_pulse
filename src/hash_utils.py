import hashlib
import json


def generate_event_id(event_type: str, event_time: str, vendor: str, payload: dict) -> str:
    """
    Gera um event_id determinístico baseado no conteúdo do evento.
    """
    normalized_payload = json.dumps(payload, sort_keys=True)

    raw_string = f"{event_type}|{event_time}|{vendor}|{normalized_payload}"

    return hashlib.sha256(raw_string.encode("utf-8")).hexdigest()
