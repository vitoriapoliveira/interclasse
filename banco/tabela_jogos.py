from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import db_session, Jogador


def select_todos():
    jogadores_sql = select(Jogador)
    jogadores = db_session.execute(jogadores_sql).scalars().all()
    return jogadores

def salvar(nome,numero_camisa,posicao,time_id):
    try:
        jogador_novo =Jogador(nome=nome,numero_camisa=numero_camisa,posicao=posicao,time_id=time_id)
        db_session.add(jogador_novo)
        db_session.commit()
        flash("jogadores adicionado com sucesso", "success")
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("ocorreu um erro,tente novamente", "error")
        print(f"erro: {e}")
    except exception as e:
        db_session.rollback()
        flash("ocorreu um erro,tente novamente", "error")
        print(f"erro: {e}")

