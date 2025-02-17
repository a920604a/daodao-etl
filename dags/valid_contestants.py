from config import default_args, mongo_uri, mongo_db_name, postgres_uri
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import User, Contact, Project
import json
import os
from typing import List

engine = create_engine(postgres_uri)
Session = sessionmaker(bind=engine)
session = Session()



def get_valid_contestants():

    # 假設 names_list 包含你要查找的名字列表
    with open("marathon.json", "r", encoding="utf-8") as f:
        config = json.load(f)
        names_list = config["paid_names_list"]



    matched_users = []

    for name in names_list:
        isExist = False
        for u in name.split("/"):
            users = session.query(User).filter_by(nickname=u).all()
            if users:
                isExist = True
                matched_users.extend([user.id for user in users])
                break  
            else:
                last_two_chars = u[-2:] 
                users = session.query(User).filter(User.nickname.like(f'%{last_two_chars}%')).all()
                if users:
                    isExist = True
                    matched_users.extend([user.id for user in users])
                    break 

        if not isExist:
            print(f"User with nickname '{name}' does not exist.")
    # assert len(names_list) == len(matched_users), "有人沒在 user 表格當中"
    
    return sorted(matched_users)
    
    
def get_marthon_user_list():
    result = session.query(User.id).join(Project, Project.user_id == User.id).all()
    user_ids = [row[0] for row in result]
    return sorted(user_ids)

def set_player_role_id(user_list : List, role_id = 3):
    session.execute(
            update(User).where(User.id.in_(user_list)).values(role_id=role_id)
        )
    session.commit()
    session.close()

if __name__ == "__main__":
    valid_user_list = get_valid_contestants()
    print("已繳款的使用者 ID :", valid_user_list, len(valid_user_list))
    
    marthon_user_list = get_marthon_user_list()
    print("註冊馬拉松的使用者 ID :", marthon_user_list, len(marthon_user_list))
    
    # 將列表轉換為集合並找出未入選的使用者（有效參賽者但沒有參與專案）
    invalid_users = set(marthon_user_list) - set(valid_user_list)
    print("「沒繳費」和「沒入選」的使用者 ID :", invalid_users, len(invalid_users))
    
    
    # 將已繳款的使用者 設定role_id = 3
    print("將已繳款的使用者 設定role_id = 3")
    set_player_role_id(valid_user_list)
        
    # 將繳費的使用者 並且 豬案在 project_marathon 的專案都設定為 公開
    
    # 未繳費 可以使用一個學習計畫，馬拉松參與者且繳費的 可以使用3個
    
    # 將繳費的使用者 