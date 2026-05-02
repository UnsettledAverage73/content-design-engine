"use client";

import { useEffect, useState } from "react";
import { fetchEvents, Event } from "@/lib/api";
import { LayoutDashboard, Users, FileText, Settings, Plus, MapPin, Calendar, Image as ImageIcon } from "lucide-react";

export default function Dashboard() {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEvents()
      .then(setEvents)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200">
        <div className="p-6">
          <h1 className="text-xl font-bold text-blue-600">Content Engine</h1>
        </div>
        <nav className="mt-6">
          <a href="#" className="flex items-center px-6 py-3 text-blue-600 bg-blue-50 border-r-4 border-blue-600">
            <LayoutDashboard className="w-5 h-5 mr-3" />
            Dashboard
          </a>
          <a href="#" className="flex items-center px-6 py-3 text-gray-600 hover:bg-gray-50 hover:text-blue-600 transition-colors">
            <Users className="w-5 h-5 mr-3" />
            Brands
          </a>
          <a href="#" className="flex items-center px-6 py-3 text-gray-600 hover:bg-gray-50 hover:text-blue-600 transition-colors">
            <FileText className="w-5 h-5 mr-3" />
            Reports
          </a>
          <a href="#" className="flex items-center px-6 py-3 text-gray-600 hover:bg-gray-50 hover:text-blue-600 transition-colors">
            <Settings className="w-5 h-5 mr-3" />
            Settings
          </a>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <header className="flex items-center justify-between px-8 py-6 bg-white border-b border-gray-200">
          <h2 className="text-2xl font-semibold text-gray-800">Events</h2>
          <button className="flex items-center px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors">
            <Plus className="w-5 h-5 mr-2" />
            Process New Event
          </button>
        </header>

        <div className="p-8">
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {events.length === 0 ? (
                <div className="col-span-full p-12 text-center bg-white rounded-xl border-2 border-dashed border-gray-200">
                  <p className="text-gray-500">No events processed yet.</p>
                </div>
              ) : (
                events.map((event) => (
                  <div key={event.id} className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
                    <div className="p-6">
                      <h3 className="text-lg font-bold text-gray-900">{event.name}</h3>
                      <div className="mt-4 space-y-2">
                        <div className="flex items-center text-sm text-gray-500">
                          <MapPin className="w-4 h-4 mr-2" />
                          {event.location}
                        </div>
                        <div className="flex items-center text-sm text-gray-500">
                          <Calendar className="w-4 h-4 mr-2" />
                          {new Date(event.date).toLocaleDateString()}
                        </div>
                      </div>
                      <div className="mt-6 flex items-center justify-between pt-4 border-t border-gray-100">
                        <div className="flex items-center text-sm font-medium text-blue-600">
                          <ImageIcon className="w-4 h-4 mr-1" />
                          {event.asset_count} Assets
                        </div>
                        <div className="text-sm font-medium text-green-600">
                          {event.generation_count} Generated
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
    </div>
  );
}
