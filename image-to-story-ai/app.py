from flask import Flask, render_template, request
import os
from transformers import BlipProcessor, BlipForConditionalGeneration, pipeline
from PIL import Image

# Flask App Initialization
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Generate Caption using BLIP
def generate_caption(image_path):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    image = Image.open(image_path).convert('RGB')
    inputs = processor(image, return_tensors="pt")
    caption_ids = model.generate(**inputs)
    caption = processor.decode(caption_ids[0], skip_special_tokens=True)
    return caption

# Generate Story using GPT
from transformers import pipeline

def generate_story(caption):
    try:
        # Use GPT-2 to generate the story
        story_generator = pipeline("text-generation", model="gpt2")
        story = story_generator(caption, max_length=150, num_return_sequences=1)
        return story[0]["generated_text"]
    except Exception as e:
        return f"An error occurred: {e}"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Save the uploaded image
        image = request.files['image']
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)

        # Generate caption and story
        caption = generate_caption(image_path)
        story = generate_story(caption)

        return render_template("index.html", image_path=image_path, caption=caption, story=story)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
