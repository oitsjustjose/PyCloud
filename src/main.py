"""
Author: Jose Stovall | oitsjustjose@git
"""

import json
import os
import time
from distutils.dir_util import copy_tree, remove_tree
from shutil import copyfile
from typing import Dict, List, Union

from watchdog.events import (
    EVENT_TYPE_CREATED,
    EVENT_TYPE_DELETED,
    EVENT_TYPE_MODIFIED,
    FileSystemEvent,
    FileSystemEventHandler,
)
from watchdog.observers import Observer


class ChangeHandler(FileSystemEventHandler):
    """
    Listens / handles changes from WatchDog
    Arguments:
        target (str): the target directory to copy to
        ignore (List[str]): a list of files to ignore changes of
    """

    def __init__(self, watch: str, target: str, ignore: List[str]):
        self._watch = watch
        self._cp_target = target
        self._ignore = ignore

        print(f"Making initial clone of {self._watch} to dir {self._cp_target}")
        copy_tree(self._watch, self._cp_target)

    def on_any_event(self, event: FileSystemEvent):
        if event.event_type == EVENT_TYPE_DELETED:
            self.on_deleted(event)
        elif event.event_type == EVENT_TYPE_CREATED:
            self.on_created(event)
        elif event.event_type == EVENT_TYPE_MODIFIED:
            self.on_created(event)

    def on_deleted(self, event: FileSystemEvent):
        # Ignore files that we say to ignore
        if os.path.basename(event.src_path) in self._ignore:
            return

        path = f"{self._cp_target}{event.src_path.replace(self._watch, '')}"
        
        if not os.path.exists(path):
            return

        try:
            if event.is_directory:
                remove_tree(path)
            else:
                os.unlink(path)
        except PermissionError:
            pass

    def on_created(self, event: FileSystemEvent):
        # Ignore files that we say to ignore
        if os.path.basename(event.src_path) in self._ignore:
            return

        path = f"{self._cp_target}{event.src_path.replace(self._watch, '')}"
        
        if not os.path.exists(event.src_path):
            return

        try:
            if event.is_directory:
                copy_tree(event.src_path, path)
            else:
                copyfile(event.src_path, path)
        except PermissionError:
            pass

    def on_modified(self, event: FileSystemEvent):
        # Ignore files that we say to ignore
        if os.path.basename(event.src_path) in self._ignore:
            return

        path = f"{self._cp_target}{event.src_path.replace(self._watch, '')}"
        
        if not os.path.exists(event.src_path):
            return

        try:
            if event.is_directory:
                if os.path.exists(path):
                    remove_tree(path)
                copy_tree(event.src_path, path)
            else:
                if os.path.exists(path):
                    os.unlink(path)
                copyfile(event.src_path, path)
        except PermissionError:
            pass

    def on_moved(self, event: FileSystemEvent):
        # Ignore files that we say to ignore
        if os.path.basename(event.src_path) in self._ignore:
            return
        if self._watch in event.src_path:
            self.on_modified(event)


def main(config: Dict[str, Union[List[str], float, List[Dict[str, str]]]]) -> None:
    """
    The main listen loop
    """
    observers: List[Observer] = list()

    for watch_conf in config["dirs"]:
        handler = ChangeHandler(
            watch_conf["watch"], watch_conf["target"], config["ignore"]
        )

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
