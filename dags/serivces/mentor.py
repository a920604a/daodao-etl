
from config import postgres_uri
from sqlalchemy import create_engine, update, select
from sqlalchemy.orm import sessionmaker
from models import User, Contact
import json
from airflow.models import Variable


# engine = create_engine(postgres_uri)
# Session = sessionmaker(bind=engine)
# session = Session()



def set_mentor_role_id(session, role_id = 4):
    
    # with open("marathon.json", "r", encoding="utf-8") as f:
    #     config = json.load(f)
    #     email_list  = config["mentor_list"]
        
    email_list_str = Variable.get("mentor_list")
    email_list = json.loads(email_list_str)
    
    contact_ids = session.scalars(
            select(Contact.id).where(Contact.email.in_(email_list))
        ).all()
    
    if contact_ids:
        session.execute(
            update(User).where(User.contact_id.in_(contact_ids)).values(role_id=role_id)
        )
        session.commit()
        session.close()
    
def get_mentor_info(session):
    users = session.query(User).filter_by(role_id=4).all()
    print("\n".join(str(user) for user in users))
    
# if __name__ == "__main__":
#     set_mentor_role_id()
#     get_mentor_info()