#!/usr/bin/env python3
"""
HeadCount Terminal - No GUI version
Opens images in default viewer, type to categorize
"""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path

DEFAULT_INPUT = "dc_photos"
DEFAULT_OUTPUT = "dc_photos_sorted"
DEFAULT_CATEGORIES = {
    'b': 'black',
    'w': 'white',
    'h': 'hispanic',
    'a': 'asian',
    'o': 'other',
    's': 'skip',
}


def main():
    """Run the HeadCount Terminal for sorting images into categories.
    
    This function sets up the command-line interface for the HeadCount Terminal,
    parsing input and output folder paths. It checks for the existence of the input
    directory, creates necessary output folders, and gathers all image files.  The
    function then identifies already sorted images and prompts the user to
    categorize the remaining images, handling user input and file operations
    throughout the process.
    """
    parser = argparse.ArgumentParser(description="HeadCount Terminal - No GUI image sorting")
    parser.add_argument('--input', '-i', default=DEFAULT_INPUT, help="Input folder")
    parser.add_argument('--output', '-o', default=DEFAULT_OUTPUT, help="Output folder")
    args = parser.parse_args()
    
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    
    if not input_dir.exists():
        print(f"Input folder not found: {input_dir}")
        sys.exit(1)
    
    # Create output folders
    for cat in DEFAULT_CATEGORIES.values():
        (output_dir / cat).mkdir(parents=True, exist_ok=True)
    
    # Get photos
    all_photos = sorted(
        list(input_dir.glob("*.jpg")) + 
        list(input_dir.glob("*.jpeg")) + 
        list(input_dir.glob("*.png"))
    )
    
    # Check what's already sorted
    sorted_photos = set()
    for cat_dir in output_dir.iterdir():
        if cat_dir.is_dir():
            for f in cat_dir.iterdir():
                sorted_photos.add(f.name)
    
    photos = [p for p in all_photos if p.name not in sorted_photos]
    
    print(f"Total photos: {len(all_photos)}")
    print(f"Already sorted: {len(sorted_photos)}")
    print(f"Remaining: {len(photos)}")
    
    if not photos:
        print("\nAll photos sorted!")
        print_results(output_dir)
        sys.exit(0)
    
    # Build help text
    keys_help = "  ".join([f"{k.upper()}={v}" for k, v in DEFAULT_CATEGORIES.items()])
    print(f"\nKeys: {keys_help}  Q=quit\n")
    
    for i, photo in enumerate(photos):
        # Open photo in default viewer
        try:
            subprocess.Popen(
                ['xdg-open', str(photo)], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
        except:
            print(f"  Could not open {photo}")
        
        while True:
            choice = input(f"[{i+1}/{len(photos)}] {photo.name}: ").strip().lower()
            
            if choice == 'q':
                print("\nQuitting...")
                print_results(output_dir)
                sys.exit(0)
            
            if choice in DEFAULT_CATEGORIES:
                dest = output_dir / DEFAULT_CATEGORIES[choice] / photo.name
                shutil.copy(photo, dest)
                print(f"  → {DEFAULT_CATEGORIES[choice]}")
                break
            else:
                print(f"  Invalid. Use: {'/'.join(DEFAULT_CATEGORIES.keys())} or q")
    
    print("\nDone!")
    print_results(output_dir)


def print_results(output_dir):
    """Print category counts and total from the specified output directory."""
    print("\n" + "="*40)
    print("RESULTS")
    print("="*40)
    total = 0
    for cat in DEFAULT_CATEGORIES.values():
        cat_dir = output_dir / cat
        count = len(list(cat_dir.glob("*"))) if cat_dir.exists() else 0
        total += count
        print(f"  {cat}: {count}")
    print("-"*40)
    print(f"  total: {total}")


if __name__ == "__main__":
    main()
