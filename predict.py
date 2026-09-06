import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# ۱. بارگذاری مدل آموزش‌دیده
model_path = 'kidney_model.h5'
if os.path.exists(model_path):
    model = tf.keras.models.load_model(model_path)
    print("✅ مدل با موفقیت بارگذاری شد. آماده تشخیص هستم!")
else:
    print("❌ خطای بحرانی: فایل kidney_model.h5 پیدا نشد!")
    print("لطفا مطمئن شو که این فایل در کنار همین کد قرار دارد.")
    exit()

def predict_kidney_image(img_path):
    # ۲. پیش‌پردازش عکس ورودی
    try:
        # تغییر اندازه عکس به ۱۵۰ در ۱۵۰ (مطابق با آموزشی که دادیم)
        img = image.load_img(img_path, target_size=(150, 150))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) # اضافه کردن بعد برای بچ (Batch)
        img_array /= 255.0 # نرمال‌سازی پیکسل‌ها

        # ۳. پیش‌بینی توسط مدل
        prediction = model.predict(img_array, verbose=0)
        
        # تحلیل خروجی (sigmoid)
        if prediction[0][0] > 0.5:
            result = "سنگ کلیه (Kidney Stone)"
            confidence = prediction[0][0] * 100
        else:
            result = "سالم (Normal)"
            confidence = (1 - prediction[0][0]) * 100
            
        print(f"\n-----------------------------------")
        print(f"🔍 نتیجه تحلیل: {result}")
        print(f"🎯 میزان اطمینان مدل: {confidence:.2f}%")
        print(f"-----------------------------------")
        
    except Exception as e:
        print(f"❌ خطا در خواندن عکس: {e}")

# --- بخش اجرای تست ---
if __name__ == "__main__":
    print("\n🌟 به سیستم تشخیص هوشمند کلیه خوش آمدید!")
    print("برای خروج حرف 'q' را تایپ کنید.")
    while True:
        path = input("\nلطفاً مسیر عکس را وارد کنید (مثال: test.jpg): ")
        if path.lower() == 'q':
            print("خداحافظ! موفق باشی زهرا جان! 💎")
            break
        predict_kidney_image(path)