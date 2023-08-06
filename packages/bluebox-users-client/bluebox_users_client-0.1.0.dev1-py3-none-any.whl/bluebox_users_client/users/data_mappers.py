import uuid

from .entities import User
from .proto import users_objects_pb2


class UserDataMapper:
    @staticmethod
    def proto_model_to_entity(proto_model: users_objects_pb2.User) -> User:
        return User(
            user_id=uuid.UUID(proto_model.user_id),
            email=proto_model.email,
            balance=proto_model.balance,
        )
