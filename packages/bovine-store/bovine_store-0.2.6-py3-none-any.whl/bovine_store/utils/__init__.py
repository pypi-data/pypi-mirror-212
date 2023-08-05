from urllib.parse import urljoin, urlparse

from bovine_store.types import EndpointType


def determine_summary(obj):
    for key in ["summary", "name", "content"]:
        if obj.get(key):
            return obj[key][:97]
    return


def get_actor_endpoint(endpoints):
    for endpoint in endpoints:
        if endpoint.endpoint_type == EndpointType.ACTOR:
            return endpoint


def get_account(keypairs):
    for kp in keypairs:
        if kp.public_key.startswith("acct:"):
            return kp


def user_to_account_and_actor_url(user):
    if not user:
        return None, None

    endpoint = get_actor_endpoint(user.endpoints)
    keypair = get_account(user.keypairs)

    return (keypair.public_key, endpoint.name)


def path_from_request(request) -> str:
    url = request.url
    if request.headers.get("X-Forwarded-Proto") == "https":
        url = url.replace("http://", "https://")

    return urljoin(url, urlparse(url).path)
