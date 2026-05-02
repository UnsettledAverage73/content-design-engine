const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

// For this prototype, we'll use a dummy token to satisfy the backend check
const DUMMY_TOKEN = "Bearer local-dev-token";

export interface Event {
  id: number;
  name: string;
  location: string;
  date: string;
  status: string;
  asset_count: number;
  generation_count: number;
}

export async function fetchEvents(): Promise<Event[]> {
  const response = await fetch(`${API_BASE_URL}/events`, {
    headers: {
      "Authorization": DUMMY_TOKEN
    }
  });
  if (!response.ok) {
    throw new Error("Failed to fetch events");
  }
  return response.json();
}

export async function fetchEventDetails(eventId: number): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/events/${eventId}`, {
    headers: {
      "Authorization": DUMMY_TOKEN
    }
  });
  if (!response.ok) {
    throw new Error("Failed to fetch event details");
  }
  return response.json();
}

export async function processEvent(inputPath: string, brandId?: number): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/process-event`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": DUMMY_TOKEN
    },
    body: JSON.stringify({
      input_path: inputPath,
      brand_id: brandId,
    }),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to process event");
  }
  return response.json();
}
