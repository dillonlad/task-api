from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select

from models import Task
from routers.task.data_structures import TaskOut, TaskInBM, MessageOut, UpdateTaskInBM
from components import db

router = APIRouter(prefix="/tasks")


@router.get("/", response_model=list[TaskOut])
async def get_tasks(
    completed: bool = None, 
    priority: int = None, 
    db_session=Depends(db.get_session),
):
    """
    Retrieve all tasks with optional filters.

    **Query Parameters:**
    - `completed` (bool, optional): Filter tasks by completion status.
    - `priority` (int, optional): Filter tasks by priority level.

    **Returns:**
    - A list of tasks matching the criteria.
    """

    _query = select(Task)
    if completed is not None:
        _query = _query.filter(Task.completed == completed)
    if priority is not None:
        _query = _query.filter(Task.priority == priority)

    tasks = db_session.execute(_query).scalars().all()

    return tasks


@router.get("/{task_id}/", response_model=TaskOut)
async def get_task(task_id: int, db_session=Depends(db.get_session)):
    """
    Retrieve a specific task by ID.

    **Path Parameter:**
    - `task_id` (int): The unique identifier of the task.

    **Returns:**
    - The requested task if found.

    **Raises:**
    - `HTTPException 404`: If the task ID does not exist.
    """

    _query = select(Task).filter(Task.id == task_id)
    task = db_session.execute(_query).scalars().first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.post("/", response_model=TaskOut)
async def create_task(task_params: TaskInBM, db_session=Depends(db.get_session)):
    """
    Create a new task.

    **Request Body:**
    - `title`: (str) The title of the task.
    - `description`: (str, optional) Task description.
    - `priority`: (int) Task priority (1 = High, 2 = Medium, 3 = Low).
    - `due_date`: (datetime) The due date for the task.
    - `completed`: (bool, default=False) Task completion status.

    **Returns:**
    - The created task with an assigned `id`.
    """

    try:
        task_db = Task(**task_params.model_dump())
        db_session.add(task_db)
        db_session.commit()
    except:
        db_session.rollback()
        raise HTTPException(status_code=500, detail="Database transaction failed.")

    return task_db


@router.put("/{task_id}/", response_model=TaskOut)
async def update_task(task_id: int, task_params: UpdateTaskInBM, db_session=Depends(db.get_session)):
    """
    Update an existing task.

    **Path Parameter:**
    - `task_id` (int): The ID of the task to update.

    **Request Body:**
    - Any field in the `Task` model can be updated.

    **Returns:**
    - The updated task object.

    **Raises:**
    - `HTTPException 404`: If the task ID does not exist.
    """

    _query = select(Task).filter(Task.id == task_id)

    task = db_session.execute(_query).scalars().first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update attributes in db model
    for key, value in task_params.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    try:
        db_session.commit()
        db_session.refresh(task)
    except:
        db_session.rollback()
        raise HTTPException(status_code=500, detail="Database transaction failed.")

    return task


@router.delete("/{task_id}/", response_model=MessageOut)
async def delete_task(task_id: int, db_session=Depends(db.get_session)):
    """
    Delete a task by ID.

    **Path Parameter:**
    - `task_id` (int): The ID of the task to delete.

    **Returns:**
    - A message confirming successful deletion.

    **Raises:**
    - `HTTPException 404`: If the task ID does not exist.
    """

    _query = select(Task).filter(Task.id == task_id)

    # Could possibly use delete statement on task_id instead of getting task from database first
    # for faster API response.
    task = db_session.execute(_query).scalars().first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        db_session.delete(task)
        db_session.commit()
    except:
        db_session.rollback()
        raise HTTPException(status_code=500, detail="Database transaction failed.")

    return MessageOut(message="Task deleted successfully.")
