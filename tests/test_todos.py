from http import HTTPStatus

import factory
import factory.fuzzy
import pytest

from fastapi_zero.models import Todo, TodoState


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


def test_created_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Titulo de exemplo',
            'description': 'Descrição de exemplo',
            'state': 'draft',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'title': 'Titulo de exemplo',
        'description': 'Descrição de exemplo',
        'state': 'draft',
        'id': 1,
    }


@pytest.mark.asyncio
async def test_list_todos_should_return_5_todos(session, client, user, token):
    except_todos = 5
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos',  # sem query
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == except_todos


@pytest.mark.asyncio
async def test_list_todos_pagination_should_return_2_todos(
    session, client, user, token
):
    except_todos = 2
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',  # sem query
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == except_todos


@pytest.mark.asyncio
async def test_list_todos_filter_title_return(session, client, user, token):
    except_todos = 5
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, title='Test Todo Title 1')
    )
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos/?title=Test Todo Title 1',  # sem query
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == except_todos


@pytest.mark.asyncio
async def test_list_todos_filter_description_return(
    session, client, user, token
):
    except_todos = 5
    session.add_all(
        TodoFactory.create_batch(
            5, user_id=user.id, description='Test Todo Description 1'
        )
    )
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos/?description=Test Todo Description 1',  # sem query
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == except_todos


@pytest.mark.asyncio
async def test_list_todos_filter_states_return(session, client, user, token):
    except_todos = 5
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, state='draft')
    )
    session.add_all(TodoFactory.create_batch(5, user_id=user.id, state='todo'))
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, state='doing')
    )
    session.add_all(TodoFactory.create_batch(5, user_id=user.id, state='done'))
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, state='trash')
    )

    await session.commit()
    response = client.get(
        '/todos/?state=todo',  # sem query
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == except_todos

    response = client.get(
        '/todos/?state=draft',  # sem query
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == except_todos

    response = client.get(
        '/todos/?state=doing',  # sem query
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == except_todos

    response = client.get(
        '/todos/?state=done',  # sem query
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == except_todos

    response = client.get(
        '/todos/?state=trash',  # sem query
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == except_todos


def test_delete_todo_error(client, token):
    response = client.delete(
        '/todos/10', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


@pytest.mark.asyncio
async def test_delete_todo(client, session, token, user):
    todo = TodoFactory.create(user_id=user.id)
    session.add(todo)
    await session.commit()
    response = client.delete(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task has been deleted successfuly'}
