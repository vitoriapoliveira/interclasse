from sqlalchemy import select
from database import Time, db_session


def select_todos():
    # buscar todos os times no banco
    # 1- montar o select
    times_sql = select(Time)
    # 2 - executar o select
    times = db_session.execute(times_sql).scalars().all()
    return times


def salvar(nome, turma, responsavel):
    try:
        time_novo = Time(nome=nome, responsavel=responsavel, turma=turma)
        db_session.add(time_novo)
        db_session.commit()
        flash(" time criado com sucesso", "success")

    except SQLAlchemyError as e:
        db_session.rollback()
        print(e)
        flash("ocorreu um erro tente novamente", "error")


    except Exception as e:
        db_session.rollback()
        flash("erro inesperado", "error")
        print(e)
