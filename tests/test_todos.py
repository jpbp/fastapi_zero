from http import HTTPStatus
import factory
import factory.fuzzy
from fastapi_zero.models import Todo, TodoState


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo
    
    title = factory.faker('text')
    description = factory.faker('text')
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
        'id': 1
    }