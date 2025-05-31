import React, { useState } from 'react';

interface ChatInterfaceProps {
  onCodeGenerated: (code: string, language: string) => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ onCodeGenerated }) => {
  const [input, setInput] = useState('');

  const sendMessage = () => {
    if (!input.trim()) return;
    const mockCode = `# Generated from: ${input}\nprint("Hello from AI!")`;
    onCodeGenerated(mockCode, 'python');
    setInput('');
  };

  return (
    <div className="flex flex-col h-full bg-gray-900 text-white">
      <div className="p-4 border-b border-gray-700">
        <h2 className="text-lg font-semibold">AI Assistant</h2>
      </div>
      
      <div className="flex-1 p-4">
        <div className="bg-gray-700 p-3 rounded">
          <p className="text-sm">Hello! Ask me to generate code.</p>
        </div>
      </div>

      <div className="p-4 border-t border-gray-700">
        <div className="flex space-x-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Generate a Python function..."
            className="flex-1 p-3 bg-gray-800 text-white rounded"
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          />
          <button
            onClick={sendMessage}
            className="px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
