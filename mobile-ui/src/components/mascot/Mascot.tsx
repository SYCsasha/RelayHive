import React, { useState } from 'react';

interface MascotProps {
  onLeftHandGesture?: () => void;
  onRightHandGesture?: () => void;
}

export const Mascot: React.FC<MascotProps> = ({ onLeftHandGesture, onRightHandGesture }) => {
  const [leftGestureActive, setLeftGestureActive] = useState(false);
  const [rightGestureActive, setRightGestureActive] = useState(false);

  const handleLeftGesture = () => {
    setLeftGestureActive(true);
    onLeftHandGesture?.();
    setTimeout(() => setLeftGestureActive(false), 500);
  };

  const handleRightGesture = () => {
    setRightGestureActive(true);
    onRightHandGesture?.();
    setTimeout(() => setRightGestureActive(false), 500);
  };

  return (
    <div className="flex flex-col items-center justify-center h-full select-none">
      {/* Mascot Character */}
      <div className="relative w-32 h-40 mb-4">
        {/* Head/Face */}
        <div className="absolute left-1/2 top-0 transform -translate-x-1/2 w-24 h-24 bg-gradient-to-b from-yellow-300 to-yellow-400 rounded-full shadow-lg flex items-center justify-center">
          {/* Eyes */}
          <div className="flex gap-6">
            <div className="w-6 h-6 bg-black rounded-full"></div>
            <div className="w-6 h-6 bg-black rounded-full"></div>
          </div>
        </div>

        {/* Body */}
        <div className="absolute left-1/2 top-20 transform -translate-x-1/2 w-16 h-14 bg-gradient-to-b from-orange-300 to-orange-400 rounded-lg shadow-md"></div>

        {/* Left Hand - Slap gesture */}
        <div
          className={`absolute left-0 top-20 w-6 h-6 bg-yellow-300 rounded-full shadow-md transform transition-transform duration-300 cursor-pointer ${
            leftGestureActive ? 'translate-x-2 -translate-y-2' : ''
          }`}
          onClick={handleLeftGesture}
          title="Left hand - Slap left sidebar"
        >
          <div className="absolute w-8 h-2 bg-yellow-300 transform -translate-y-0 left-1/2 top-1/2"></div>
        </div>

        {/* Right Hand - Grab gesture */}
        <div
          className={`absolute right-0 top-20 w-6 h-6 bg-yellow-300 rounded-full shadow-md transform transition-transform duration-300 cursor-pointer ${
            rightGestureActive ? '-translate-x-2 -translate-y-2' : ''
          }`}
          onClick={handleRightGesture}
          title="Right hand - Grab right sidebar"
        >
          <div className="absolute w-8 h-2 bg-yellow-300 transform -translate-y-0 -left-2 top-1/2"></div>
        </div>
      </div>

      {/* Instruction text */}
      <div className="text-sm text-gray-500 mt-4 text-center">
        <p>👈 Slap Left | Grab Right 👉</p>
      </div>
    </div>
  );
};
