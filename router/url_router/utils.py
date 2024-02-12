from glob import glob
from .constants import *
from .errors import *
from .error_messages import *
import json
import os
import re
from urllib.parse import urlparse


def find_target_url(path, url_mapping):
    # Normalize path and target mapping:
    path = __normalize_path(path, removeRoot=True)

    # Locate target for path:
    url_mapping = __normalize_mapping(url_mapping)
    return __find_target_by_path(path, url_mapping)


def __normalize_mapping(mapping):
    return {
        __normalize_path(path, removeRoot=False): target.lower()
        for (path, target) in mapping.items() if path
    }


def __find_target_by_path(path, url_mapping):
    _path = path
    target = None

    # Navigate routes to final URL:
    while _path in url_mapping:
        target = url_mapping[_path]
        _path = target

    # Fallback case, if configured:
    if not target:
        raise RouteNotFoundError(TARGET_URL_NOT_FOUND.format(path=path))
    return target


def __normalize_path(path, removeRoot=True, root=URL_ROOT):
    PART_SEP = '/'

    # Normalize path:
    normalized = path.lower()
    normalized = re.sub(r"\s+", "", path).split(PART_SEP)

    # Remove empty parts:
    normalized = filter(lambda x: (x != '' and x is not None), normalized)

    # Remove prefix:
    normalized = filter(lambda x: x != root,
                        normalized) if removeRoot else normalized

    # Re-compose URL:
    return PART_SEP.join(normalized)


def parse_path_to_url(path):
    try:
        return urlparse(path)
    except Exception as e:
        raise InvalidPathError(
            ORIGIN_URL_PATH_FAILED_TO_PARSE.format(path=path)) from e


def resolve_path_to_file(filename):
    path = None
    paths = glob(f'./**/{filename}', recursive=True)

    if paths and len(paths) > 0:
        return os.path.realpath(paths[0])
    raise InternalServerError(
        PATH_TO_FILE_FAILED_TO_RESOLVE.format(file=filename))


def get_request_param(name, request):
    # Try read as GET:
    originUrl = request.params.get(name)

    # Try read as POST:
    if originUrl is None:
        try:
            req_body = request.get_json()
        except ValueError as e:
            pass
        else:
            originUrl = req_body.get(name)

    # If parameter found:
    if originUrl is not None:
        return originUrl

    raise MissingArgumentError(REQUEST_PARAMETER_MISSING.format(name=name))


def load_html_content(path, parameters):
    try:
        path = resolve_path_to_file(path)

        # Read file content:
        with open(path, mode='r', encoding='utf-8') as file:
            content = file.read()

        # Replace parameters:
        if content:
            for name, value in parameters.items():
                content = content.replace(f"[{name}]", str(value))
        return content

    except Exception as ex:
        raise InternalServerError(
            HTML_FILE_FAILED_TO_LOAD.format(path=path)) from ex


def map_to_str(m):
    return [f"{k}: {v}" for k, v in m.items()]
