import uuid

import grpc

from . import errors
from .data_mappers import UserDataMapper
from .entities import User
from .proto import users_objects_pb2
from .proto import users_services_pb2
from .proto import users_services_pb2_grpc
from ..errors import UnknownError


class UsersService:
    def __init__(self, server_url: str):
        self.service_url = server_url

    def get_by_id(self, user_id: uuid.UUID) -> User:
        with grpc.insecure_channel(self.service_url) as channel:
            stub = users_services_pb2_grpc.UsersServiceStub(channel)
            request = users_services_pb2.GetByIdRequest(user_id=str(user_id))
            response = stub.GetById(request)
        if response.error == users_objects_pb2.Error.USER_NOT_FOUND:
            raise errors.UserNotFoundError()
        if response.error:
            raise UnknownError()
        return UserDataMapper.proto_model_to_entity(response.user)

    def create(self):
        with grpc.insecure_channel(self.service_url) as channel:
            stub = users_services_pb2_grpc.UsersServiceStub(channel)
            request = users_services_pb2.CreateRequest()
            response = stub.Create(request)
        if response.error:
            raise UnknownError()
        return UserDataMapper.proto_model_to_entity(response.user)
