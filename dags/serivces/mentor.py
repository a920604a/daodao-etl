
from config import postgres_uri
from sqlalchemy import create_engine, update, select
from sqlalchemy.orm import sessionmaker
from models import User, Contact, MentorParticipants
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
    
def get_mentor_info(session, role_id):
    users = session.query(User).filter_by(role_id=role_id).all()
    print("\n".join(str(user) for user in users))
    return users

def get_mentor_map_dict(session):
    
    mentor_mapping = Variable.get("mentor_mapping")
    mentor_map = json.loads(mentor_mapping)
    print(mentor_map)
    ret = {}
    for mentor_email, player_names in mentor_map.items():
        
        mentor_contact = session.query(Contact).filter_by(email = mentor_email).first()
        if mentor_contact:
            mentor_user = session.query(User).filter_by(contact_id = mentor_contact.id).first()
        
            ret[mentor_user.id] = list()
            
            for name in player_names:
                    isExist = False
                    for u in name.split("/"):
                        users = session.query(User).filter_by(nickname=u).all()
                        if users:
                            isExist = True
                            ret[mentor_user.id].extend([user.id for user in users])
                            break  
                        else:
                            last_two_chars = u[-2:] 
                            users = session.query(User).filter(User.nickname.like(f'%{last_two_chars}%')).all()
                            if users:
                                isExist = True
                                ret[mentor_user.id].extend([user.id for user in users])
                                break 

                    if not isExist:
                        print(f"User with nickname '{name}' does not exist.")
        print(f"{mentor_email} :{ret}")
        
    return ret
    
    
def insert_participant_into_mentor(session, mentor_participant:dict):
    # mentor_participants
    for mentor, participants in mentor_participant.items():
        print(f"mentor :{mentor}")
        for participant in participants:
            session.add(MentorParticipants(
                mentor_id = mentor,
                participant_id = participant
            ))
            session.commit()
            # print(f" mentor is { mentor }, participant {participant}")
      
    
    
    
    
    
# if __name__ == "__main__":
#     set_mentor_role_id()
#     get_mentor_info()