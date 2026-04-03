from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import RegisterRequest, UserPublic, TokenResponse
from app.usecases.auth import AuthUseCase
from app.api.deps import get_auth_usecase, get_current_user_id
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError

router = APIRouter()

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    auth_uc: AuthUseCase = Depends(get_auth_usecase),
):
    try:
        user = await auth_uc.register(email=request.email, password=request.password)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)
    # user уже содержит id, email, role (публичные данные)
    return UserPublic(id=user["id"], email=user["email"], role=user["role"])

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_uc: AuthUseCase = Depends(get_auth_usecase),
):
    try:
        tokens = await auth_uc.login(email=form_data.username, password=form_data.password)
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenResponse(access_token=tokens["access_token"], token_type=tokens["token_type"])

@router.get("/me", response_model=UserPublic)
async def get_me(
    user_id: int = Depends(get_current_user_id),
    auth_uc: AuthUseCase = Depends(get_auth_usecase),
):
    try:
        user = await auth_uc.get_profile(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    return UserPublic(id=user["id"], email=user["email"], role=user["role"])