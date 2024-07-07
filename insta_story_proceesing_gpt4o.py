from openai import OpenAI
import os
import base64

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = ""

# Initialize the OpenAI client
client = OpenAI()


text = ""

def encode_image(image_path):
    """Encode an image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def process_images(folder_path):
    """Process all images in the specified folder"""
    global text  
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            image_path = os.path.join(folder_path, filename)
            try:
                base64_image = encode_image(image_path)
            except Exception as e:
                print(f"Error processing image {filename}: {e}")
                continue

           
            prompt = {
                "role": "system",
                "content": "You are a helpful assistant that extracts information about skincare and skincare products from informative images. Try to summarise the content of the image , it be maybe a discsussion of a skincare issue or a skincare product and it's use case etc."
            }

            message = {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Extract useful information about the skincare issue or the skincare product from the image.Answer in a single paragraph form'{filename}'"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                ]
            }

            try:
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[prompt, message],
                    temperature=0.0,  
                )

            
                text += response.choices[0].message.content + '\n'
                # print(response.choices[0].message.content)
            except Exception as e:
                print(f"Error processing image {filename}: {e}")
                continue


folder_path = '/Users/mhmh/Desktop/p2/skincare/cleaned/FAQs'  # Path to your folder with cleaned images
process_images(folder_path)

print("Text from image processing:")
print(text)
