from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    email: EmailStr # Валидирует, что значение является корректным email
    password: str = Field(min_length=8, max_length = 30)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Если логин принимается не через OAuth2PasswordRequestForm, то
class LoginRequest(BaseModel):
    username: str
    password: str

# Публичные данные о пользователе, которые выводятся при запросе
class UserPublic(BaseModel):
    id: int
    email: EmailStr
    role: str
