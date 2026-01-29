#!/usr/bin/env python3
"""
HeadCount - Fast image classification for demographic analysis
https://github.com/[username]/headcount

When they won't publish the data, count it yourself.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

try:
    from PIL import Image, ImageTk
    import tkinter as tk
    from tkinter import Label, Frame
except ImportError:
    print("Missing dependencies. Install with:")
    print("  sudo apt install python3-tk python3-pil.imagetk")
    print("  pip install pillow --break-system-packages")
    sys.exit(1)

# Default configuration
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


class HeadCount:
    def __init__(self, input_dir, output_dir, categories):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.categories = categories
        self.current_idx = 0
        self.img_tk = None
        
        # Create output folders
        for cat in self.categories.values():
            (self.output_dir / cat).mkdir(parents=True, exist_ok=True)
        
        # Get unsorted photos
        self.all_photos = sorted(
            list(self.input_dir.glob("*.jpg")) + 
            list(self.input_dir.glob("*.jpeg")) + 
            list(self.input_dir.glob("*.png"))
        )
        
        # Check what's already sorted
        sorted_photos = set()
        for cat_dir in self.output_dir.iterdir():
            if cat_dir.is_dir():
                for f in cat_dir.iterdir():
                    sorted_photos.add(f.name)
        
        self.photos_to_sort = [p for p in self.all_photos if p.name not in sorted_photos]
        
        print(f"Total photos: {len(self.all_photos)}")
        print(f"Already sorted: {len(sorted_photos)}")
        print(f"Remaining: {len(self.photos_to_sort)}")
        
        if not self.photos_to_sort:
            print("\nAll photos sorted!")
            self.print_results()
            sys.exit(0)
    
    def print_results(self):
        """Print category counts and total results."""
        print("\n" + "="*40)
        print("RESULTS")
        print("="*40)
        total = 0
        for cat in self.categories.values():
            cat_dir = self.output_dir / cat
            count = len(list(cat_dir.glob("*"))) if cat_dir.exists() else 0
            total += count
            pct = (count / total * 100) if total > 0 else 0
            print(f"  {cat}: {count}")
        print("-"*40)
        print(f"  total: {total}")
    
    def run(self):
        """Start the GUI for the HeadCount application."""
        self.root = tk.Tk()
        self.root.title("HeadCount")
        self.root.geometry("650x750")
        self.root.configure(bg='#1a1a1a')
        
        # Photo display
        self.photo_label = Label(self.root, bg='#1a1a1a')
        self.photo_label.pack(pady=20)
        
        # Status
        self.status_label = Label(
            self.root, 
            text="", 
            font=("Courier", 11),
            fg='#ffffff',
            bg='#1a1a1a',
            justify='center'
        )
        self.status_label.pack(pady=10)
        
        # Key bindings
        self.root.bind('<Key>', self.on_key)
        
        # Show first photo
        self.show_photo()
        
        self.root.mainloop()
    
    def show_photo(self):
        """Display the current photo and update the status label."""
        if self.current_idx >= len(self.photos_to_sort):
            self.status_label.config(text="\n✓ DONE!\n\nAll photos sorted.")
            self.print_results()
            return
        
        photo_path = self.photos_to_sort[self.current_idx]
        
        # Load and resize
        try:
            img = Image.open(photo_path)
            img.thumbnail((500, 500))
            self.img_tk = ImageTk.PhotoImage(img)
            self.photo_label.config(image=self.img_tk)
        except Exception as e:
            print(f"Error loading {photo_path}: {e}")
            self.current_idx += 1
            self.show_photo()
            return
        
        # Build key help text
        keys_help = "  ".join([f"{k.upper()}={v}" for k, v in self.categories.items()])
        
        self.status_label.config(
            text=f"[{self.current_idx + 1}/{len(self.photos_to_sort)}]  {photo_path.name}\n\n"
                 f"{keys_help}\n"
                 f"Q=quit"
        )
    
    def on_key(self, event):
        """Handle keypress events for photo sorting.
        
        This method processes keypress events to manage photo sorting.  If the 'q' key
        is pressed, it prints the results and quits the application.  For other keys
        that correspond to categories, it copies the current photo  to the designated
        output directory and updates the index to show the next photo.
        """
        key = event.char.lower()
        
        if key == 'q':
            self.print_results()
            self.root.quit()
            return
        
        if key in self.categories and self.current_idx < len(self.photos_to_sort):
            photo_path = self.photos_to_sort[self.current_idx]
            dest = self.output_dir / self.categories[key] / photo_path.name
            
            try:
                shutil.copy(photo_path, dest)
                print(f"  {photo_path.name} → {self.categories[key]}")
            except Exception as e:
                print(f"  Error: {e}")
            
            self.current_idx += 1
            self.show_photo()


def main():
    """Run the HeadCount image classification application.
    
    This function sets up the command-line interface for the HeadCount application,
    allowing users to specify input and output directories for image
    classification.  It handles the counting of already-sorted images if the
    `--count` flag is provided,  and initializes the HeadCount application to
    process images if the input directory exists.  The function also includes error
    handling for missing directories.
    """
    parser = argparse.ArgumentParser(
        description="HeadCount - Fast image classification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example: python3 headcount.py --input photos --output sorted"
    )
    parser.add_argument('--input', '-i', default=DEFAULT_INPUT,
                        help=f"Input folder with images (default: {DEFAULT_INPUT})")
    parser.add_argument('--output', '-o', default=DEFAULT_OUTPUT,
                        help=f"Output folder for sorted images (default: {DEFAULT_OUTPUT})")
    parser.add_argument('--count', '-c', action='store_true',
                        help="Just count already-sorted results")
    
    args = parser.parse_args()
    
    if args.count:
        output_dir = Path(args.output)
        if not output_dir.exists():
            print(f"Output folder not found: {output_dir}")
            sys.exit(1)
        
        print("\n" + "="*40)
        print("RESULTS")
        print("="*40)
        total = 0
        for cat_dir in sorted(output_dir.iterdir()):
            if cat_dir.is_dir():
                count = len(list(cat_dir.glob("*")))
                total += count
                print(f"  {cat_dir.name}: {count}")
        print("-"*40)
        print(f"  total: {total}")
        sys.exit(0)
    
    if not Path(args.input).exists():
        print(f"Input folder not found: {args.input}")
        print(f"Run a scraper first, or specify --input")
        sys.exit(1)
    
    app = HeadCount(args.input, args.output, DEFAULT_CATEGORIES)
    app.run()


if __name__ == "__main__":
    main()
