# app/infrastructure/di/providers/presentation/media.py

from dishka import Provider, Scope, provide

from app.application.controllers.media_controller import MediaController
from app.application.use_cases.media.delete_file import DeleteFileUseCase
from app.application.use_cases.media.get_presigned_url import GetPresignedUrlUseCase
from app.application.use_cases.media.upload_file import UploadFileUseCase


class MediaControllerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_media_controller(
        self,
        upload_uc: UploadFileUseCase,
        delete_uc: DeleteFileUseCase,
        presigned_url_uc: GetPresignedUrlUseCase,
    ) -> MediaController:
        return MediaController(upload_uc, delete_uc, presigned_url_uc)
