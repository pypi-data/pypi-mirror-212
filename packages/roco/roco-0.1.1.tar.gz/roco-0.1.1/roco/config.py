from pydantic import BaseSettings, root_validator


class Settings(BaseSettings):

    google_client_id: str | None = None
    google_authorize_url: str | None = None
    google_redirect_uri: str | None = None
    google_scope: str = 'openid email'

    github_client_id: str | None = None
    github_authorize_url: str | None = None
    github_redirect_uri: str | None = None
    github_scope: str = 'openid email'

    @root_validator
    def check_google_params(cls, values):
        three_values = [
            values.get('google_client_id'),
            values.get('google_authorize_url'),
            values.get('google_redirect_uri')
        ]
        count = len([v for v in three_values if v])

        if count not in (0, 3):
            raise ValueError(
                'google_client_id, google_authorize_url and google_redirect_uri'
                ' should be either all absent or all present'
            )

        return values

    @root_validator
    def check_github_params(cls, values):
        three_values = [
            values.get('github_client_id'),
            values.get('github_authorize_url'),
            values.get('github_redirect_uri')
        ]
        count = len([v for v in three_values if v])

        if count not in (0, 3):
            raise ValueError(
                'github_client_id, github_authorize_url and github_redirect_uri'
                ' should be either all absent or all present'
            )

        return values

    class Config:
        env_prefix = 'PAPERMERGE__AUTH__'


def get_settings():
    return Settings()
