import streamlit as st
from textly import sentiment, summarize, extract_text_from_txt, extract_text_from_docx, extract_text_from_pdf
import nltk
import speech_recognition as sr
import pyttsx3
from googletrans import Translator
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

positive_style = "color: green; font-weight: bold;"
negative_style = "color: red; font-weight: bold;"

# Download NLTK resource
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        st.write("Sorry, could not understand audio.")
        return ""

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    st.markdown("<h1 style='text-align: center;  font-size:60px;'>Welcome to TextAnalyzer!</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; font-size:45px;'<p>&#129302;</p></h3>", unsafe_allow_html=True)
   
    # Create two columns for the images
    col1, col2 = st.columns(2)

    # Display the first image in the first column
    with col1:
        st.image("hello123.png", width=300)

    # Display the second image in the second column
    with col2:
        st.image("text mining.png", width=300)
    st.markdown('___')
    st.markdown("<h3 style='text-align: center; color: #F63366; font-size:24px; font-weight: bold;'>Summarize, Sentiment-Analysis, Text & PDF Analysis, and More!</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #F63366; font-size:18px;'>Effortlessly summarize lengthy documents, delve into sentiment analysis, and analyze a variety of text formats including PDFs, TXT files, and Docs. Unlock the power to extract insights from your documents with ease!</p>", unsafe_allow_html=True)
    st.markdown('___')

    st.sidebar.header('TextAnalyzer')
    nav_option = st.sidebar.radio("Go to", ("About", "Summarizations", "Sentiment Analysis", "Translation", "Word Counter", "Parts of Speech (POS) Tagging"))

    if nav_option == "About":
        st.subheader("About")
        st.write("This app utilizes natural language processing techniques to summarize text and perform sentiment analysis.")
        st.write("It leverages NLTK (Natural Language Toolkit) for these tasks! Users can input text, and the app generates both brief and full summaries, allowing for efficient comprehension of textual content. Additionally, the app supports PDF files for summarization and analysis, providing users with a convenient way to process text documents.")

    elif nav_option == "Summarizations":
        st.subheader("Summarizations")
        user_input = st.text_area('Enter text here')
        uploaded_file = st.file_uploader("Choose a file", type=["txt", "docx", "pdf"])
        if uploaded_file is not None:
            file_extension = uploaded_file.name.split(".")[-1]

            if file_extension == "txt":
                text = extract_text_from_txt(uploaded_file)

            elif file_extension == "docx":
                text = extract_text_from_docx(uploaded_file)

            elif file_extension == "pdf":
                text = extract_text_from_pdf(uploaded_file)

        col1, col2 = st.columns(2)
        with col1:
            short = st.button("Brief overview")
        with col2:
            long = st.button("Full summary")

        if short:
            if user_input:
                summary = summarize(user_input, max_value=100, min_value=20)
                summary_word_count = len(summary.split())
                st.subheader("Generated Summary:")
                st.write(summary)
                st.markdown(f"<p style='{positive_style}'>Total words in summary: {summary_word_count}</p>", unsafe_allow_html=True)
                speak(summary)
            elif uploaded_file is not None:
                summary = summarize(text, max_value=100, min_value=20)
                summary_word_count = len(summary.split())
                st.write(summary)
                st.markdown(f"<p style='{positive_style}'>Total words in summary: {summary_word_count}</p>", unsafe_allow_html=True)
                speak(summary)
        if long:
            if user_input:
                summary = summarize(user_input, max_value=400, min_value=90)
                summary_word_count = len(summary.split())
                st.subheader("Generated Summary:")
                st.write(summary)
                st.markdown(f"<p style='{positive_style}'>Total words in summary: {summary_word_count}</p>", unsafe_allow_html=True)
                speak(summary)
            elif uploaded_file is not None:
                summary = summarize(text, max_value=400, min_value=80)
                summary_word_count = len(summary.split())
                st.write(summary)
                st.markdown(f"<p style='{positive_style}'>Total words in summary: {summary_word_count}</p>", unsafe_allow_html=True)
                speak(summary)

    elif nav_option == "Sentiment Analysis":
        st.subheader("Sentiment Analysis")
        user_input = st.text_area('Enter text here')
        uploaded_file = st.file_uploader("Choose a file", type=["txt", "docx", "pdf"])
        if uploaded_file is not None:
            file_extension = uploaded_file.name.split(".")[-1]

            if file_extension == "txt":
                text = extract_text_from_txt(uploaded_file)

            elif file_extension == "docx":
                text = extract_text_from_docx(uploaded_file)

            elif file_extension == "pdf":
                text = extract_text_from_pdf(uploaded_file)

        if st.button("Perform Sentiment Analysis"):
            if user_input:
                sentiment_result = sentiment(user_input)
                if sentiment_result == 'Positive':
                    style = positive_style
                elif sentiment_result == "Negative":
                    style = negative_style
                else:
                    style = ""
                st.subheader("Sentiment Analysis Result:")
                st.markdown(f"**Sentiment:** <span style='{style}'>{sentiment_result}</span>", unsafe_allow_html=True)
                speak(sentiment_result)
            else:
                st.warning("Please input text or upload a file before performing sentiment analysis.")

    elif nav_option == "Translation":
        st.subheader("Text Translation")
        user_input = st.text_area('Enter text here')
        target_language = st.selectbox("Select Target Language", ["Hindi", "Urdu", "Arabic", "French"])
        translator = Translator()
        if st.button("Translate"):
            if user_input:
                translated_text = translator.translate(user_input, dest=target_language.lower()).text
                st.subheader("Translated Text:")
                st.write(translated_text)
            else:
                st.warning("Please input text before translating.")

    elif nav_option == "Word Counter":
        st.subheader("Word Counter")
        user_input = st.text_area('Enter text here')
        if st.button("Count Words"):
            if user_input:
                word_count = len(user_input.split())
                st.write(f"Total Words: {word_count}")
            else:
                st.warning("Please input text before counting words.")

            # Plotting word frequency graph
            if user_input:
                word_list = user_input.split()
                sns.set(style="whitegrid")
                plt.figure(figsize=(10, 6))
                sns.countplot(x=word_list, order=pd.Series(word_list).value_counts().index[:10], palette="viridis")
                plt.title("Top 10 Most Frequent Words")
                plt.xticks(rotation=45)
                plt.xlabel("Words")
                plt.ylabel("Frequency")
                st.pyplot(plt.gcf())

    elif nav_option == "Parts of Speech (POS) Tagging":
        st.subheader("Parts of Speech (POS) Tagging")
        user_input = st.text_area('Enter text here')
        uploaded_file = st.file_uploader("Choose a file", type=["txt", "docx", "pdf"])
        if uploaded_file is not None:
            file_extension = uploaded_file.name.split(".")[-1]

            if file_extension == "txt":
                text = extract_text_from_txt(uploaded_file)

            elif file_extension == "docx":
                text = extract_text_from_docx(uploaded_file)

            elif file_extension == "pdf":
                text = extract_text_from_pdf(uploaded_file)

        if st.button("Perform Parts of Speech (POS) Tagging"):
            if user_input:
                # Tokenize the input text
                words = nltk.word_tokenize(user_input)
                # Perform POS tagging
                pos_tags = nltk.pos_tag(words)
                st.subheader("Parts of Speech (POS) Tagging Result:")
                pos_tags_description = {
                    'CC': 'Coordinating Conjunction',
                    'CD': 'Cardinal Number',
                    'DT': 'Determiner',
                    'EX': 'Existential There',
                    'FW': 'Foreign Word',
                    'IN': 'Preposition or Subordinating Conjunction',
                    'JJ': 'Adjective',
                    'JJR': 'Adjective, comparative',
                    'JJS': 'Adjective, superlative',
                    'LS': 'List Item Marker',
                    'MD': 'Modal',
                    'NN': 'Noun, singular or mass',
                    'NNS': 'Noun, plural',
                    'NNP': 'Proper Noun, singular',
                    'NNPS': 'Proper Noun, plural',
                    'PDT': 'Predeterminer',
                    'POS': 'Possessive Ending',
                    'PRP': 'Personal Pronoun',
                    'PRP$': 'Possessive Pronoun',
                    'RB': 'Adverb',
                    'RBR': 'Adverb, comparative',
                    'RBS': 'Adverb, superlative',
                    'RP': 'Particle',
                    'SYM': 'Symbol',
                    'TO': 'to',
                    'UH': 'Interjection',
                    'VB': 'Verb, base form',
                    'VBD': 'Verb, past tense',
                    'VBG': 'Verb, gerund or present participle',
                    'VBN': 'Verb, past participle',
                    'VBP': 'Verb, non-3rd person singular present',
                    'VBZ': 'Verb, 3rd person singular present',
                    'WDT': 'Wh-determiner',
                    'WP': 'Wh-pronoun',
                    'WP$': 'Possessive Wh-pronoun',
                    'WRB': 'Wh-adverb'
                }
                pos_tags_with_full_forms = [(word, pos_tags_description.get(tag)) for word, tag in pos_tags]
                st.write(pos_tags_with_full_forms)

                # Count POS tags and plot the graph
                pos_df = pd.DataFrame(pos_tags_with_full_forms, columns=['Word', 'POS Tag'])
                plt.figure(figsize=(10, 6))
                sns.countplot(data=pos_df, x='POS Tag', palette="viridis")
                plt.title("Parts of Speech (POS) Tag Distribution")
                plt.xlabel("POS Tags")
                plt.ylabel("Frequency")
                plt.xticks(rotation=45, ha='right')
                st.pyplot(plt.gcf())
            else:
                st.warning("Please input text or upload a file before performing Parts of Speech (POS) Tagging.")

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #666666;'>This app uses NLTK (Natural Language Toolkit), a leading platform for building Python programs to work with human language data. NLTK is a comprehensive library for natural language processing tasks such as tokenization, stemming, tagging, parsing, and more.<br> Creator: Mohd Kaif 153</p>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
