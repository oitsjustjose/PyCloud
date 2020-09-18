# PyCloud - A Python-based, Dynamic Backup App Based on File Changes

## About

PyCloud is a python-based backup app that listens for changes to files in the folders you specify in the config (see #Config ). With PyCloud, you can copy your local files to the cloud (such as DropBox or Google Drive) or a local NAS based on your personal preference. This highly-configurable app allows you to create a backup experience tailored to your use-case, ranging from syncing files between two computers via NAS, backing up local document edits to Google Drive or more!

## Installation

PyCloud uses Python (as the name hints), so you'll need to have Python installed in advance ([get it here!](https://www.python.org/downloads/)) - you'll want version 3.8.5 as of writing this.

Once installed, you'll want to open up the `.sh` or `.bat` file to install the Python dependencies (there's only one).

### Windows
To install the Python dependencies, just double-click on `install.bat`. You should get a success message when it's completed!

### macOS + Linux 🐧
To install the Python dependencies, you'll need to crack open the terminal (`/Applications/Utilities/Terminal.app` for macOS; it varies for Linux). Once there, you'll need to type in the following:

```
$ > cd <directory of unzipped project>
$ > chmod +x ./install.sh
$ > ./install.sh
```

Once completed you should get a success message!

## Usage

Once you have Python and its dependencies set up, it's time to run! To do so, just run the following command in your terminal / Python (don't forget to `cd` into the project folder first if necessary)

```python main.py```

You should see messages informing you of the watched folders. You'll want to leave this window open, or [run it in the background](https://www.tecmint.com/run-linux-command-process-in-background-detach-process/) if you know how 😊

## Config

PyCloud's config is pretty powerful, allowing you to customize most of its behavior. Let's walk through it -- anything after // is a comment that indicates what to do.

```jsonc
{
// These are files that will be ignored, no matter where you are.
  "ignore": [".DS_Store"],
// How many seconds apart to wait for updates. 0.5 works just fine
  "updateFreq": 0.5, 
// A list (add as many as you want!) of dirs to clone
  "dirs": [{
	// The directory to listen for (in this case, my downloads)
    "watch": "/Users/jose/Downloads",
    // The directory to copy to. It'll make a Downloads folder in DownloadsClone
    "target": "/Users/jose/Documents/DownloadClone" 
  }]
}
```