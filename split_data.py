#C:\Users\user\source\python\kidey_Project



import os
import shutil
import random

# --- Configuration ---
# Change 'archive' to the actual folder name where your 'Normal' and 'stone' folders are located.
source_dir = 'C:\\Users\\user\\source\\python\\kidey_Project\\dataset\\archive (1)'  
base_dir = 'dataset'    

# Categories as per your dataset
categories = ['Normal', 'stone']

# Split ratio: 80% for training, 20% for testing
split_ratio = 0.8

def split_dataset():
    print("🚀 Starting the dataset splitting process...")
    
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"❌ Error: The folder '{source_dir}' was not found. Please check the folder name in the script.")
        return

    # Create the target folder structure
    for cat in categories:
        os.makedirs(os.path.join(base_dir, 'train', cat), exist_ok=True)
        os.makedirs(os.path.join(base_dir, 'test', cat), exist_ok=True)

    for cat in categories:
        src_path = os.path.join(source_dir, cat)
        
        # Check if the category folder exists in source
        if not os.path.exists(src_path):
            print(f"⚠️ Warning: Category folder '{cat}' not found in {source_dir}. Skipping...")
            continue
            
        # Get all image files
        all_images = [f for f in os.listdir(src_path) if os.path.isfile(os.path.join(src_path, f))]
        
        # Shuffle images randomly
        random.shuffle(all_images)
        
        # Calculate split point
        split_point = int(len(all_images) * split_ratio)
        
        train_images = all_images[:split_point]
        test_images = all_images[split_point:]
        
        # Copy images to train folder
        for img in train_images:
            shutil.copy(os.path.join(src_path, img), os.path.join(base_dir, 'train', cat, img))
        
        # Copy images to test folder
        for img in test_images:
            shutil.copy(os.path.join(src_path, img), os.path.join(base_dir, 'test', cat, img))

        print(f"✅ Category {cat}: {len(train_images)} images to train, {len(test_images)} to test.")

    print("\n✨ All done! Your dataset is now perfectly split and organized in the 'dataset' folder!")

if __name__ == "__main__":
    split_dataset()
