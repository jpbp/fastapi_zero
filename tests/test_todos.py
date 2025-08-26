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
