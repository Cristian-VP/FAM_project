from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
import uuid

# Enum que define los posibles estados de una tarea
class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

# Modelo base que representa una tarea en la aplicación
class TaskBase(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id", description="ID único de la tarea")
    title: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: TaskStatus = Field(default=TaskStatus.pending)
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")
    due_date: Optional[datetime] = Field(default=None, alias="dueDate")
    tags: Optional[List[str]] = Field(default=None, description="Etiquetas para organizar tareas")

    class Config:
        allow_population_by_field_name = True

# Modelo para la creación de una tarea (campos requeridos y opcionales)
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None

# Modelo para la actualización de una tarea (todos los campos opcionales)
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow, alias="updatedAt")