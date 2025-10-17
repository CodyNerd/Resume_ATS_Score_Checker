# Resume ATS Score Checker

A powerful Streamlit application that evaluates how well your resume matches a job description using AI-powered analysis. Get instant feedback on your ATS compatibility score, keyword matching, and actionable improvement suggestions.

## 🚀 Features

- **AI-Powered Analysis**: Uses NVIDIA Nemotron LLM for intelligent resume evaluation
- **Multiple File Formats**: Supports PDF, DOCX, and TXT resume uploads
- **Comprehensive Scoring**: Get detailed ATS scores (0-100) with explanations
- **Keyword Analysis**: See matched and missing keywords from job descriptions
- **Actionable Suggestions**: Receive specific recommendations to improve your resume
- **User-Friendly Interface**: Clean, intuitive Streamlit web interface

## 📋 Requirements

- Python 3.8 or higher
- Internet connection for AI analysis
- Supported resume formats: PDF, DOCX, TXT

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/CodyNerd/Resume_ATS_Score_Checker.git
   cd Resume_ATS_Score_Checker
   ```

2. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your NVIDIA API key
   # Get your API key from: https://build.nvidia.com/
   ```
   
   Edit the `.env` file and replace `your_nvidia_api_key_here` with your actual NVIDIA API key.

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, navigate to the URL shown in your terminal

## 📖 Usage

### Step 1: Upload Your Resume
- Click "Choose your resume file" 
- Select a PDF, DOCX, or TXT file
- The app will extract and preview the text content

### Step 2: Add Job Description
- Copy the complete job description from the job posting
- Paste it into the "Job Description" text area
- Include requirements, skills, and qualifications for best results

### Step 3: Get Your ATS Score
- Click "Check ATS Score" button
- Wait for the AI analysis (usually 10-30 seconds)
- Review your comprehensive results

### Understanding Your Results

**ATS Score (0-100)**
- 🟢 80-100: Excellent match, high ATS compatibility
- 🟡 60-79: Good match, some improvements needed
- 🔴 0-59: Needs significant improvements

**Analysis Sections**:
- **📊 Overall ATS Score**: Numerical score with competitiveness summary
- **✅ Matched Keywords**: Skills and terms found in both resume and job description
- **❌ Missing Critical Keywords**: Important terms from job description not in resume
- **✏️ Text Replacements**: Specific resume improvements with before/after examples
- **🎯 Detailed Suggestions**: Priority action items (High/Medium/Low) with expected impact
- **📈 Score Breakdown**: Explanation of how the ATS score was calculated
- **🚀 Next Steps**: Concise action plan for resume improvement

**Text Report**: Copy the complete analysis in a structured text format for easy sharing

## 🔧 Technical Details

### Project Structure
```
resume-ats-checker/
├── app.py                 # Main Streamlit application
├── utils/
│   ├── llm_client.py     # NVIDIA LLM API integration
│   └── parser.py         # Resume text extraction utilities
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### Key Components

**app.py**
- Streamlit user interface
- File upload handling
- Results display and formatting

**utils/llm_client.py**
- NVIDIA Nemotron API integration
- Prompt engineering for resume analysis
- Response parsing and validation

**utils/parser.py**
- Text extraction from PDF, DOCX, TXT files
- Error handling for different file formats
- Text cleaning and normalization

## 🔑 API Configuration

### Getting Your NVIDIA API Key

1. Visit [NVIDIA Build](https://build.nvidia.com/)
2. Sign up or log in to your NVIDIA account
3. Navigate to the API section
4. Generate a new API key for the Nemotron model
5. Copy the API key and add it to your `.env` file

### Environment Variables

The application uses the following environment variables:

- `NVIDIA_API_KEY` (required): Your NVIDIA API key
- `NVIDIA_BASE_URL` (optional): API base URL (default: https://integrate.api.nvidia.com/v1)
- `NVIDIA_MODEL` (optional): Model name (default: nvidia/llama-3.3-nemotron-super-49b-v1.5)

### Deployment

For deployment on platforms like Streamlit Cloud, Heroku, or similar:

1. Set the `NVIDIA_API_KEY` as an environment variable in your deployment platform
2. Do not commit the `.env` file to your repository
3. Use the `.env.example` file as a template for required variables

## 🚨 Troubleshooting

### Common Issues

**"PyPDF2 library is required"**
```bash
pip install PyPDF2
```

**"python-docx library is required"**
```bash
pip install python-docx
```

**"Error during analysis"**
- Check your internet connection
- Ensure the resume and job description are not empty
- Try with a smaller file if the resume is very large

**PDF text extraction issues**
- Some PDFs (especially image-based) may not extract text properly
- Try converting to DOCX or TXT format
- Ensure the PDF is not password-protected

### Performance Tips

- Keep resume files under 5MB for faster processing
- Provide complete job descriptions for better analysis
- Use text-based files (DOCX/TXT) for fastest processing

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## 🚀 Deployment

For deployment instructions (Streamlit Cloud, Heroku, Docker, etc.), see [DEPLOYMENT.md](DEPLOYMENT.md).

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

This tool provides AI-powered suggestions for resume improvement. Always review and customize recommendations based on your specific situation and the actual job requirements. The ATS score is an estimate and may not reflect the exact scoring of all ATS systems.
