import requests
import uuid

ENDPOINT = "https://todo.pixegami.io/"


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_can_create_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    data = create_task_response.json()
    task_id = data["task"]["task_id"]

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]


def test_can_update_task():
    # create new task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    data = create_task_response.json()
    task_id = data["task"]["task_id"]

    # update task
    new_payload = {
        "content": "Ians updated task",
        "is_done": True,
        "user_id": payload["user_id"],
        "task_id": task_id,
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200

    # get updated task
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["user_id"] == new_payload["user_id"]


def test_can_list_tasks_for_user():
    # create N tasks
    n = 3
    payload = new_task_payload()

    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    list_task_response = list_tasks_for_user(payload["user_id"])
    assert list_task_response.status_code == 200
    data = list_task_response.json()
    tasks = data["tasks"]
    assert len(tasks) == n


def test_can_delete_task():
    # create new task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    data = create_task_response.json()
    task_id = data["task"]["task_id"]

    # delete task
    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    # try to get deleted task & check that it doesn't exist
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404


def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)


def get_task(task_id):
    return requests.get(ENDPOINT + f"get-task/{task_id}")


def delete_task(task_id):
    return requests.delete(ENDPOINT + f"delete-task/{task_id}")


def list_tasks_for_user(user_id):
    return requests.get(ENDPOINT + f"list-tasks/{user_id}")


def update_task(payload):
    return requests.put(ENDPOINT + "/update-task", json=payload)


def new_task_payload():
    # uses uuid to generate unique values so that tests can be successfully isolated from each other
    return {
        "content": f"test_content_{uuid.uuid4().hex}",
        "user_id": f"test_user_{uuid.uuid4().hex}",
        "is_done": False,
    }
