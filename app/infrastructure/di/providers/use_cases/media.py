from dishka import Provider, Scope, provide

from app.application.use_cases.media.delete_file import DeleteFileUseCase
from app.application.use_cases.media.get_presigned_url import GetPresignedUrlUseCase
from app.application.use_cases.media.upload_file import UploadFileUseCase
from app.domain.ports.repositories.file_storage import FileStoragePort
from app.domain.ports.repositories.media_file import IMediaFileRepository


class MediaUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_upload_file_uc(
        self,
        file_storage: FileStoragePort,
        media_repo: IMediaFileRepository,
    ) -> UploadFileUseCase:
        return UploadFileUseCase(file_storage, media_repo)

    @provide(scope=Scope.REQUEST)
    def provide_delete_file_uc(
        self,
        file_storage: FileStoragePort,
        media_repo: IMediaFileRepository,
    ) -> DeleteFileUseCase:
        return DeleteFileUseCase(file_storage, media_repo)

    @provide(scope=Scope.REQUEST)
    def provide_presigned_url_uc(
        self,
        file_storage: FileStoragePort,
        media_repo: IMediaFileRepository,
    ) -> GetPresignedUrlUseCase:
        return GetPresignedUrlUseCase(file_storage, media_repo)
