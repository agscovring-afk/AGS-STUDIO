from dataclasses import dataclass


@dataclass
class Tenant:

    id:int
    name:str
    status:str="active"
