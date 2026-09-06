import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# --- Configuration ---
# مسیر پوشه‌هایی که در مرحله قبل ساختیم
train_dir = 'dataset/train'
test_dir = 'dataset/test'

# سایز استاندارد برای تمام عکس‌ها (استاندارد مدل‌های جهانی)
IMG_SIZE = (224, 224) 
BATCH_SIZE = 32 # در هر مرحله ۳۲ عکس وارد مدل شود

print("🚀 Starting data pre-processing...")

try:
    # 1. تعریف ابزار پردازش عکس‌ها
    # rescale=1./255 باعث می‌شود تمام اعداد پیکسل‌ها بین 0 و 1 قرار بگیرند (نرمال‌سازی)
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,      # کمی عکس‌ها را می‌چرخاند تا مدل قوی‌تر شود (Data Augmentation)
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,   # عکس‌ها را قرینه می‌کند
        zoom_range=0.2
    )

    test_datagen = ImageDataGenerator(rescale=1./255)

    # 2. خواندن عکس‌ها از پوشه‌ها و تبدیل آن‌ها به فرمت قابل فهم برای مدل
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary' # چون فقط دو دسته داریم: سالم یا سنگ
    )

    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary'
    )

    print("\n✅ Data pre-processing completed successfully!")
    print(f"Found {train_generator.samples} images in train set.")
    print(f"Found {test_generator.samples} images in test set.")
    print(f"Classes found: {train_generator.class_indices}")

except Exception as e:
    print(f"❌ An error occurred: {e}")
    print("\n💡 Tip: Make sure the 'dataset' folder is in the same directory as this script.")
    