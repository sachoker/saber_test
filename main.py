from typing import Union, Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from yaml_work import extract_and_load_yaml

app = FastAPI()


class Build(BaseModel):
    name: str


tasks = extract_and_load_yaml('builds/tasks.yaml', 'tasks')
builds = extract_and_load_yaml('builds/builds.yaml', 'builds')


def sort_tasks(task: str, task_list: dict) -> list:
    """
    Recursively sorts tasks based on dependencies.

    Parameters:
        task (str): The task to be sorted.
        task_list (dict): The list of tasks

    Returns:
        list: A list of tasks sorted based on their dependencies.
    """
    if task not in task_list:
        return []

    sorted_tasks = []
    for t in task_list[task]['dependencies']:
        sorted_tasks.extend(sort_tasks(t, task_list))
    sorted_tasks.append(task)
    return sorted_tasks


def build_queue(build: str, build_list: dict, task_list: dict) -> list:
    """
    Build the task order for a given build.

    Parameters:
        build (str): The name of the build.
        build_list (dict): The list of builds
        task_list (dict): The list of tasks

    Returns:
        list: The task order for the build.
    """
    task_order = []
    build_tasks = build_list.get(build, {}).get('tasks', [])
    for task in build_tasks:
        if task in task_list:
            task_order.extend(sort_tasks(task, task_list))
    return task_order


@app.post("/get_tasks")
async def get_tasks(build: Build) -> Union[Dict[str, str], List[str]]:
    if build.name not in builds:
        raise HTTPException(status_code=404, detail="Build not found")
    task_order = build_queue(build.name, builds, tasks)
    return task_order
