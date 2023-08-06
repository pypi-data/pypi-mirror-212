from datetime import datetime
from typing import Dict, List, Optional, Union

from runhouse.rh_config import rns_client
from runhouse.rns.packages import Package
from runhouse.rns.utils.env import _get_conda_yaml, _process_reqs
from .conda_env import CondaEnv

from .env import Env


# generic Env factory method
def env(
    reqs: List[Union[str, Package]] = [],
    conda_env: Union[str, Dict] = None,
    name: Optional[str] = None,
    setup_cmds: List[str] = None,
    dryrun: bool = True,
    load: bool = True,
):
    """FBuilds an instance of :class:`Env`.

    Args:
        reqs (List[str]): List of package names to install in this environment.
        conda_env (Union[str, Dict], optional): Dict representing conda env, Path to a conda env yaml file,
            or name of a local conda environment.
        name (Optional[str], optional): Name of the environment resource.
        setup_cmds (Optional[List[str]]): List of CLI commands to run for setup when the environment is
            being set up on a cluster.
        dryrun (bool, optional): Whether to run in dryrun mode. (Default: ``True``)
        load (bool, optional): Whether to load the environment. (Default: ``True``)

    Returns:
        Env: The resulting Env object.

    Example:
        >>> # regular python env
        >>> env = rh.env(reqs=["torch", "pip"])
        >>> env = rh.env(reqs=["reqs:./"], name="myenv")
        >>>
        >>> # conda env, see also rh.conda_env
        >>> conda_env_dict =
        >>>     {"name": "new-conda-env", "channels": ["defaults"], "dependencies": "pip", {"pip": "diffusers"})
        >>> conda_env = rh.env(conda_env=conda_env_dict)             # from a dict
        >>> conda_env = rh.env(conda_env="conda_env.yaml")           # from a yaml file
        >>> conda_env = rh.env(conda_env="local-conda-env-name")     # from a existing local conda env
        >>> conda_env = rh.env(conda_env="conda_env.yaml", reqs=["pip:/accelerate"])   # with additional reqs
    """

    config = rns_client.load_config(name) if load else {}
    config["name"] = name or config.get("rns_address", None) or config.get("name")

    reqs = reqs if reqs else config.get("reqs", [])
    config["reqs"] = _process_reqs(reqs)

    config["setup_cmds"] = (
        setup_cmds if setup_cmds is not None else config.get("setup_cmds")
    )
    conda_yaml = _get_conda_yaml(conda_env) or config.get("conda_yaml")

    if conda_yaml:
        config["conda_yaml"] = conda_yaml
        return CondaEnv.from_config(config, dryrun=dryrun)

    return Env.from_config(config, dryrun=dryrun)


# Conda Env factory method
def conda_env(
    reqs: List[Union[str, Package]] = [],
    conda_env: Union[str, Dict] = None,
    setup_cmds: List[str] = None,
    name: Optional[str] = None,
    dryrun: bool = True,
    load: bool = True,
):
    """Builds an instance of :class:`CondaEnv`.

    Args:
        reqs (List[str]): List of package names to install in this environment.
        conda_env (Union[str, Dict], optional): Dict representing conda env, Path to a conda env yaml file,
            or name of a local conda environment.
        name (Optional[str], optional): Name of the environment resource.
        setup_cmds (Optional[List[str]]): List of CLI commands to run for setup when the environment is
            being set up on a cluster.
        dryrun (bool, optional): Whether to run in dryrun mode. (Default: ``True``)
        load (bool, optional): Whether to load the environment. (Default: ``True``)

    Returns:
        CondaEnv: The resulting CondaEnv object.

    Example:
        >>> rh.conda_env(reqs=["torch"])
        >>> rh.conda_env(reqs=["torch"], name="resource_name")
        >>> rh.conda_env(reqs=["torch"], name="resource_name", conda_env={"name": "conda_env"})
    """
    if not conda_env:
        if name:
            conda_env = {"name": name}
        else:
            conda_env = {"name": datetime.now().strftime("%Y%m%d_%H%M%S")}

    return env(reqs, conda_env, name, setup_cmds, dryrun, load)
