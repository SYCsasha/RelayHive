import React, { useState } from 'react';
import { AIEmployeeCard } from './AIEmployeeCard';

type ViewType = 'workstation' | 'logs' | 'tasks';

interface LeftSidebarProps {
  isOpen: boolean;
  onClose?: () => void;
}

// Mock data
const mockAIEmployees = [
  { id: '1', name: 'Claude', role: 'Writer', status: 'busy' as const },
  { id: '2', name: 'GPT-4', role: 'Coder', status: 'idle' as const },
  { id: '3', name: 'Gemini', role: 'Analyzer', status: 'thinking' as const },
  { id: '4', name: 'Llama', role: 'Designer', status: 'idle' as const },
];

const mockLogs = [
  { time: '14:36:21', message: 'EA-141号正在生成图片...' },
  { time: '14:36:18', message: 'Coder-02正在检索GitHub' },
  { time: '14:36:15', message: 'Writer-01完成文案编写' },
  { time: '14:36:12', message: 'Designer-03启动UI设计' },
  { time: '14:36:09', message: 'Analyzer-04正在分析数据' },
];

const mockTasks = [
  { id: '1', title: '生成营销文案', priority: 'high', status: 'pending' },
  { id: '2', title: '设计UI原型', priority: 'medium', status: 'in_progress' },
  { id: '3', title: '编写代码模块', priority: 'high', status: 'pending' },
  { id: '4', title: '数据分析报告', priority: 'low', status: 'pending' },
];

export const LeftSidebar: React.FC<LeftSidebarProps> = ({ isOpen, onClose }) => {
  const [currentView, setCurrentView] = useState<ViewType>('workstation');

  const handleViewChange = (view: ViewType) => {
    setCurrentView(view);
  };

  return (
    <div
      className={`fixed left-0 top-0 h-full w-64 bg-gradient-to-b from-slate-50 to-slate-100 shadow-lg transform transition-transform duration-300 z-30 flex flex-col ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      }`}
    >
      {/* Header with view selector */}
      <div className="bg-white border-b border-gray-200 p-3 flex justify-between items-center">
        <h2 className="font-bold text-gray-800">AI 工位</h2>
        <button
          onClick={onClose}
          className="p-1 hover:bg-gray-100 rounded transition-colors"
        >
          ✕
        </button>
      </div>

      {/* View selector tabs */}
      <div className="flex border-b border-gray-200 bg-white">
        <button
          onClick={() => handleViewChange('workstation')}
          className={`flex-1 py-2 px-2 text-xs font-semibold transition-colors ${
            currentView === 'workstation'
              ? 'bg-green-100 text-green-700 border-b-2 border-green-500'
              : 'text-gray-600 hover:bg-gray-50'
          }`}
          title="Workstation - 工位页"
        >
          🟢 工位
        </button>
        <button
          onClick={() => handleViewChange('logs')}
          className={`flex-1 py-2 px-2 text-xs font-semibold transition-colors ${
            currentView === 'logs'
              ? 'bg-yellow-100 text-yellow-700 border-b-2 border-yellow-500'
              : 'text-gray-600 hover:bg-gray-50'
          }`}
          title="Log Tracker - 生产流水日志"
        >
          🟡 日志
        </button>
        <button
          onClick={() => handleViewChange('tasks')}
          className={`flex-1 py-2 px-2 text-xs font-semibold transition-colors ${
            currentView === 'tasks'
              ? 'bg-purple-100 text-purple-700 border-b-2 border-purple-500'
              : 'text-gray-600 hover:bg-gray-50'
          }`}
          title="Task Hall - 事务大厅"
        >
          🟣 任务
        </button>
      </div>

      {/* Content area - scrollable */}
      <div className="flex-1 overflow-y-auto p-3">
        {currentView === 'workstation' && (
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-3">AI 员工花名册</h3>
            {mockAIEmployees.map((employee) => (
              <AIEmployeeCard
                key={employee.id}
                {...employee}
                onConfig={() => alert(`Configure ${employee.name}`)}
                onWorkspace={() => alert(`Open ${employee.name} workspace`)}
              />
            ))}
          </div>
        )}

        {currentView === 'logs' && (
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-3">生产流水日志</h3>
            <div className="space-y-2">
              {mockLogs.map((log, idx) => (
                <div
                  key={idx}
                  className="bg-white p-2 rounded text-xs border-l-2 border-yellow-400 hover:bg-yellow-50 transition-colors"
                >
                  <div className="text-gray-500 font-mono">{log.time}</div>
                  <div className="text-gray-700">{log.message}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {currentView === 'tasks' && (
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-3">事务大厅</h3>
            <div className="space-y-2">
              {mockTasks.map((task) => (
                <div
                  key={task.id}
                  className="bg-white p-3 rounded border-l-4 border-purple-400 hover:shadow-md transition-shadow cursor-pointer"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-grow">
                      <div className="font-semibold text-sm text-gray-800">{task.title}</div>
                      <div className="text-xs text-gray-500 mt-1">
                        {task.status === 'in_progress' ? '进行中' : '待办'}
                      </div>
                    </div>
                    <span
                      className={`text-xs px-2 py-1 rounded ${
                        task.priority === 'high'
                          ? 'bg-red-100 text-red-700'
                          : task.priority === 'medium'
                          ? 'bg-yellow-100 text-yellow-700'
                          : 'bg-green-100 text-green-700'
                      }`}
                    >
                      {task.priority === 'high' ? '高' : task.priority === 'medium' ? '中' : '低'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
