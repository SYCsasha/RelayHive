import React, { useState } from 'react';
import { LeftSidebar } from '../sidebar/LeftSidebar';
import { RightSidebar } from '../sidebar/RightSidebar';
import { CentralCanvas } from '../canvas/CentralCanvas';
import { BottomInput } from '../input/BottomInput';
import { Mascot } from '../mascot/Mascot';

export const MainLayout: React.FC = () => {
  const [leftSidebarOpen, setLeftSidebarOpen] = useState(false);
  const [rightSidebarOpen, setRightSidebarOpen] = useState(false);
  const [showMascot, setShowMascot] = useState(true);

  const handleLeftGesture = () => {
    setLeftSidebarOpen(!leftSidebarOpen);
  };

  const handleRightGesture = () => {
    setRightSidebarOpen(!rightSidebarOpen);
  };

  return (
    <div className="h-screen w-screen bg-white flex flex-col overflow-hidden">
      {/* Overlay for opened sidebars */}
      {(leftSidebarOpen || rightSidebarOpen) && (
        <div
          className="fixed inset-0 bg-black bg-opacity-30 z-20"
          onClick={() => {
            setLeftSidebarOpen(false);
            setRightSidebarOpen(false);
          }}
        ></div>
      )}

      {/* Main content area */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Sidebar */}
        <LeftSidebar
          isOpen={leftSidebarOpen}
          onClose={() => setLeftSidebarOpen(false)}
        />

        {/* Center area with mascot/canvas toggle */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Toggle button for mascot view */}
          {showMascot && (
            <button
              onClick={() => setShowMascot(false)}
              className="absolute top-4 right-32 z-10 px-3 py-1 bg-blue-500 text-white rounded text-xs hover:bg-blue-600 transition-colors"
            >
              进入聊天
            </button>
          )}

          {/* Mascot OR Canvas view */}
          {showMascot ? (
            <div className="flex-1 flex items-center justify-center">
              <Mascot
                onLeftHandGesture={handleLeftGesture}
                onRightHandGesture={handleRightGesture}
              />
            </div>
          ) : (
            <>
              <div className="flex-1 overflow-hidden">
                <CentralCanvas
                  onLeftSidebarToggle={() => setLeftSidebarOpen(!leftSidebarOpen)}
                  onRightSidebarToggle={() => setRightSidebarOpen(!rightSidebarOpen)}
                />
              </div>
            </>
          )}
        </div>

        {/* Right Sidebar */}
        <RightSidebar
          isOpen={rightSidebarOpen}
          onClose={() => setRightSidebarOpen(false)}
        />
      </div>

      {/* Bottom input - visible only in canvas view */}
      {!showMascot && (
        <BottomInput
          onSendMessage={(message) => {
            console.log('Message sent:', message);
            setShowMascot(false);
          }}
          onModelSwitch={(model) => {
            console.log('Model switched to:', model);
          }}
          onFileUpload={(file) => {
            console.log('File uploaded:', file.name);
          }}
          onVoiceToggle={(active) => {
            console.log('Voice mode:', active ? 'on' : 'off');
          }}
        />
      )}
    </div>
  );
};
