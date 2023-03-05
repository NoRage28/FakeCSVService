from celery import shared_task
from schema.services import DatasetCreator
from django.core.cache import cache
from typing import Dict, Any
from datetime import datetime


@shared_task()
def create_dataset_task(
        cache_task_id: str, user_id: str, data: Dict[str, Any], schema_pk: str
):
    try:
        cache.set(cache_task_id, {"ready": False, "errors": []})
        DatasetCreator().create_dataset(user_id=user_id, data=data, schema_pk=schema_pk)
    except Exception as exc:
        cache.set(cache_task_id, {"ready": False, "errors": [exc.args]})
    else:
        cache.set(cache_task_id, {"ready": True, "errors": []})


def start_create_dataset_task(user_id: str, data: Dict[str, Any], schema_pk: str):
    cache_task_key = str(datetime.utcnow().timestamp())
    create_dataset_task.delay(cache_task_key, user_id, data, schema_pk)
    return cache_task_key
