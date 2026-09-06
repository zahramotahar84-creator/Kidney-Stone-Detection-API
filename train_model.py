import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# 1. Basic Settings
img_height = 150
img_width = 150
batch_size = 32

# 2. Data Preparation (Data Augmentation)
# This helps the model learn better by rotating and zooming images
train_datagen = ImageDataGenerator(
    rescale=1./255,           # Normalize pixel values to be between 0 and 1
    rotation_range=20,         # Randomly rotate images
    width_shift_range=0.2,     # Randomly shift images horizontally
    height_shift_range=0.2,    # Randomly shift images vertically
    horizontal_flip=True,      # Flip images horizontally
    zoom_range=0.2             # Randomly zoom inside images
)

test_datagen = ImageDataGenerator(rescale=1./255)

# Loading images from the folders
train_generator = train_datagen.flow_from_directory(
    'dataset/train',
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'         # Binary because we have 2 classes: Normal or Stone
)

test_generator = test_datagen.flow_from_directory(
    'dataset/test',
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'
)

# 3. Brain Architecture (CNN Model)
model = models.Sequential([
    # Layer 1: Detecting basic edges
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    layers.MaxPooling2D((2, 2)),
    
    # Layer 2: Detecting more complex shapes
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    
    # Layer 3: Final feature extraction
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    
    # Flattening the output for the decision layers
    layers.Flatten(),
    
    # Decision Layers (Dense Layers)
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5), # Prevents overfitting (memorizing data)
    layers.Dense(1, activation='sigmoid') # Final output: probability between 0 and 1
])

# 4. Learning Configuration
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Display the brain structure
model.summary()

print("\n✅ Brain Architecture is Ready! Now we can start training.")
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

# 1. Initial Settings
img_height = 150
img_width = 150
batch_size = 32
epochs = 10  # Number of times the model sees the entire dataset

# 2. Data Preparation (Data Augmentation)
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2
)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    'dataset/train',
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'
)

test_generator = test_datagen.flow_from_directory(
    'dataset/test',
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'
)

# 3. Brain Architecture (CNN Model)
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# 4. Start Training Process
print("\n⏳ Training started... Please wait. This might take a while!")
history = model.fit(
    train_generator,
    epochs=epochs,
    validation_data=test_generator
)

# 5. Save the trained model
model.save('kidney_model.h5')
print("\n✅ Model saved as 'kidney_model.h5'!")

# 6. Plot Progress Graphs
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.title('Training and Validation Loss')
plt.legend()

plt.show()

print("\n🎉 Training Complete! You can now check the charts.")