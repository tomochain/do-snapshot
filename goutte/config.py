import sys

import colorlog
import yaml
import yamale


SCHEMA = """name: regex('^[a-zA-Z]{3,}$', name='valid name')
keep: int()
targets: include('type')
---
type:
    droplets: include('droplet', required=False)
    volumes: include('volume', required=False)
---
droplet:
    names: list(regex('^[^-][A-Za-z0-9.-]*[^-]$', name='valid droplet name'), required=False)
    tags: list(regex('^[A-Za-z0-9:-_]+$', name='valid droplet tag'), required=False)
---
volume:
    names: list(regex('^[^-][A-Za-z0-9-]*[^-]$', name='valid volume name'), required=False)
"""  # noqa

log = colorlog.getLogger(__name__)


def get(path: str) -> dict:
    """Get the configuration.
    Parse and validate it with the config schema.
    Exits if could not get a valid config.

    Args:
        path (str): path to the configuration file

    Returns:
        dict: valide configuration
    """
    config = {}
    try:
        with open(path) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError:
        log.fatal("no configuration file found")
        sys.exit(1)
    except PermissionError:
        log.fatal("access designed")
        sys.exit(1)
    except yaml.YAMLError:
        log.fatal("malformated yml configuration")
        sys.exit(1)
    except (IOError, IsADirectoryError):
        log.fatal("error while reading dx configuration")
        sys.exit(1)
    try:
        yamale.validate(
            yamale.make_schema(content=SCHEMA),
            yamale.make_data(content=yaml.dump(config)),
        )
    except yamale.yamale_error.YamaleError as e:
        log.fatal(e)
        sys.exit(1)
    return config
