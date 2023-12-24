import tkinter as tk
from tkinter import filedialog
import json

class InstagramReelsSaverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Reels Saver")

        self.urls = []
        self.file_path = "./reels.json"  # Replace with the actual path

        # Create and pack widgets
        self.label = tk.Label(root, text="Enter Instagram Reel URLs:")
        self.label.pack()

        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()

        self.add_button = tk.Button(root, text="Add URL", command=self.add_url_and_save)
        self.add_button.pack()

        self.remove_button = tk.Button(root, text="Remove URL", command=self.remove_url)
        self.remove_button.pack()

        self.clear_button = tk.Button(root, text="Clear File", command=self.clear_file)
        self.clear_button.pack()

        self.urls_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=50)
        self.urls_listbox.pack()
        
        # Initialize the URLs listbox by calling read_file
        self.read_file()

    def add_url_and_save(self):
        url = self.url_entry.get()
        if url:
            self.urls.append(url)
            self.urls_listbox.insert(tk.END, url)
            self.url_entry.delete(0, tk.END)
            self.save_to_json()

    def remove_url(self):
        selected_index = self.urls_listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            removed_url = self.urls.pop(selected_index)
            self.urls_listbox.delete(selected_index)
            print(f"Removed URL: {removed_url}")
            self.save_to_json()

    def clear_file(self):
        self.urls = []
        self.urls_listbox.delete(0, tk.END)
        self.save_to_json()

    def save_to_json(self):
        with open(self.file_path, "w") as json_file:
            json.dump({"urls": self.urls}, json_file)
            print(f"URLs saved to {self.file_path}")

    def read_file(self):
        try:
            with open(self.file_path, "r") as json_file:
                data = json.load(json_file)
                self.urls = data.get("urls", [])
                for url in self.urls:
                    self.urls_listbox.insert(tk.END, url)
        except FileNotFoundError:
            print(f"File {self.file_path} not found. Creating a new one.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramReelsSaverApp(root)
    root.mainloop()
