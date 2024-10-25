from django.shortcuts import render
from .forms import ImageUploadForm
from google.generativeai import configure, GenerativeModel
import textwrap
from PIL import Image

# Configure the Google Generative AI API
GOOGLE_API_KEY = "AIzaSyA3Qz-3UGkvx8DAj9hMp8hJw-zc3QNcp00"
configure(api_key=GOOGLE_API_KEY)
model = GenerativeModel("gemini-1.5-flash")

def to_markdown(text):
    text = text.replace("•", "  *")
    return textwrap.indent(text, "> ", predicate=lambda _: True)

def image_upload_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the image file
            image_file = request.FILES['image']
            img = Image.open(image_file)

            try:
                # Call the model to generate content based on the image
                response = model.generate_content(
                    [
                        "Based on the image of an item provided by the user, which represents a product they wish to recycle, repurpose, or upcycle, please analyze the item and generate one innovative and practical idea for extending its lifecycle. Your suggestions should focus on creative uses that go beyond traditional recycling methods, especially for items not typically considered recyclable. After identifying a potential new use, provide a detailed step-by-step guide on how the user can transform the item from its current state into the new, repurposed form. Your recommendations should be feasible for the average person to accomplish with common tools and materials. Please draw from your extensive database of knowledge to ensure the ideas are both unique and practical, highlighting any specific techniques or materials needed for the transformation.",
                        img,  # Use the PIL.Image object here
                    ],
                    stream=True,
                )

                # Resolve the response to ensure it's fully processed
                response.resolve()

                # Retrieve the generated text safely after resolving
                generated_text = to_markdown(response.text)

            except Exception as e:
                # Handle any exceptions that occur during processing
                print(f"An error occurred: {e}")
                generated_text = "An error occurred while generating content."

            # Return the result to the template
            return render(request, 'myapp/image_upload_result.html', {'generated_text': generated_text})

    else:
        form = ImageUploadForm()  # Create the form if not a POST submission

    return render(request, 'myapp/image_upload.html', {'form': form})
