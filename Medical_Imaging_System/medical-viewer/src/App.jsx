import { useState, useEffect } from 'react';
import axios from 'axios';

export default function App() {
  const [activeStudy, setActiveStudy] = useState({
    id: "Waiting for scan...",
    patientId: "--",
    confidence: 0,
    heatmapUrl: "",
    status: "Pending Review"
  });

  // Auto-fetch the latest scan every 3 seconds
  useEffect(() => {
    const fetchLatest = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/latest');
        if (response.data.status === 'success') {
          setActiveStudy(prev => ({
            ...prev,
            id: response.data.id,
            patientId: response.data.patientId,
            confidence: response.data.confidence,
            heatmapUrl: response.data.heatmapUrl
          }));
        }
      } catch (error) {
        console.error("API disconnected");
      }
    };

    const interval = setInterval(fetchLatest, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleDecision = (decision) => {
    setActiveStudy(prev => ({ ...prev, status: decision }));
    alert(`Study ${activeStudy.id} marked as: ${decision}`);
  };

  // ... keep the rest of your return() JSX exactly the same ...


  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-8 font-sans">
      <header className="mb-8 border-b border-gray-700 pb-4">
        <h1 className="text-3xl font-bold text-blue-400">AI Medical Imaging Diagnostic Viewer</h1>
        <p className="text-sm text-gray-400 mt-1">For Education Only - Not for Clinical Use</p>
      </header>

      <main className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Image Viewer Section */}
        <div className="lg:col-span-2 bg-gray-800 rounded-lg p-4 shadow-lg border border-gray-700">
          <h2 className="text-xl font-semibold mb-4">Grad-CAM AI Overlay</h2>
          <div className="bg-black rounded border border-gray-600 aspect-square flex items-center justify-center overflow-hidden">
            {/* React will look for this image in the /public/assets/ folder */}
            <img 
              src={activeStudy.heatmapUrl} 
              alt="AI Heatmap" 
              className="max-w-full max-h-full object-contain"
              onError={(e) => { e.target.src = 'https://via.placeholder.com/600x600?text=Awaiting+DICOM+Processing' }}
            />
          </div>
        </div>

        {/* Clinical Data & Actions Section */}
        <div className="flex flex-col gap-6">
          <div className="bg-gray-800 rounded-lg p-6 shadow-lg border border-gray-700">
            <h3 className="text-lg font-semibold text-gray-300 mb-4">Study Details</h3>
            <div className="space-y-3 text-sm">
              <p><span className="text-gray-500">Study ID:</span> {activeStudy.id}</p>
              <p><span className="text-gray-500">Patient ID:</span> {activeStudy.patientId}</p>
              <p><span className="text-gray-500">Model:</span> DenseNet121</p>
            </div>
            
            <div className="mt-6 p-4 bg-gray-900 rounded border border-gray-700">
              <p className="text-gray-400 text-sm mb-1">Disease Detection Confidence</p>
              <p className={`text-3xl font-bold ${activeStudy.confidence > 50 ? 'text-red-400' : 'text-green-400'}`}>
                {activeStudy.confidence.toFixed(2)}%
              </p>
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 shadow-lg border border-gray-700">
            <h3 className="text-lg font-semibold text-gray-300 mb-4">Radiologist Decision</h3>
            <p className="mb-4 text-sm">Current Status: <span className="font-bold text-blue-300">{activeStudy.status}</span></p>
            
            <div className="flex gap-4">
              <button 
                onClick={() => handleDecision("Approved")}
                className="flex-1 bg-green-600 hover:bg-green-500 text-white py-2 px-4 rounded font-medium transition-colors"
              >
                Approve AI
              </button>
              <button 
                onClick={() => handleDecision("Rejected")}
                className="flex-1 bg-red-600 hover:bg-red-500 text-white py-2 px-4 rounded font-medium transition-colors"
              >
                Reject AI
              </button>
            </div>
          </div>
        </div>

      </main>
    </div>
  );
}