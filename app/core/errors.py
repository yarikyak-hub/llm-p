# Собственные исключения приложения.

class AppException(Exception):
    """Базовое исключение приложения. Все доменные ошибки наследуются от него"""
    def __init__(self, detail: str = "An error occurred"):
        self.detail = detail
        super().__init__(detail)

# Типовые доменные ошибки
class ConflictError(AppException):
    """Исключение, при конфликте данных (уже существующим email, имя и тд)"""
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(detail)

class UnauthorizedError(AppException):
    """Исключение, при ошибке аутентификации (неверный пароль, отсутствие токена)"""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(detail)

class ForbiddenError(AppException):
    """Исключение, при недостатке прав доступа (пользователь аутентифицирован, но не авторизован)"""
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(detail)

class NotFoundError(AppException):
    """Исключение, при отсутствии запрашиваемого объекта (пользователь, чат, сообщение)"""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail)

class ExternalServiceError(AppException):
    """Исключение, при ошибке вызова внешнего сервиса, например OpenRouter API"""
    def __init__(self, detail: str = "External service error"):
        super().__init__(detail)