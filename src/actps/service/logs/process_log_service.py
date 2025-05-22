import json
from typing import Dict

from pydantic import BaseModel
from src.actps.core.unit_of_work import UnitOfWork
from src.actps.domain.logs import ProcessLog


class ProcessLogService:

    async def create_process_log(
        self,
        data: BaseModel,
        uow: UnitOfWork,
    ):

        process_log = ProcessLog(
            name=data.name, 
            path=f"files/{data.name}.json",
            pred=data.pred
        )
        print(process_log)
        
        async with uow as uow:
            await uow.add(process_log)
            await uow.commit()

        with open(f"files/{data.name}.json", "w") as f:
            json.dump(data.report, f)
