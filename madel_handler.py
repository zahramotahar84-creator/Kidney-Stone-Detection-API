
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# مسیر فایل مدل - چون همه فایل‌ها در یک پوشه هستند، فقط اسم فایل کافی است
MODEL_PATH = 'kidney_model.h5'

# بارگذاری مدل در حافظه (برای اینکه هر بار با هر درخواست لود نشود و سرعت بالا برود)
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")

def get_prediction(img_path):
    """
    این تابع مسیر عکس را می‌گیرد، آن را پیش‌پردازش می‌کند 
    و نتیجه تشخیص (سالم یا سنگ) را برمی‌گرداند.
    """
    try:
        # 1. لود کردن عکس با سایزی که مدل آموزش دیده (150x150)
        img = image.load_img(img_path, target_size=(150, 150))
        
        # 2. تبدیل عکس به آرایه عددی
        img_array = image.img_to_array(img)
        
        # 3. اضافه کردن بعد Batch (تبدیل به شکل (1, 150, 150, 3))
        img_array = np.expand_dims(img_array, axis=0)
        
        # 4. نرمال‌سازی (تبدیل مقادیر 0-255 به 0-1)
        img_array /= 255.0
        
        # 5. پیش‌بینی توسط مدل
        prediction = model.predict(img_array, verbose=0)
        
        # 6. تحلیل نتیجه (فرض بر این است که مدل Binary است)
        # اگر خروجی بیشتر از 0.5 باشد -> سنگ کلیه / کمتر باشد -> سالم
        score = prediction[0][0]
        
        if score > 0.5:
            diagnosis = "Kidney Stone (سنگ کلیه)"
            confidence = float(score * 100)
        else:
            diagnosis = "Normal (سالم)"
            confidence = float((1 - score) * 100)
            
        return diagnosis, confidence

    except Exception as e:
        print(f"❌ Prediction Error: {e}")
        return f"Error analyzing image: {str(e)}", 0.0
