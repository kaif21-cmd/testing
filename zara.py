import streamlit as st
from textly import sentiment, summarize, extract_text_from_txt, extract_text_from_docx, extract_text_from_pdf
import nltk

positive_style = "color: green; font-weight: bold;"
negative_style = "color: red; font-weight: bold;"

def main():
    st.markdown("<h1 style='text-align: center; color: white; font-size:60px;'>Welcome to TextAnalyzer!</h1>", unsafe_allow_html=True)
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

    st.sidebar.header('Navigation')
    nav_option = st.sidebar.radio("Go to", ("About", "Summarization", "Sentiment Analysis"))

    if nav_option == "About":
        st.subheader("About")
        st.markdown("<h3 style='text-align: left; color:#F63366; font-size:18px;'><b>What is this App about?<b></h3>", unsafe_allow_html=True)
        st.write("This app utilizes natural language processing techniques to summarize text and perform sentiment analysis.")
        st.write("It leverages NLTK (Natural Language Toolkit) for these tasks! Users can input text, and the app generates both brief and full summaries, allowing for efficient comprehension of textual content. Additionally, the app supports PDF files for summarization and analysis, providing users with a convenient way to process text documents.")

    elif nav_option == "Summarization":
        st.subheader("Summarization")
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
            elif uploaded_file is not None:
                summary = summarize(text, max_value=100, min_value=20)
                summary_word_count = len(summary.split())
                st.write(summary)
                st.markdown(f"<p style='{positive_style}'>Total words in summary: {summary_word_count}</p>", unsafe_allow_html=True)
        if long:
            if user_input:
                summary = summarize(user_input, max_value=400, min_value=90)
                summary_word_count = len(summary.split())
                st.subheader("Generated Summary:")
                st.write(summary)
                st.markdown(f"<p style='{positive_style}'>Total words in summary: {summary_word_count}</p>", unsafe_allow_html=True)
            elif uploaded_file is not None:
                summary = summarize(text, max_value=400, min_value=80)
                summary_word_count = len(summary.split())
                st.write(summary)
                st.markdown(f"<p style='{positive_style}'>Total words in summary: {summary_word_count}</p>", unsafe_allow_html=True)

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
            sentiment_result = sentiment(user_input)
            if sentiment_result == 'Positive':
                style = positive_style
            elif sentiment_result == "Negative":
                style = negative_style
            else:
                style = ""
            st.subheader("Sentiment Analysis Result:")
            st.markdown(f"**Sentiment:** <span style='{style}'>{sentiment_result}</span>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #666666;'>This app uses NLTK (Natural Language Toolkit), a leading platform for building Python programs to work with human language data. NLTK is a comprehensive library for natural language processing tasks such as tokenization, stemming, tagging, parsing, and more.<br> Creater: Mohd Kaif 153</p>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
