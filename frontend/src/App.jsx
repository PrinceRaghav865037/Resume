import React, { useState } from 'react';
import axios from 'axios';
import UploadForm from './components/UploadForm';
import ChatBox from './components/ChatBox';
import Results from './components/Results';

function App() {
  const [file, setFile] = useState(null);
  const [jdText, setJdText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [results, setResults] = useState(null);

  const simulateProgress = () => {
    const steps = [
      "Uploading resume...",
      "Extracting skills from resume...",
      "Analyzing Job Description...",
      "Simulating skill assessment interview...",
      "Evaluating gap analysis...",
      "Generating personalized learning plan..."
    ];
    
    setMessages([]);
    // Because the backend API is a single synchronous call, we simulate the progress 
    // steps in the UI to give the user a sense of what's happening.
    steps.forEach((step, i) => {
      setTimeout(() => {
        // Only add messages if we are still loading
        setMessages(prev => {
          if (prev.includes("Analysis Complete!") || prev.some(m => m.includes("Error"))) return prev;
          return [...prev, step];
        });
      }, i * 2000); 
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !jdText) return;

    setIsLoading(true);
    setResults(null);
    simulateProgress(); 

    const formData = new FormData();
    formData.append('file', file);
    formData.append('jd_text', jdText);

    try {
      const response = await axios.post('http://127.0.0.1:8000/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setMessages(prev => [...prev.filter(m => !m.includes("Error") && !m.includes("Complete")), "Analysis Complete!"]);
      setResults(response.data);
    } catch (error) {
      console.error(error);
      const errorMsg = error.response?.data?.detail || error.message || "An unknown error occurred.";
      setMessages(prev => [...prev, `Error: ${errorMsg}`]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#f8fafc] py-10 px-4 sm:px-6 lg:px-8 font-sans text-gray-900">
      <div className="max-w-4xl mx-auto space-y-8">
        
        <div className="text-center mb-10">
          <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 tracking-tight mb-2">
            AI Resume Analyzer
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Upload your resume and the target job description to instantly receive a personalized skill gap assessment and dynamic learning roadmap.
          </p>
        </div>

        <UploadForm 
          file={file} 
          setFile={setFile} 
          jdText={jdText} 
          setJdText={setJdText} 
          onSubmit={handleSubmit} 
          isLoading={isLoading} 
        />

        <ChatBox messages={messages} />

        <Results results={results} />

      </div>
    </div>
  );
}

export default App;
