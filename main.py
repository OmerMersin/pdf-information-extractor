import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os
import argparse
import spacy

nlp = spacy.load('es_core_news_md')

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Generate text by given pdf')

# Add arguments
parser.add_argument('arg1', type=str, help='PDF name to get text')

# Parse the arguments
args = parser.parse_args()

n = list()

class ExtractInfo():
    def __init__(self, file_name):
        self.file = file_name

        self.pdf_to_file(self.file)

        text = self.get_text()

        self.get_email(text)
        
    def pdf_to_file(self, pdf):
        images = convert_from_path(f'{pdf}.pdf')
        for i in range(len(images)):
            # Save pages as images in the pdf
            images[i].save('page'+ str(i) +'.jpg', 'JPEG')

    def get_text(self):

        folder_path = "."  # Replace with the path to your folder

        # Loop through each file in the folder
        for file_name in os.listdir(folder_path):
            # Check if the file has a .txt extension
            if file_name.endswith('.jpg'):
                # Open the image file using PIL
                image = Image.open(f'{file_name}')
                # Convert the image to grayscale
                image = image.convert('L')
                # Use Tesseract to extract the text from the image
                text = pytesseract.image_to_string(image)
                # Print the extracted text
                print(text)

                # Get the full path of the file
                file_path = os.path.join(folder_path, file_name)
                
                # Delete the file
                os.remove(file_path)

                doc = nlp(text)

                for ent in doc.ents:
                    if ent.label_ == 'PER':
                        print(ent.text)
                
                return text

    def get_email(self, text):
        words = text.split()
        print(words)
        for word in words:
            # print(word)
            with open("names.txt", "r") as names:
                names = names.readlines()
                for name in names:
                    l = len(name)
                    name = name[0:l-1]
                    n.append(name)
                if word in n:
                    print(word)
            if "nome" in word.lower():
                print(word)
            if "@" in word:
                print(word)


if __name__ == "__main__":
    # Access the values of the arguments
    file_name = args.arg1

    file = ExtractInfo(file_name)

