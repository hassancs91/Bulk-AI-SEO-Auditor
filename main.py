
import streamlit as st
from helpers import free_seo_audit, ai_analysis,api_seo_audit,display_wrapped_json




def main():
    st.title("Bulk AI SEO Auditor")
    
    audit_type = st.radio("Choose audit type:", ("Simple Built-in Audit", "Full API Audit"))
    
    uploaded_file = st.file_uploader("Upload a text file containing URLs (one per line)", type="txt")
    
    if uploaded_file is not None:
        urls = uploaded_file.getvalue().decode("utf-8").splitlines()
        st.write(f"Found {len(urls)} URLs in the uploaded file.")
        
        if st.button("Start Analysis"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, url in enumerate(urls):
                progress = (i + 1) / len(urls)
                progress_bar.progress(progress)
                status_text.text(f"Analyzing URL {i+1} of {len(urls)}: {url}")
                
                with st.expander(f"SEO Audit for {url}", expanded=False):
                    if audit_type == "Simple Built-in Audit":
                        report = free_seo_audit(url)
                    else:
                        report = api_seo_audit(url)
                    
                    ai_result = ai_analysis(report)  # You'll need to implement this function
                    
                    ai_tab, seo_tab = st.tabs(["AI Analysis", "SEO Report"])
                    
                    with ai_tab:
                        st.subheader("AI Analysis")
                        st.write(ai_result)
                    
                    with seo_tab:
                        st.subheader("SEO Report")
                        display_wrapped_json(report)
            
            status_text.text("Analysis complete!")
            progress_bar.progress(1.0)

if __name__ == "__main__":
    main()