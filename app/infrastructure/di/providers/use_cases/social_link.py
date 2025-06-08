from dishka import Provider, Scope, provide

from app.application.use_cases.social_link.add_social_link import AddSocialLinkUseCase
from app.application.use_cases.social_link.get_profile_social_links import (
    GetProfileSocialLinksUseCase,
)
from app.application.use_cases.social_link.remove_social_link import (
    RemoveSocialLinkUseCase,
)
from app.domain.ports.repositories.social_link import ISocialLinkRepository


class SocialLinkUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_add_social_link_uc(self, repo: ISocialLinkRepository) -> AddSocialLinkUseCase:
        return AddSocialLinkUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_remove_social_link_uc(self, repo: ISocialLinkRepository) -> RemoveSocialLinkUseCase:
        return RemoveSocialLinkUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_social_links_uc(self, repo: ISocialLinkRepository) -> GetProfileSocialLinksUseCase:
        return GetProfileSocialLinksUseCase(repo)
