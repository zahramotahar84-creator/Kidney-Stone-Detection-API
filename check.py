import os

# 1. Print the current working directory to see where Python is looking
print("--- Current Working Directory ---")
print(os.getcwd())
print("-" * 30)

# 2. Check the 'dataset' folder
path = 'dataset'
if os.path.exists(path):
    print(f"✅ Folder '{path}' found!")
    
    # List items inside the dataset folder
    try:
        items = os.listdir(path)
        print(f"Items inside dataset: {items}")
        
        # Check each subfolder (like train and test)
        for item in items:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                sub_items = os.listdir(item_path)
                print(f"\n📁 Folder '{item}' found.")
                
                # Check Normal and Stone folders inside train or test
                for sub_item in sub_items:
                    sub_item_path = os.path.join(item_path, sub_item)
                    if os.path.isdir(sub_item_path):
                        files = os.listdir(sub_item_path)
                        print(f"   └── 📂 {sub_item}: {len(files)} files")
    except Exception as e:
        print(f"Error reading dataset folder: {e}")
else:
    print(f"❌ Folder '{path}' NOT found in this location!")

print("-" * 30)
print("Done!")