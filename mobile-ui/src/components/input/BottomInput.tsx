import React, { useState, useRef } from 'react';

interface BottomInputProps {
  onSendMessage?: (message: string) => void;
  onModelSwitch?: (model: string) => void;
  onFileUpload?: (file: File) => void;
  onVoiceToggle?: (active: boolean) => void;
}

const models = ['Gemini', 'Claude 3', 'GPT-4', 'Llama 2', 'LLaMA 70B'];

export const BottomInput: React.FC<BottomInputProps> = ({
  onSendMessage,
  onModelSwitch,
  onFileUpload,
  onVoiceToggle,
}) => {
  const [message, setMessage] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [showModelSelector, setShowModelSelector] = useState(false);
  const [selectedModel, setSelectedModel] = useState(models[0]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSendMessage = () => {
    if (message.trim()) {
      onSendMessage?.(message);
      setMessage('');
    }
  };

  const handleVoiceToggle = () => {
    const newState = !isListening;
    setIsListening(newState);
    onVoiceToggle?.(newState);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      onFileUpload?.(e.target.files[0]);
    }
  };

  const handleModelSwitch = (model: string) => {
    setSelectedModel(model);
    setShowModelSelector(false);
    onModelSwitch?.(model);
  };

  return (
    <div className="bg-white border-t border-gray-200 p-3 flex flex-col gap-2">
      {/* Model selector - card flip animation */}
      {showModelSelector && (
        <div className="bg-gradient-to-b from-slate-50 to-slate-100 rounded-lg p-3 border border-gray-200 animate-fade-in">
          <div className="flex justify-between items-center mb-2">
            <span className="font-semibold text-sm text-gray-800">选择模型</span>
            <button
              onClick={() => setShowModelSelector(false)}
              className="text-sm text-gray-600 hover:text-gray-800"
            >
              ✕
            </button>
          </div>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {models.map((model) => (
              <button
                key={model}
                onClick={() => handleModelSwitch(model)}
                className={`w-full px-3 py-2 rounded text-left text-sm transition-colors ${
                  selectedModel === model
                    ? 'bg-blue-500 text-white font-semibold'
                    : 'bg-white text-gray-800 hover:bg-gray-100 border border-gray-300'
                }`}
              >
                {model}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input controls row */}
      <div className="flex gap-2 items-end">
        {/* File upload button */}
        <input
          ref={fileInputRef}
          type="file"
          onChange={handleFileSelect}
          className="hidden"
        />
        <button
          onClick={() => fileInputRef.current?.click()}
          className="p-2 rounded hover:bg-gray-100 transition-colors text-xl flex-shrink-0"
          title="Upload file"
        >
          📎
        </button>

        {/* Text input field */}
        <div className="flex-1 flex items-center gap-2 bg-gray-50 rounded-lg border border-gray-300 px-3 py-2 focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-400">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="输入消息或 # 命令..."
            className="flex-1 bg-transparent outline-none text-sm"
          />
        </div>

        {/* Model switcher button */}
        <button
          onClick={() => setShowModelSelector(!showModelSelector)}
          className="px-2 py-2 rounded bg-purple-100 text-purple-700 hover:bg-purple-200 transition-colors text-xs font-semibold flex-shrink-0"
          title="Switch model"
        >
          {selectedModel.split(' ')[0]}
        </button>

        {/* Voice input button - polymorphic */}
        <button
          onMouseDown={handleVoiceToggle}
          onMouseUp={handleVoiceToggle}
          className={`p-2 rounded transition-all flex-shrink-0 font-bold text-lg ${
            isListening
              ? 'listening bg-red-500 text-white shadow-lg'
              : 'bg-blue-500 text-white hover:bg-blue-600'
          }`}
          title={isListening ? '按住说话' : '点击语音/按住实时监听'}
        >
          🎤
        </button>

        {/* Send button */}
        <button
          onClick={handleSendMessage}
          disabled={!message.trim()}
          className="p-2 rounded bg-green-500 text-white hover:bg-green-600 disabled:bg-gray-300 transition-colors flex-shrink-0 font-bold text-lg"
          title="Send message"
        >
          ➤
        </button>
      </div>

      {/* Voice status indicator */}
      {isListening && (
        <div className="flex items-center gap-2 px-3 py-1 bg-red-50 rounded text-xs text-red-700">
          <span className="inline-block w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
          实时待机监听模式 - 随时可以插话
        </div>
      )}

      {/* Command hint */}
      <div className="text-xs text-gray-500 px-2">
        💡 提示: 使用"#1_search"格式的标签协议可以激发AI员工
      </div>
    </div>
  );
};
