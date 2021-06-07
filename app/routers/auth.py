from app.db.postgre_connector import PostgreSqlConnector
from app.managers.user import UserManager
from fastapi import APIRouter, Depends, HTTPException
from app.security.functions import JWTFunctions
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.serializers.token import Token as TokenSerializer

router = APIRouter()


@router.post('/login', response_model=TokenSerializer)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    user = await UserManager.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    access_token = JWTFunctions.create_access_token({
        'sub': user.username,
        'user_uuid': str(user.uuid)
    })
    return {'access_token': access_token, 'token_type': 'bearer'}
