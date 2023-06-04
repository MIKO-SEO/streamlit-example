import streamlit as st
import pytesseract
from google.cloud import translate_v2 as translate

# Set up Google Cloud Translation API credentials
translate_client = translate.Client()

# Set up Tesseract OCR engine
pytesseract.pytesseract.tesseract_cmd = 'path/to/tesseract'

def translate_text(text, target_lang):
    # Translate text using Google Cloud Translation API
    translation = translate_client.translate(text, target_language=target_lang)
    return translation['translatedText']

def extract_text_from_image(image):
    # Use Tesseract OCR to extract text from manga page image
    text = pytesseract.image_to_string(image)
    return text

def process_manga_chapter(manga_images, target_lang):
    translated_chapter = []
    
    for image in manga_images:
        # Extract text from manga page image
        text = extract_text_from_image(image)
        
        # Translate the extracted text
        translated_text = translate_text(text, target_lang)
        
        # Append the translated text to the translated chapter
        translated_chapter.append(translated_text)
    
    return translated_chapter

# Streamlit app
def main():
    st.title("Auto Manga Translation Tool")
    st.write("Upload a manga chapter to translate:")
    
    uploaded_files = st.file_uploader("Upload images", accept_multiple_files=True)
    target_language = st.selectbox("Select target language", ["English", "Spanish", "French"])
    
    if st.button("Translate"):
        if uploaded_files is not None:
            manga_images = [pytesseract.image.load_img(file) for file in uploaded_files]
            translated_chapter = process_manga_chapter(manga_images, target_language)
            
            st.write("Translated Chapter:")
            for page_num, page_text in enumerate(translated_chapter, start=1):
                st.subheader(f"Page {page_num}")
                st.write(page_text)
        else:
            st.warning("Please upload manga images.")
    
if __name__ == '__main__':
    main()
