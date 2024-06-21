#!/usr/bin/env python3

import json
import sys

def navigate_json(data, path=[]):
    while True:
        print("\nCurrent path:", " -> ".join(path))
        if isinstance(data, dict):
            print(" Keys:", ", ".join(data.keys()))
            action = input("Enter 'next' to navigate to a key, 'print' to print from here, or 'back' to go back: ")
            if action == "back":
                return
            elif action == "next":
                key = input("Enter the key: ")
                while key not in data:
                    print("No such key:", key)
                    key = input("Enter the key: ")
                navigate_json(data[key], path + [key])
            elif action == "print":
                print("Data:", json.dumps(data, indent=4))
            else:
                print("Invalid action:", action)
        elif isinstance(data, list):
            print(" Indices:", ", ".join(map(str, range(len(data)))))
            action = input("Enter 'next' to navigate to an index, 'print' to print from here, or 'back' to go back: ")
            if action == "back":
                return
            elif action == "next":
                while True:
                    index = input("Enter the index: ")
                    try:
                        index = int(index)
                        if 0 <= index < len(data):
                            navigate_json(data[index], path + [str(index)])
                            break
                        else:
                            print("Index out of range:", index)
                    except ValueError:
                        print("Invalid index:", index)
            elif action == "print":
                print("Data:", json.dumps(data, indent=4))
            else:
                print("Invalid action:", action)
        else:
            print("Value:", data)
            return

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            data = json.load(f)
    else:
        filename = input("Enter the JSON file path: ")
        with open(filename) as f:
            data = json.load(f)
    navigate_json(data)

if __name__ == "__main__":
    main()
