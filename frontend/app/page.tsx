"use client";

import { useEffect, useState } from "react";
import { fetchEvents, processEvent, Event } from "@/lib/api";
import { LayoutDashboard, Users, FileText, Settings, Plus, MapPin, Calendar, Image as ImageIcon, X, Loader2 } from "lucide-react";

export default function Dashboard() {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [inputPath, setInputPath] = useState("input/");

  const loadEvents = () => {
    setLoading(true);
    fetchEvents()
      .then(setEvents)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadEvents();
  }, []);

  const handleProcess = async (e: React.FormEvent) => {
    e.preventDefault();
    setProcessing(true);
    try {
      await processEvent(inputPath);
      setShowModal(false);
      loadEvents();
    } catch (error) {
      alert(error instanceof Error ? error.message : "Processing failed");
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200 shadow-sm">
        <div className="p-6">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <ImageIcon className="text-white w-5 h-5" />
            </div>
            <h1 className="text-xl font-bold text-gray-900 tracking-tight">Intelligence</h1>
          </div>
        </div>
        <nav className="mt-6">
          <a href="#" className="flex items-center px-6 py-3 text-blue-600 bg-blue-50 border-r-4 border-blue-600 font-medium">
            <LayoutDashboard className="w-5 h-5 mr-3" />
            Dashboard
          </a>
          <a href="#" className="flex items-center px-6 py-3 text-gray-500 hover:bg-gray-50 hover:text-blue-600 transition-all">
            <Users className="w-5 h-5 mr-3" />
            Brands
          </a>
          <a href="#" className="flex items-center px-6 py-3 text-gray-500 hover:bg-gray-50 hover:text-blue-600 transition-all">
            <FileText className="w-5 h-5 mr-3" />
            Reports
          </a>
          <a href="#" className="flex items-center px-6 py-3 text-gray-500 hover:bg-gray-50 hover:text-blue-600 transition-all">
            <Settings className="w-5 h-5 mr-3" />
            Settings
          </a>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <header className="flex items-center justify-between px-8 py-6 bg-white border-b border-gray-200">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Event Dashboard</h2>
            <p className="text-sm text-gray-500 mt-1">Manage and automate your marketing assets.</p>
          </div>
          <button 
            onClick={() => setShowModal(true)}
            className="flex items-center px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 active:scale-95 transition-all shadow-md font-medium"
          >
            <Plus className="w-5 h-5 mr-2" />
            Process New Event
          </button>
        </header>

        <div className="p-8">
          {loading ? (
            <div className="flex flex-col items-center justify-center h-64 space-y-4">
              <Loader2 className="w-10 h-10 text-blue-600 animate-spin" />
              <p className="text-gray-500 font-medium text-sm">Syncing events...</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {events.length === 0 ? (
                <div className="col-span-full p-20 text-center bg-white rounded-2xl border-2 border-dashed border-gray-200">
                  <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4">
                    <ImageIcon className="text-gray-400 w-8 h-8" />
                  </div>
                  <h3 className="text-lg font-bold text-gray-900">No events found</h3>
                  <p className="text-gray-500 max-w-xs mx-auto mt-2">Start by processing your first folder of event media.</p>
                  <button 
                    onClick={() => setShowModal(true)}
                    className="mt-6 text-blue-600 font-semibold hover:underline"
                  >
                    Process an event now →
                  </button>
                </div>
              ) : (
                events.map((event) => (
                  <div key={event.id} className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-xl transition-all group cursor-pointer">
                    <div className="p-6">
                      <div className="flex justify-between items-start">
                        <h3 className="text-lg font-bold text-gray-900 group-hover:text-blue-600 transition-colors">{event.name}</h3>
                        <span className={`text-[10px] px-2 py-1 rounded-full font-bold uppercase tracking-wider ${
                          event.status === 'completed' ? 'bg-green-50 text-green-700' : 
                          event.status === 'processing' ? 'bg-blue-50 text-blue-700 animate-pulse' : 
                          'bg-red-50 text-red-700'
                        }`}>
                          {event.status}
                        </span>
                      </div>
                      <div className="mt-4 space-y-2">
                        <div className="flex items-center text-sm text-gray-600">
                          <MapPin className="w-4 h-4 mr-2 text-gray-400" />
                          {event.location}
                        </div>
                        <div className="flex items-center text-sm text-gray-600">
                          <Calendar className="w-4 h-4 mr-2 text-gray-400" />
                          {new Date(event.date).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}
                        </div>
                      </div>
                      <div className="mt-8 grid grid-cols-2 gap-4 pt-6 border-t border-gray-50">
                        <div>
                          <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest">Media Assets</p>
                          <p className="text-xl font-bold text-blue-600">{event.asset_count}</p>
                        </div>
                        <div>
                          <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest">Generated</p>
                          <p className="text-xl font-bold text-gray-900">{event.generation_count}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      </main>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-white w-full max-w-md rounded-2xl shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200">
            <div className="p-6 border-b border-gray-100 flex justify-between items-center">
              <h3 className="text-xl font-bold text-gray-900">Process New Event</h3>
              <button 
                onClick={() => !processing && setShowModal(false)}
                className="text-gray-400 hover:text-gray-600 p-1"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            <form onSubmit={handleProcess} className="p-6 space-y-6">
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2 uppercase tracking-wide">Media Input Path</label>
                <input 
                  type="text" 
                  value={inputPath}
                  onChange={(e) => setInputPath(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                  placeholder="e.g., input/"
                  required
                />
                <p className="text-xs text-gray-400 mt-2">Relative path to the folder containing JPG/MP4 files.</p>
              </div>
              <div className="pt-4">
                <button 
                  type="submit" 
                  disabled={processing}
                  className="w-full flex items-center justify-center px-6 py-4 text-white bg-blue-600 rounded-xl font-bold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg shadow-blue-200"
                >
                  {processing ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-3 animate-spin" />
                      Analyzing Media...
                    </>
                  ) : (
                    "Launch Engine"
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
