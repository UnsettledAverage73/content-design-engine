const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export interface Event {
  id: number;
  name: string;
  location: string;
  date: string;
  asset_count: number;
  generation_count: number;
}

export async function fetchEvents(): Promise<Event[]> {
  const response = await fetch(`${API_BASE_URL}/events`);
  if (!response.ok) {
    throw new Error("Failed to fetch events");
  }
  return response.json();
}

export async function processEvent(inputPath: string, brandId?: number): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/process-event`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
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
