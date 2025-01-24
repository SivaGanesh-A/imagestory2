import os

# Define the folder structure
structure = {
    "image-to-story-ai": [
        "app.py",
        "requirements.txt",
        "README.md",
        "templates/index.html",
        "static/uploads/",
        "models/"
    ]
}

# Create folders and files
for base, files in structure.items():
    for item in files:
        path = os.path.join(base, item)
        if item.endswith('/'):  # Create folders
            os.makedirs(path, exist_ok=True)
        else:  # Create files
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                pass

print("Project structure created successfully!")
