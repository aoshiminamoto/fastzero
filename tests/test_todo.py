from http import HTTPStatus

from fastzero.factories import TodoFactory
from fastzero.models import TodoState
from fastzero.schemas import TodoPublic


def test_create_todo(client, todo, token):
    response = client.post(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
        json=TodoPublic.model_validate(todo).model_dump(),
    )

    todo.id += 1  # Monkey Patch
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == TodoPublic.model_validate(todo).model_dump()


def test_read_todo_by_id(client, todo, token):
    response = client.get(
        "/todos/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == TodoPublic.model_validate(todo).model_dump()


def test_read_todo_by_id_not_found(client, token):
    response = client.get(
        "/todos/0",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_list_todos_should_return_5_todos(session, client, user, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    expected_todos = 5
    session.commit()

    response = client.get(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_pagination_should_return_2_todos(session, user, client, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    expected_todos = 2
    session.commit()

    response = client.get(
        "/todos/?offset=1&limit=2",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_filter_title_should_return_5_todos(session, user, client, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id, title="Test todo 1"))
    expected_todos = 5
    session.commit()

    response = client.get(
        "/todos/?title=Test todo 1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_filter_description_should_return_5_todos(session, user, client, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id, description="description"))
    expected_todos = 5
    session.commit()

    response = client.get(
        "/todos/?description=desc",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_filter_state_should_return_5_todos(session, user, client, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft))
    expected_todos = 5
    session.commit()

    response = client.get(
        "/todos/?state=draft",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_filter_combined_should_return_5_todos(session, user, client, token):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title="Test todo combined",
            description="combined description",
            state=TodoState.done,
        )
    )

    session.bulk_save_objects(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title="Other title",
            description="other description",
            state=TodoState.todo,
        )
    )
    session.commit()

    response = client.get(
        "/todos/?title=Test todo combined&description=combined&state=done",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_delete_todo(session, client, user, token, todo):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.delete(f"/todos/{todo.id}", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Task has been deleted successfully."}


def test_delete_todo_error(client, token):
    response = client.delete(f"/todos/{10}", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Task not found."}


def test_patch_todo_error(client, token):
    response = client.patch(
        "/todos/10",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Task not found."}


def test_patch_todo(session, client, user, token, todo):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.patch(
        f"/todos/{todo.id}",
        json={"title": "teste!"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == "teste!"
