import streamlit as st
import os
from utils.parser import extract_text

# Try to import LLM client and handle missing API key
try:
    from utils.llm_client import analyze_resume
    LLM_AVAILABLE = True
except ValueError as e:
    LLM_AVAILABLE = False
    LLM_ERROR = str(e)

def main():
    st.set_page_config(
        page_title="Resume ATS Score Checker",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 Resume ATS Score Checker")
    st.markdown("**Powered by NVIDIA Nemotron LLM**")
    
    # Check if LLM is available
    if not LLM_AVAILABLE:
        st.error("🔑 API Configuration Required")
        st.markdown(f"**Error:** {LLM_ERROR}")
        st.markdown("""
        **To fix this:**
        1. Create a `.env` file in the project root
        2. Add your NVIDIA API key: `NVIDIA_API_KEY=your_api_key_here`
        3. Get your API key from: https://build.nvidia.com/
        4. Restart the application
        """)
        st.stop()
    
    st.markdown("Upload your resume and job description to get an ATS compatibility score and improvement suggestions.")
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📋 Resume Upload")
        uploaded_file = st.file_uploader(
            "Choose your resume file",
            type=['pdf', 'docx', 'txt'],
            help="Supported formats: PDF, DOCX, TXT"
        )
        
        resume_text = ""
        if uploaded_file is not None:
            # Debug information
            st.info(f"File info: {uploaded_file.name}, Size: {uploaded_file.size} bytes, Type: {uploaded_file.type}")
            
            # Test PDF library import in Streamlit context
            try:
                from pypdf import PdfReader
                st.success(f"✅ pypdf available in Streamlit context")
            except ImportError:
                try:
                    import PyPDF2
                    st.success(f"✅ PyPDF2 available in Streamlit context, version: {PyPDF2.__version__}")
                except ImportError as e:
                    st.error(f"❌ No PDF library available in Streamlit context: {e}")
            
            try:
                resume_text = extract_text(uploaded_file)
                st.success(f"✅ Resume uploaded successfully! ({len(resume_text)} characters)")
                
                # Show preview of extracted text
                with st.expander("Preview extracted text"):
                    st.text_area("Resume content preview", resume_text[:500] + "..." if len(resume_text) > 500 else resume_text, height=150, disabled=True)
            except Exception as e:
                st.error(f"❌ Error processing resume: {str(e)}")
                # Show more detailed error info
                import traceback
                st.code(traceback.format_exc())
    
    with col2:
        st.header("💼 Job Description")
        job_desc = st.text_area(
            "Paste the job description here",
            height=200,
            placeholder="Copy and paste the complete job description including requirements, skills, and qualifications..."
        )
        
        if job_desc:
            st.success(f"✅ Job description added! ({len(job_desc)} characters)")
    
    # Analysis section
    st.markdown("---")
    
    if st.button("🔍 Check ATS Score", type="primary", use_container_width=True):
        if not resume_text:
            st.error("❌ Please upload a resume first!")
            return
        
        if not job_desc.strip():
            st.error("❌ Please provide a job description!")
            return
        
        # Show loading spinner
        with st.spinner("🤖 Analyzing your resume with AI... This may take a few moments."):
            try:
                result = analyze_resume(resume_text, job_desc)
                
                # Display results in the specified text format
                st.markdown("## 📊 ATS Analysis Report")
                
                # Overall ATS Score Section
                score = result.get('ats_score', 0)
                score_summary = result.get('score_summary', 'Analysis completed')
                
                st.markdown("### 📊 Overall ATS Score")
                if score >= 80:
                    score_color = "🟢"
                    score_status = "Excellent"
                elif score >= 60:
                    score_color = "🟡"
                    score_status = "Good"
                else:
                    score_color = "🔴"
                    score_status = "Needs Improvement"
                
                st.markdown(f"**{score}/100** - {score_summary}")
                st.progress(score / 100)
                
                # Score breakdown visualization
                if 'score_breakdown' in result and result['score_breakdown']:
                    breakdown_cols = st.columns(5)
                    breakdown = result['score_breakdown']
                    
                    categories = [
                        ("Keywords", "keywords", 25),
                        ("Experience", "experience", 25),
                        ("Skills", "skills", 20),
                        ("Education", "education", 15),
                        ("Format", "formatting", 15)
                    ]
                    
                    for i, (name, key, max_score) in enumerate(categories):
                        with breakdown_cols[i]:
                            category_score = breakdown.get(key, 0)
                            percentage = (category_score / max_score) * 100 if max_score > 0 else 0
                            st.metric(name, f"{category_score}/{max_score}", f"{percentage:.0f}%")
                
                # Keywords Analysis
                st.markdown("---")
                keyword_col1, keyword_col2 = st.columns([1, 1])
                
                with keyword_col1:
                    st.markdown("### ✅ Matched Keywords")
                    matched_keywords = result.get('matched_keywords', [])
                    if matched_keywords:
                        for keyword in matched_keywords:
                            st.markdown(f"• {keyword}")
                    else:
                        st.info("No specific matched keywords identified.")
                
                with keyword_col2:
                    st.markdown("### ❌ Missing Critical Keywords")
                    missing_keywords = result.get('missing_keywords', [])
                    if missing_keywords:
                        for keyword in missing_keywords:
                            st.markdown(f"• {keyword}")
                    else:
                        st.info("No missing keywords identified.")
                
                # Detailed Analysis Section
                if 'detailed_analysis' in result and result['detailed_analysis']:
                    st.markdown("---")
                    st.markdown("## 🔍 Detailed Analysis")
                    
                    analysis = result['detailed_analysis']
                    
                    # Strengths and Weaknesses
                    strength_col, weakness_col = st.columns([1, 1])
                    
                    with strength_col:
                        st.markdown("### 💪 Key Strengths")
                        strengths = analysis.get('strengths', [])
                        if strengths:
                            for strength in strengths:
                                st.success(f"✓ {strength}")
                        else:
                            st.info("Strengths analysis not available.")
                    
                    with weakness_col:
                        st.markdown("### ⚠️ Areas for Improvement")
                        weaknesses = analysis.get('weaknesses', [])
                        if weaknesses:
                            for weakness in weaknesses:
                                st.warning(f"⚡ {weakness}")
                        else:
                            st.info("Weakness analysis not available.")
                    
                    # Detailed assessments
                    if analysis.get('keyword_analysis'):
                        st.markdown("#### 🔤 Keyword Analysis")
                        st.write(analysis['keyword_analysis'])
                    
                    if analysis.get('experience_assessment'):
                        st.markdown("#### 💼 Experience Assessment")
                        st.write(analysis['experience_assessment'])
                    
                    if analysis.get('skills_gap_analysis'):
                        st.markdown("#### 🎯 Skills Gap Analysis")
                        st.write(analysis['skills_gap_analysis'])
                
                # Text Replacements Section
                if 'text_replacements' in result and result['text_replacements']:
                    st.markdown("---")
                    st.markdown("### ✏️ Text Replacements (Resume Improvements)")
                    
                    for i, replacement in enumerate(result['text_replacements'], 1):
                        section = replacement.get('section', 'Section')
                        original = replacement.get('original_text', 'Original text not provided')
                        improved = replacement.get('improved_text', 'Improved text not provided')
                        reason = replacement.get('reason', 'Improvement reason not provided')
                        
                        st.markdown(f"**{i}. {section}**")
                        st.markdown(f"**Current Text:** {original}")
                        st.markdown(f"**Improved Text:** {improved}")
                        st.markdown(f"**Why this helps:** {reason}")
                        st.markdown("")
                
                # Detailed Suggestions
                st.markdown("---")
                st.markdown("### 🎯 Detailed Suggestions")
                
                detailed_suggestions = result.get('detailed_suggestions', [])
                if detailed_suggestions:
                    # Group by priority
                    high_priority = [s for s in detailed_suggestions if s.get('priority') == 'High']
                    medium_priority = [s for s in detailed_suggestions if s.get('priority') == 'Medium']
                    low_priority = [s for s in detailed_suggestions if s.get('priority') == 'Low']
                    
                    for priority_group, priority_name, priority_emoji in [
                        (high_priority, "High Priority", "🔴"),
                        (medium_priority, "Medium Priority", "🟡"),
                        (low_priority, "Low Priority", "🟢")
                    ]:
                        if priority_group:
                            st.markdown(f"**{priority_emoji} {priority_name}**")
                            for suggestion in priority_group:
                                category = suggestion.get('category', 'General')
                                issue = suggestion.get('issue', 'Issue not specified')
                                solution = suggestion.get('solution', 'Solution not provided')
                                impact = suggestion.get('expected_impact', 'Impact not specified')
                                
                                st.markdown(f"• **Category:** {category}")
                                st.markdown(f"  **Issue:** {issue}")
                                st.markdown(f"  **Suggested Fix:** {solution}")
                                st.markdown(f"  **Expected Impact:** {impact}")
                                st.markdown("")
                else:
                    # Fallback to simple suggestions
                    suggestions = result.get('suggestions', [])
                    if suggestions:
                        for i, suggestion in enumerate(suggestions, 1):
                            st.markdown(f"• {suggestion}")
                    else:
                        st.info("No specific suggestions available.")
                
                # ATS Optimization Tips
                if 'ats_optimization_tips' in result and result['ats_optimization_tips']:
                    st.markdown("### 🎯 ATS Optimization Tips")
                    for tip in result['ats_optimization_tips']:
                        st.info(f"💡 {tip}")
                
                # Competitive Analysis
                if 'competitive_analysis' in result and result['competitive_analysis']:
                    st.markdown("---")
                    st.markdown("## 📊 Competitive Analysis")
                    st.write(result['competitive_analysis'])
                
                # Score Breakdown Explanation
                if 'score_explanation' in result and result['score_explanation']:
                    st.markdown("---")
                    st.markdown("### � Scrore Breakdown Explanation")
                    st.markdown(result['score_explanation'])
                
                # Next Steps
                if 'next_steps' in result and result['next_steps']:
                    st.markdown("---")
                    st.markdown("### 🚀 Next Steps")
                    next_steps = result['next_steps']
                    if '1.' in next_steps and '2.' in next_steps:
                        # Parse numbered list more carefully
                        import re
                        steps = re.split(r'\d+\.', next_steps)
                        for step in steps:
                            clean_step = step.strip()
                            if clean_step and len(clean_step) > 3:  # Avoid empty or very short fragments
                                st.markdown(f"• {clean_step}")
                    else:
                        st.markdown(next_steps)
                
                # Generate Text Report
                st.markdown("---")
                st.markdown("### 📄 Copy Text Report")
                
                text_report = generate_text_report(result)
                st.text_area(
                    "Complete ATS Analysis Report (Copy this text)",
                    text_report,
                    height=400,
                    help="Copy this formatted report to share or save your analysis"
                )
                
                # Fallback Overall Feedback
                if not result.get('score_explanation') and not result.get('next_steps'):
                    st.markdown("---")
                    st.markdown("### 📝 Summary")
                    overall_feedback = result.get('overall_feedback', result.get('feedback', 'Analysis completed successfully.'))
                    st.write(overall_feedback)
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.info("Please check your internet connection and try again.")
    
    # Footer
    st.markdown("---")
    st.markdown("**Note:** This tool provides AI-powered suggestions. Always review and customize recommendations based on your specific situation.")

def generate_text_report(result: dict) -> str:
    """
    Generate a clean text report matching the specified format requirements
    """
    report = []
    
    # Overall ATS Score
    score = result.get('ats_score', 0)
    score_summary = result.get('score_summary', 'Analysis completed')
    report.append("📊 Overall ATS Score")
    report.append(f"{score}/100")
    report.append(f"{score_summary}")
    report.append("")
    
    # Matched Keywords
    report.append("✅ Matched Keywords")
    matched_keywords = result.get('matched_keywords', [])
    if matched_keywords:
        for keyword in matched_keywords:
            report.append(f"• {keyword}")
    else:
        report.append("• No specific matched keywords identified")
    report.append("")
    
    # Missing Critical Keywords
    report.append("❌ Missing Critical Keywords")
    missing_keywords = result.get('missing_keywords', [])
    if missing_keywords:
        for keyword in missing_keywords:
            report.append(f"• {keyword}")
    else:
        report.append("• No missing keywords identified")
    report.append("")
    
    # Text Replacements
    text_replacements = result.get('text_replacements', [])
    if text_replacements:
        report.append("✏️ Text Replacements (Resume Improvements)")
        for i, replacement in enumerate(text_replacements, 1):
            section = replacement.get('section', 'Section')
            original = replacement.get('original_text', 'Original text not provided')
            improved = replacement.get('improved_text', 'Improved text not provided')
            reason = replacement.get('reason', 'Improvement reason not provided')
            
            report.append(f"{i}. Section: {section}")
            report.append(f"   Current Text: {original}")
            report.append(f"   Improved Text: {improved}")
            report.append(f"   Why this helps: {reason}")
            report.append("")
    
    # Detailed Suggestions
    detailed_suggestions = result.get('detailed_suggestions', [])
    if detailed_suggestions:
        report.append("🎯 Detailed Suggestions")
        
        # Group by priority
        high_priority = [s for s in detailed_suggestions if s.get('priority') == 'High']
        medium_priority = [s for s in detailed_suggestions if s.get('priority') == 'Medium']
        low_priority = [s for s in detailed_suggestions if s.get('priority') == 'Low']
        
        for priority_group, priority_name in [
            (high_priority, "High Priority"),
            (medium_priority, "Medium Priority"),
            (low_priority, "Low Priority")
        ]:
            if priority_group:
                report.append(f"{priority_name}:")
                for suggestion in priority_group:
                    category = suggestion.get('category', 'General')
                    issue = suggestion.get('issue', 'Issue not specified')
                    solution = suggestion.get('solution', 'Solution not provided')
                    impact = suggestion.get('expected_impact', 'Impact not specified')
                    
                    report.append(f"• Category: {category}")
                    report.append(f"  Issue: {issue}")
                    report.append(f"  Suggested Fix: {solution}")
                    report.append(f"  Expected Impact: {impact}")
                    report.append("")
    
    # Score Breakdown Explanation
    score_explanation = result.get('score_explanation', '')
    if score_explanation:
        report.append("📈 Score Breakdown Explanation")
        report.append(score_explanation)
        report.append("")
    
    # Next Steps
    next_steps = result.get('next_steps', '')
    if next_steps:
        report.append("🚀 Next Steps")
        if '1.' in next_steps and '2.' in next_steps:
            # Parse numbered list more carefully
            import re
            steps = re.split(r'\d+\.', next_steps)
            for step in steps:
                clean_step = step.strip()
                if clean_step and len(clean_step) > 3:  # Avoid empty or very short fragments
                    report.append(f"• {clean_step}")
        else:
            report.append(next_steps)
        report.append("")
    
    return "\n".join(report)

if __name__ == "__main__":
    main()