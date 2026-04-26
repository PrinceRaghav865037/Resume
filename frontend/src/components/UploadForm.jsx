import React from 'react';

const UploadForm = ({ file, setFile, jdText, setJdText, onSubmit, isLoading }) => {
  return (
    <div className="bg-white shadow-md rounded-xl p-6 mb-6">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Analyze Candidate</h2>
      <form onSubmit={onSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Resume (PDF/DOCX)</label>
          <input
            type="file"
            accept=".pdf,.doc,.docx"
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-blue-500 outline-none"
            required
            disabled={isLoading}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Job Description</label>
          <textarea
            rows="5"
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            className="w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-blue-500 outline-none"
            placeholder="Paste the job description here..."
            required
            disabled={isLoading}
          ></textarea>
        </div>
        <button
          type="submit"
          disabled={isLoading || !file || !jdText}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? 'Processing...' : 'Start Analysis'}
        </button>
      </form>
    </div>
  );
};

export default UploadForm;
