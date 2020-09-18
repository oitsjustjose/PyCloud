"""
Author: Jose Stovall | oitsjustjose@git
"""

import json
import os
import time
from distutils.dir_util import copy_tree, remove_tree
from distutils.errors import DistutilsFileError
from typing import Dict, List, Union

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


class ChangeHandler(FileSystemEventHandler):
    """
    Listens / handles changes from WatchDog
    Arguments:
        target (str): the target directory to copy to
        ignore (List[str]): a list of files to ignore changes of
    """

    def __init__(self, target: str, ignore: List[str]):
        self._cp_target = target
        self._ignore = ignore

        if not os.path.exists(os.path.basename(self._cp_target)):
            os.mkdir(self._cp_target)

    def on_modified(self, event: FileSystemEvent):
        if os.path.basename(event.src_path) in self._ignore:
            return
        try:
            folder_name = f"{self._cp_target}/{os.path.basename(event.src_path)}"

            if os.path.exists(folder_name) and os.path.isdir(folder_name):
                remove_tree(folder_name)

            os.mkdir(folder_name)

            copy_tree(event.src_path, folder_name)
        except DistutilsFileError as exc:
            print(f"Failed to clone: {exc}")


def main(config: Dict[str, Union[List[str], float, List[Dict[str, str]]]]) -> None:
    """
    The main listen loop
    """
    observers: List[Observer] = list()

    for watch_conf in config["dirs"]:
        handler = ChangeHandler(watch_conf["target"], config["ignore"])

        observer = Observer()
        observers.append(observer)
        observer.schedule(
            path=watch_conf["watch"], event_handler=handler, recursive=True
        )
        observer.start()

        print(
            f"Copying any file changes in {watch_conf['watch']} to {watch_conf['target']}"
        )

    while True:
        try:
            time.sleep(config["updateFreq"])
        except KeyboardInterrupt:
            print("Quitting..")
            map(lambda x: x.stop(), observers)
            map(lambda x: x.join(), observers)
            break


if __name__ == "__main__":
    if os.path.exists("./config.json"):
        with open("./config.json", "r") as file:
            CONFIG = json.loads(file.read())
        main(CONFIG)
    else:
        print("No config found at project root. Quitting...")
