import React, { useState } from 'react';

interface Message {
  id: string;
  sender: 'mascot' | 'user';
  content: string;
  timestamp: Date;
}

interface CentralCanvasProps {
  onLeftSidebarToggle?: () => void;
  onRightSidebarToggle?: () => void;
}

export const CentralCanvas: React.FC<CentralCanvasProps> = ({
  onLeftSidebarToggle,
  onRightSidebarToggle,
}) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      sender: 'mascot',
      content: '你好！我是你的AI助手，准备好开始工作了吗？',
      timestamp: new Date(Date.now() - 60000),
    },
    {
      id: '2',
      sender: 'user',
      content: '帮我生成一份营销文案',
      timestamp: new Date(Date.now() - 30000),
    },
    {
      id: '3',
      sender: 'mascot',
      content: '收到！我已经将任务分配给文案AI了，正在进行中...',
      timestamp: new Date(),
    },
  ]);

  const [currentEmotion, setCurrentEmotion] = useState('😊');

  const emotions = ['😊', '🤔', '😃', '😴', '🥰', '😲'];

  return (
    <div className="flex flex-col h-full bg-gradient-to-b from-blue-50 to-white">
      {/* Header with close/open sidebar hints */}
      <div className="bg-white border-b border-gray-200 px-4 py-3 flex justify-between items-center shadow-sm">
        <button
          onClick={onLeftSidebarToggle}
          className="p-2 hover:bg-gray-100 rounded transition-colors text-lg"
          title="Toggle left sidebar"
        >
          ☰
        </button>
        <h1 className="font-bold text-gray-800">RelayHive 大管家</h1>
        <button
          onClick={onRightSidebarToggle}
          className="p-2 hover:bg-gray-100 rounded transition-colors text-lg"
          title="Toggle right sidebar"
        >
          ☰
        </button>
      </div>

      {/* Emotion card display area */}
      <div className="px-4 py-2 flex justify-center">
        <div className="bg-white rounded-lg shadow px-6 py-2 inline-block border-2 border-yellow-300">
          <div className="text-3xl mb-1">{currentEmotion}</div>
          <div className="text-xs text-gray-600 text-center mb-2">
            {currentEmotion === '😊' && '天气不错，想吃个冰激凌'}
            {currentEmotion === '🤔' && '主人最近好像有点忙'}
            {currentEmotion === '😃' && '今天收到很多有趣的任务'}
            {currentEmotion === '😴' && '有点累，需要休息一下'}
            {currentEmotion === '🥰' && '主人对我很友好呢'}
            {currentEmotion === '😲' && '哇，这个任务好有意思！'}
          </div>
          <button
            onClick={() => {
              const nextEmotion = emotions[(emotions.indexOf(currentEmotion) + 1) % emotions.length];
              setCurrentEmotion(nextEmotion);
            }}
            className="text-xs text-blue-500 hover:text-blue-700"
          >
            切换情绪
          </button>
        </div>
      </div>

      {/* Chat message area - scrollable */}
      <div className="flex-1 overflow-y-auto px-4 py-3 space-y-3">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.sender === 'mascot' ? 'justify-start' : 'justify-end'}`}
          >
            <div
              className={`max-w-xs px-4 py-2 rounded-lg ${
                msg.sender === 'mascot'
                  ? 'bg-blue-100 text-gray-800 rounded-tl-none'
                  : 'bg-green-100 text-gray-800 rounded-tr-none'
              }`}
            >
              <p className="text-sm">{msg.content}</p>
              <p className="text-xs text-gray-500 mt-1">
                {msg.timestamp.toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Information panel */}
      <div className="bg-gray-50 border-t border-gray-200 px-4 py-3 text-center">
        <p className="text-xs text-gray-600 mb-2">💡 使用 # 号开头的命令可以激发吉祥物成为任务包工头</p>
        <p className="text-xs text-gray-500">例如: #1_search 查询最新AI新闻</p>
      </div>
    </div>
  );
};
