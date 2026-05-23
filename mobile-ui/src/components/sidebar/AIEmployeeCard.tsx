import React from 'react';

interface AIEmployeeCardProps {
  id: string;
  name: string;
  role: string;
  avatar?: string;
  status: 'idle' | 'busy' | 'thinking' | 'crashed' | 'scheduled';
  onConfig?: () => void;
  onWorkspace?: () => void;
}

const statusColors = {
  idle: 'bg-green-500',
  busy: 'bg-red-500',
  thinking: 'bg-blue-500',
  crashed: 'bg-gray-500',
  scheduled: 'bg-yellow-500',
};

const statusLabels = {
  idle: '空闲',
  busy: '忙碌',
  thinking: '思考',
  crashed: '宕机',
  scheduled: '计划中',
};

export const AIEmployeeCard: React.FC<AIEmployeeCardProps> = ({
  id,
  name,
  role,
  avatar,
  status,
  onConfig,
  onWorkspace,
}) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-3 flex items-center gap-3 hover:shadow-lg transition-shadow">
      {/* Avatar */}
      <div className="w-12 h-12 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex-shrink-0 flex items-center justify-center text-white font-bold">
        {avatar ? avatar : name.charAt(0)}
      </div>

      {/* Info */}
      <div className="flex-grow min-w-0">
        <div className="font-semibold text-sm text-gray-900">{name}</div>
        <div className="text-xs text-gray-600">{role}</div>
        <div className="flex items-center gap-2 mt-1">
          <div className={`w-2 h-2 rounded-full ${statusColors[status]}`}></div>
          <span className="text-xs text-gray-500">{statusLabels[status]}</span>
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex gap-2 flex-shrink-0">
        <button
          onClick={onConfig}
          className="p-2 rounded hover:bg-gray-100 transition-colors"
          title="Configure AI"
        >
          ⚙️
        </button>
        <button
          onClick={onWorkspace}
          className="p-2 rounded hover:bg-gray-100 transition-colors"
          title="View Workspace"
        >
          💼
        </button>
      </div>
    </div>
  );
};
