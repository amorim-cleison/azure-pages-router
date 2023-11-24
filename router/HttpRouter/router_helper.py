from urllib.parse import urlparse
import json
import re

ROOT = "~cca5"
MAPPING_FILE = "./HttpRouter/url_mapping.json"
FALLBACK_ROUTE = "<fallback>"


def find_route(originUrl):
    parsedUrl = urlparse(originUrl)
    path = parsedUrl.path

    # Normalize path and target mapping:
    path = normalizePath(path, removeRoot=True)

    # Locate target for path:
    urlMapping = loadUrlMapping(MAPPING_FILE)
    urlMapping = normalizeMapping(urlMapping)
    target = findTargetByPath(path, urlMapping)

    return target


def loadUrlMapping(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise Exception("Failed to read URL mapping file", e)


def normalizeMapping(mapping):
    return {
        normalizePath(path, removeRoot=False): target.lower()
        for (path, target) in mapping.items()
    }


def findTargetByPath(path, urlMapping):
    _path = path
    target = None

    # Navigate routes to final URL:
    while _path in urlMapping:
        target = urlMapping[_path]
        _path = target

    # Fallback case, if configured:
    if (not target) and (FALLBACK_ROUTE in urlMapping):
        target = urlMapping[FALLBACK_ROUTE]
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
