import React from 'react';

const ChatBox = ({ messages }) => {
  if (!messages || messages.length === 0) return null;

  return (
    <div className="bg-white shadow-md rounded-xl p-6 mb-6 border-l-4 border-blue-500">
      <h3 className="text-lg font-semibold text-gray-800 mb-3">System Status</h3>
      <div className="space-y-2">
        {messages.map((msg, idx) => {
          const isLast = idx === messages.length - 1;
          const isDone = msg === "Analysis Complete!" || msg.includes("Error");
          const isError = msg.includes("Error");
          
          return (
            <div key={idx} className={`flex items-center space-x-3 text-sm p-3 rounded-lg border ${isError ? 'bg-red-50 border-red-100 text-red-700' : 'bg-blue-50 border-blue-100 text-blue-800'}`}>
              {isLast && !isDone ? (
                <span className="flex h-3 w-3 relative">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-blue-500"></span>
                </span>
              ) : (
                <span className={`h-3 w-3 rounded-full ${isError ? 'bg-red-500' : 'bg-green-500'}`}></span>
              )}
              <span className="font-medium">{msg}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ChatBox;
