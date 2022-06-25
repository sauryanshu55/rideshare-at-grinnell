from dataclasses import dataclass,field
from datetime import date,datetime, time

@dataclass
class RideSchema:
    _id: str
    requester_name: str
    request_date: datetime
    request_time: str
    request_destination: str
    round_trip: bool
    offered_compensation: int
    datetime_flexibility: str=None
    additional_comments:str=None
    completion_status:bool=False

@dataclass
class UserSchema:
    _id:str
    user_email:str
    username:str
    user_password:str
    rides_requested_by_user:list[str]=field(default_factory=list)



