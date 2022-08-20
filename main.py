
from fastapi import  Depends, FastAPI, Request


from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schema


models.Base.metadata.create_all(bind=engine)

app=FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





# revenue api
@app.post('/', tags=['Revenue'])
def create(req:schema.Access, db:Session=Depends(get_db)):
    reven= db.execute("SELECT revenue_target.`sno`,revenue_target.`branch`, (target), round(((`adm_revenue`.`total_net_revenue`/1000000)),2), round(((`adm_revenue`.`total_net_revenue`)/((`revenue_target`.`target`)*10000000)*1000),2),revenue_target.`clustername`, (status) FROM `revenue_target` INNER JOIN `adm_revenue` ON `adm_revenue`.`branch` = `revenue_target`.`branch` WHERE DATE(`adm_revenue`.`rdate`)='2022/07/21'GROUP BY `revenue_target`.`branch` ORDER BY (`revenue_target`.`sno`)")

    response=({"message":"successful","data":[]})

    for x in reven:
        response['data'].append({'sno':x[0], 'branch':x[1], 'target':x[2],'Achieved':x[3],'Achieved_percentage':x[4], 'clustername':x[5], 'status':x[6]})


    return response







