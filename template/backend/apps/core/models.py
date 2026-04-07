from __future__ import annotations

import uuid

from django.db import models


class BaseModel(models.Model):
    """
    Modelo base para todos los modelos de tenant.
    Provee id UUID, created_at y updated_at.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
