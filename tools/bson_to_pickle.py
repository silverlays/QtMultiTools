### As of version 0.7-Alpha of QtMultiTools or TVShow Tracker
### the format of the file used as a database changes from BSON to the native Pickle package.
### This tool allows you to make the conversion smoothly.

### /!\ This tool require BSON! /!\
### To install: pip install bson
### To uninstall: pip uninstall bson six python_dateutil
import os
import bson
import pickle


DEFAULT_DB_FILENAME = "tmdb.dat"
NEW_DB_FILENAME = "tmdb_new.dat"


def convert():
  bson_data = {}
  try:
    with open(DEFAULT_DB_FILENAME, "rb") as fp:
      bson_data = bson.loads(fp.read(-1))
    
    with open(NEW_DB_FILENAME, "wb") as fp:
      pickle.dump(bson_data, fp)
  except Exception as e:
    print(f"\n[ERROR]: {e.args[0]}.")
    print(f"Please check that your <{DEFAULT_DB_FILENAME}> is a valid bson file before proceed. Exiting...")
    exit()


if __name__ == "__main__":
  if os.path.exists(DEFAULT_DB_FILENAME):
    convert()
    print(f"\nDon't forget to rename <{NEW_DB_FILENAME}> in <{DEFAULT_DB_FILENAME}> so that it is recognized by QtMultiTools and/or TVShow Tracker.\n")
    exit(0)
  else:
    print(f"\n[ERROR]: <{DEFAULT_DB_FILENAME}> cannot be found in this directory.")
    print(f"Please copy your <{DEFAULT_DB_FILENAME}> from your QtMultiTools or TVShow Tracker directory to the folder where is this script before proceed. Exiting...")
    exit()