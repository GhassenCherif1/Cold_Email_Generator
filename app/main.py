import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio


def create_streamlit_app(llm, portfolio):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-42816?from=job%20search%20funnel")
    submit_button = st.button("Submit")

    if submit_button:
        loader = WebBaseLoader([url_input])
        data = loader.load().pop().page_content
        portfolio.load_portfolio()
        job = llm.extract_jobs(data)[0]
        skills = job.get('skills', [])
        links = portfolio.query_links(skills)
        email = llm.write_mail(job, links)
        st.code(email, language='markdown')


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio)

