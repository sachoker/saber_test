from unittest import TestCase, main

from fastapi.testclient import TestClient

from main import app, sort_tasks, build_queue
from yaml_work import extract_and_load_yaml


class TestWeb(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self) -> None:
        self.client.close()

    def test_get_tasks(self):
        response = self.client.post("/get_tasks", json={"build": "test_build"})
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(),
                          ["pack_game_files", "pack_docker", "pack_server_files", "build_exe", "pack_in_zip"])

    def test_get_tasks_non_existent_build(self):
        response = self.client.post("/get_tasks", json={"build": "non_existent_build"})
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), {"error": "Build not found"})


class TestSortingTasksDependencies(TestCase):
    def test_sort_tasks(self):
        # Testing when the task is not in tasks
        self.assertEqual(sort_tasks("task1", {}), [])

    def test_sort_tasks_with_no_dependencies(self):
        # Testing when the task has no dependencies
        tasks = {
            "task1": {'dependencies': []},
        }
        self.assertEqual(sort_tasks("task1", tasks), ['task1'])

    def test_sort_tasks_with_dependencies(self):
        # Testing when the task has dependencies
        tasks = {
            "task1": {"dependencies": ["task2"]},
            "task2": {"dependencies": ["task3"]},
            "task3": {'dependencies': []},
        }
        self.assertEqual(["task3", "task2", 'task1'], sort_tasks("task1", tasks))

    def test_sort_tasks_with_multiple_dependencies(self):
        # Testing when the task has multiple dependencies
        tasks = {
            "task1": {'dependencies': ["task2", "task3"]},
            "task2": {"dependencies": ["task4"]},
            "task3": {"dependencies": ["task4"]},
            "task4": {'dependencies': []}
        }
        self.assertEqual(["task4", "task2", 'task4', "task3", 'task1'], sort_tasks("task1", tasks))


class TestBuildQueue(TestCase):
    def test_build_queue(self):
        builds = {
            "test_build": {
                "tasks": ["build_exe", "pack_in_zip"]
            }
        }
        tasks = extract_and_load_yaml("builds/tasks.yaml", "tasks")
        self.assertEqual(["pack_game_files", "pack_docker", "pack_server_files", "build_exe", "pack_in_zip"],
                         build_queue("test_build", builds, tasks))


if __name__ == '__main__':
    main()
