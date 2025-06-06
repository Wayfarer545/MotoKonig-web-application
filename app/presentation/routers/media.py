# app/presentation/routers/media.py

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile, status

from app.application.controllers.media_controller import MediaController
from app.application.exceptions import BadRequestError, NotFoundError
from app.domain.ports.token_service import TokenServicePort
from app.domain.value_objects.file_type import FileType
from app.presentation.middleware.auth import get_current_user_dishka
from app.presentation.schemas.media import (
    DeleteFileRequest,
    FileUploadResponse,
    GetPresignedUrlRequest,
    GetUploadUrlRequest,
    MessageResponse,
    PresignedUrlResponse,
    UploadUrlResponse,
)

router = APIRouter(route_class=DishkaRoute)


@router.post("/upload", response_model=FileUploadResponse, status_code=201)
async def upload_file(
        request: Request,
        file: UploadFile = File(...),
        file_type: FileType = Form(...),
        controller: FromDishka[MediaController] = None,
        token_service: FromDishka[TokenServicePort] = None
):
    """Загрузить файл через multipart/form-data"""
    current_user = await get_current_user_dishka(request, token_service)

    # Валидация файла
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required"
        )

    if not file.content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content type is required"
        )

    # Проверяем допустимый тип контента
    allowed_types = file_type.get_allowed_content_types()
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Content type {file.content_type} not allowed for {file_type.value}. "
                   f"Allowed types: {', '.join(allowed_types)}"
        )

    try:
        # Читаем содержимое файла
        file_content = await file.read()

        # Проверяем размер
        max_size_bytes = file_type.get_max_size_mb() * 1024 * 1024
        if len(file_content) > max_size_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size {len(file_content)} bytes exceeds maximum "
                       f"{file_type.get_max_size_mb()}MB for {file_type.value}"
            )

        # Загружаем файл
        result = await controller.upload_file(
            file_content=file_content,
            file_name=file.filename,
            file_type=file_type,
            content_type=file.content_type,
            owner_id=current_user["user_id"]
        )

        return result

    except BadRequestError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        ) from ex
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(ex)}"
        ) from ex


@router.post("/upload-url", response_model=UploadUrlResponse)
async def get_upload_url(
        request: Request,
        upload_request: GetUploadUrlRequest,
        controller: FromDishka[MediaController] = None,
        token_service: FromDishka[TokenServicePort] = None
):
    """Получить presigned URL для загрузки файла"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        result = await controller.get_upload_url(
            file_type=upload_request.file_type,
            file_name=upload_request.file_name,
            content_type=upload_request.content_type,
            owner_id=current_user["user_id"],
            expiry_seconds=upload_request.expiry_seconds
        )
        return result

    except BadRequestError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        ) from ex


@router.post("/download-url", response_model=PresignedUrlResponse)
async def get_download_url(
        request: Request,
        download_request: GetPresignedUrlRequest,
        controller: FromDishka[MediaController] = None,
        token_service: FromDishka[TokenServicePort] = None
):
    """Получить presigned URL для скачивания файла"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        result = await controller.get_download_url(
            file_key=download_request.file_key,
            bucket=download_request.bucket,
            expiry_seconds=download_request.expiry_seconds,
            owner_id=current_user["user_id"]  # Проверяем доступ
        )
        return result

    except BadRequestError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        ) from ex
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex


@router.delete("/", response_model=MessageResponse)
async def delete_file(
        request: Request,
        delete_request: DeleteFileRequest,
        controller: FromDishka[MediaController] = None,
        token_service: FromDishka[TokenServicePort] = None
):
    """Удалить файл из хранилища"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        await controller.delete_file(
            file_key=delete_request.file_key,
            bucket=delete_request.bucket,
            owner_id=current_user["user_id"]  # Только владелец может удалить
        )

        return {"message": "File deleted successfully"}

    except BadRequestError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        ) from ex
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex
