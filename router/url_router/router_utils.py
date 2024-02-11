from glob import glob
from os import path
import json
import re

ROOT = "~cca5"
MAPPING_FILE = "url_mapping.json"
FALLBACK_ROUTE = "<fallback>"


def find_route(originUrl):
    path = originUrl.path

    # Normalize path and target mapping:
    path = normalizePath(path, removeRoot=True)

    # Locate target for path:
    mapping_path = resolvePathToMappingFile(MAPPING_FILE)
    url_mapping = loadUrlMapping(mapping_path)
    target = findTargetByPath(path, url_mapping)

    return target


def loadUrlMapping(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            json_mapping = json.load(f)
            return normalizeMapping(json_mapping)
    except Exception as e:
        raise Exception("Failed to read URL mapping file", e)


def resolvePathToMappingFile(filename):
    paths = glob(f'./**/{filename}', recursive=True)

    if not paths:
        raise Exception(f"Could not find mapping file '{filename}'")
    return path.realpath(paths[0])


def normalizeMapping(mapping):
    return {
        normalizePath(path, removeRoot=False): target.lower()
        for (path, target) in mapping.items() if path
    }


def findTargetByPath(path, url_mapping):
    _path = path
    target = None

    # Navigate routes to final URL:
    while _path in url_mapping:
        target = url_mapping[_path]
        _path = target

    # Fallback case, if configured:
    if (not target) and (FALLBACK_ROUTE in url_mapping):
        target = url_mapping[FALLBACK_ROUTE]
    return target


def normalizePath(path, removeRoot=True, root=ROOT):
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
