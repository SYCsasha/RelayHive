import React, { useState } from 'react';

interface PluginProps {
  id: string;
  name: string;
  icon: string;
  description: string;
  status: 'connected' | 'disconnected' | 'pending';
}

interface RightSidebarProps {
  isOpen: boolean;
  onClose?: () => void;
}

const mockPlugins: PluginProps[] = [
  {
    id: '1',
    name: 'GitHub',
    icon: '🐙',
    description: '代码提交',
    status: 'connected',
  },
  {
    id: '2',
    name: '画廊展览',
    icon: '🎨',
    description: '设计图提交',
    status: 'connected',
  },
  {
    id: '3',
    name: '办公桌面',
    icon: '📄',
    description: '文档提交',
    status: 'connected',
  },
  {
    id: '4',
    name: '数据仓库',
    icon: '📊',
    description: '数据导出',
    status: 'pending',
  },
  {
    id: '5',
    name: '云盘存储',
    icon: '☁️',
    description: '文件备份',
    status: 'disconnected',
  },
];

const PluginCard: React.FC<PluginProps & { onClick?: () => void }> = ({
  icon,
  name,
  description,
  status,
  onClick,
}) => {
  const statusColor =
    status === 'connected'
      ? 'bg-green-100 text-green-700'
      : status === 'pending'
      ? 'bg-yellow-100 text-yellow-700'
      : 'bg-gray-100 text-gray-700';

  return (
    <div
      onClick={onClick}
      className="bg-white rounded-lg p-4 mb-3 border border-gray-200 hover:shadow-lg transition-shadow cursor-pointer"
    >
      <div className="flex items-start justify-between mb-2">
        <div className="text-3xl">{icon}</div>
        <span className={`text-xs px-2 py-1 rounded font-semibold ${statusColor}`}>
          {status === 'connected' ? '已连接' : status === 'pending' ? '待配置' : '未连接'}
        </span>
      </div>
      <h3 className="font-semibold text-sm text-gray-800">{name}</h3>
      <p className="text-xs text-gray-600 mt-1">{description}</p>
    </div>
  );
};

export const RightSidebar: React.FC<RightSidebarProps> = ({ isOpen, onClose }) => {
  const [expandedPlugin, setExpandedPlugin] = useState<string | null>(null);

  const handlePluginClick = (pluginId: string) => {
    setExpandedPlugin(expandedPlugin === pluginId ? null : pluginId);
  };

  return (
    <div
      className={`fixed right-0 top-0 h-full w-72 bg-gradient-to-b from-slate-50 to-slate-100 shadow-lg transform transition-transform duration-300 z-30 flex flex-col ${
        isOpen ? 'translate-x-0' : 'translate-x-full'
      }`}
    >
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-3 flex justify-between items-center">
        <h2 className="font-bold text-gray-800">📦 交付插件</h2>
        <button
          onClick={onClose}
          className="p-1 hover:bg-gray-100 rounded transition-colors"
        >
          ✕
        </button>
      </div>

      {/* Info text */}
      <div className="bg-blue-50 border-l-4 border-blue-500 p-3 text-xs text-blue-800">
        <p>AI员工将完成的成果投放到对应插件中</p>
      </div>

      {/* Plugin list - scrollable */}
      <div className="flex-1 overflow-y-auto p-3">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">可用目的地</h3>
        {mockPlugins.map((plugin) => (
          <PluginCard
            key={plugin.id}
            {...plugin}
            onClick={() => handlePluginClick(plugin.id)}
          />
        ))}

        {/* Section for expanded plugin details */}
        {expandedPlugin && (
          <div className="mt-4 p-4 bg-white rounded-lg border-2 border-blue-400">
            <h4 className="font-semibold text-gray-800 mb-3">
              {mockPlugins.find((p) => p.id === expandedPlugin)?.name} - 详细配置
            </h4>
            <div className="space-y-2 text-sm">
              <div>
                <label className="block text-gray-600 mb-1">API 密钥</label>
                <input
                  type="password"
                  placeholder="••••••••"
                  className="w-full px-2 py-1 border border-gray-300 rounded text-xs"
                />
              </div>
              <div>
                <label className="block text-gray-600 mb-1">端点</label>
                <input
                  type="text"
                  placeholder="https://api.example.com"
                  className="w-full px-2 py-1 border border-gray-300 rounded text-xs"
                />
              </div>
              <button className="w-full mt-3 bg-blue-500 text-white py-1 px-2 rounded hover:bg-blue-600 transition-colors text-xs font-semibold">
                保存配置
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Footer with action */}
      <div className="bg-white border-t border-gray-200 p-3">
        <button className="w-full bg-green-500 text-white py-2 px-3 rounded hover:bg-green-600 transition-colors font-semibold text-sm">
          + 添加新插件
        </button>
      </div>
    </div>
  );
};
