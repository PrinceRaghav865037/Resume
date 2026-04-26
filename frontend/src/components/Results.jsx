import React from 'react';

const Results = ({ results }) => {
  if (!results) return null;

  const { assessment_scores, gap_analysis, learning_plan } = results;

  return (
    <div className="space-y-6">
      <div className="bg-white shadow-md rounded-xl p-6">
        <h2 className="text-xl font-bold mb-4 text-gray-800 border-b pb-2">Skill Assessment</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {Object.entries(assessment_scores || {}).map(([skill, level]) => (
            <div key={skill} className="flex justify-between items-center p-3 border rounded-lg bg-gray-50 shadow-sm">
              <span className="font-medium text-gray-700">{skill}</span>
              <span className={`px-3 py-1 text-xs font-bold rounded-full 
                ${level === 'Advanced' ? 'bg-green-100 text-green-800 border border-green-200' : 
                  level === 'Intermediate' ? 'bg-yellow-100 text-yellow-800 border border-yellow-200' : 
                  'bg-red-100 text-red-800 border border-red-200'}`}>
                {level}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white shadow-md rounded-xl p-6">
        <h2 className="text-xl font-bold mb-4 text-gray-800 border-b pb-2">Gap Analysis</h2>
        
        <div className="mb-5">
          <h3 className="text-sm font-bold text-green-700 mb-2 uppercase tracking-wide">Strong Skills</h3>
          <div className="flex flex-wrap gap-2">
            {gap_analysis?.strong_skills?.length > 0 ? gap_analysis.strong_skills.map(s => (
              <span key={s} className="bg-green-50 border border-green-200 text-green-700 px-3 py-1 rounded-full text-sm font-medium">{s}</span>
            )) : <span className="text-gray-400 text-sm italic">None identified</span>}
          </div>
        </div>

        <div className="mb-5">
          <h3 className="text-sm font-bold text-yellow-700 mb-2 uppercase tracking-wide">Weak Skills</h3>
          <div className="flex flex-wrap gap-2">
            {gap_analysis?.weak_skills?.length > 0 ? gap_analysis.weak_skills.map(s => (
              <span key={s} className="bg-yellow-50 border border-yellow-200 text-yellow-700 px-3 py-1 rounded-full text-sm font-medium">{s}</span>
            )) : <span className="text-gray-400 text-sm italic">None identified</span>}
          </div>
        </div>

        <div>
          <h3 className="text-sm font-bold text-red-700 mb-2 uppercase tracking-wide">Missing Skills</h3>
          <div className="flex flex-wrap gap-2">
            {gap_analysis?.missing_skills?.length > 0 ? gap_analysis.missing_skills.map(s => (
              <span key={s} className="bg-red-50 border border-red-200 text-red-700 px-3 py-1 rounded-full text-sm font-medium">{s}</span>
            )) : <span className="text-gray-400 text-sm italic">None identified</span>}
          </div>
        </div>
      </div>

      <div className="bg-white shadow-md rounded-xl p-6">
        <h2 className="text-xl font-bold mb-4 text-gray-800 border-b pb-2">Learning Plan</h2>
        {learning_plan?.length > 0 ? (
          <div className="space-y-4">
            {learning_plan.map((item, idx) => (
              <div key={idx} className="border border-blue-100 rounded-xl p-5 bg-gradient-to-r from-blue-50 to-white shadow-sm">
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-3 gap-2">
                  <h3 className="text-lg font-bold text-blue-900">{item.skill}</h3>
                  <span className="text-xs font-bold bg-blue-100 text-blue-800 px-3 py-1 rounded-full border border-blue-200">
                    Duration: {item.duration}
                  </span>
                </div>
                <p className="text-sm text-gray-700 mb-4 whitespace-pre-line leading-relaxed">{item.plan}</p>
                <div className="bg-white p-3 rounded-lg border border-gray-100">
                  <h4 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Recommended Resources</h4>
                  <ul className="space-y-1">
                    {item.resources?.map((res, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm">
                        <span className="text-blue-500 mt-0.5">•</span>
                        <a href={res} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800 hover:underline break-all">
                          {res}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 italic">No learning plan required. Candidate meets all requirements!</p>
        )}
      </div>
    </div>
  );
};

export default Results;
