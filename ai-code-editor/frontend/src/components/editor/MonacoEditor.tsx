import React from 'react';

interface MonacoEditorProps {
  value: string;
  onChange: (value: string) => void;
  language: string;
  theme?: string;
}

const MonacoEditor: React.FC<MonacoEditorProps> = ({ value, onChange }) => {
  return (
    <div className="h-full w-full bg-gray-800 text-white p-4">
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full h-full bg-gray-900 text-white p-4 font-mono resize-none border-none outline-none"
        placeholder="Generated code will appear here..."
      />
    </div>
  );
};

export default MonacoEditor;
