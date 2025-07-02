from dataclasses import asdict

from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='test', email='test@test.com', password='secret'
        )
        session.add(new_user)
        session.commit()
        user = session.scalar(select(User).where(User.username == 'test'))
        assert asdict(user) == {
            'id': 1,
            'username': 'test',
            'email': 'test@test.com',
            'password': 'secret',
            'created_at': time,
            'updated_at': time,
        }


def test_get_session_returns_session():
    """Testa se get_session retorna uma instancia de Session valida."""
    session_generator = get_session()
    session = next(session_generator)

    # Verifica se e uma instancia de Session
    assert isinstance(session, Session)

    # Verifica se a sessao esta ativa
    assert session.is_active

    # Finaliza o generator para fechar a sessao
    try:
        next(session_generator)
    except StopIteration:
        pass  # Esperado quando o generator termina/exit
