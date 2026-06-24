from src.domain.common.excs import DomainException


class EmptyMessageException(DomainException):
    pass


class MessageTooLongException(DomainException):
    pass
