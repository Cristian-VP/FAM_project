from fastapi import APIRouter, Body, Request, HTTPException, status
from models import TaskBase, TaskCreate, TaskUpdate
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.get('/', response_description="Listar todas las tareas")
async def list_tasks(request: Request):
    Tasks = request.app.mongodb['tasks']
    tasks = []
    async for task in Tasks.find({}):
        tasks.append(TaskBase(**task))
    return tasks

@router.post('/', response_description="Crear una tarea")
async def create_task(request: Request, task: TaskCreate = Body(...)):
    Tasks = request.app.mongodb['tasks']
    # Verifica si ya existe una tarea con el mismo título
    if await Tasks.find_one({'title': task.title}):
        raise HTTPException(status_code=400, detail=f"Tarea '{task.title}' ya existe.")
    # Construye el objeto TaskBase con todos los campos requeridos
    task_data = TaskBase(**task.dict())
    # Inserta el documento usando los alias correctos para MongoDB
    await Tasks.insert_one(task_data.model_dump(by_alias=True))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(task_data))

@router.patch('/{id}', response_description="Actualizar una tarea")
async def update_task(id: str, request: Request, task: TaskUpdate = Body(...)):
    Tasks = request.app.mongodb['tasks']
    task = task.dict(exclude_unset=True, by_alias=True)
    if 'title' in task and not task['title']:
        raise HTTPException(status_code=400, detail="El título no puede estar vacío.")
    if not await Tasks.find_one({"_id": id}):
        raise HTTPException(status_code=404, detail=f"Tarea con ID:{id} no encontrada.")
    updated_result = await Tasks.update_one({"_id": id}, {"$set": task})
    if updated_result.modified_count == 1:
        updated_task = await Tasks.find_one({"_id": id})
        return updated_task
    raise HTTPException(status_code=400, detail="No se pudo actualizar la tarea.")

@router.delete("/{id}", response_description="Eliminar tarea")
async def delete_task(id: str, request: Request):
    Tasks = request.app.mongodb['tasks']
    delete_result = await Tasks.delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Tarea con ID:{id} no encontrada.")