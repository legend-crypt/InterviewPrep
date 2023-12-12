from core.urls.url_components import (
    accounts,
    authentication
)

URL_COMPONENTS = (
    accounts.ACCOUNTS_URLS
    + authentication.AUTHENTICATION_URLS
)

# app_name = "core"

urlpatterns = URL_COMPONENTS
