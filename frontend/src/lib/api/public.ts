import type { EventType, Slot, CalendarDaySlots, Booking, CreateBookingRequest } from '$lib/types';

const API_URL = import.meta.env.VITE_API_URL || '';

async function fetchApi<T>(url: string, options?: RequestInit): Promise<T> {
	const fullUrl = API_URL ? `${API_URL}${url}` : url;
	const response = await fetch(fullUrl, {
		headers: { 'Content-Type': 'application/json' },
		...options
	});
	if (!response.ok) {
		throw new Error(`API error: ${response.status} ${response.statusText}`);
	}
	if (response.status === 204) return undefined as T;
	return response.json();
}

export async function getEventTypes(): Promise<EventType[]> {
	return fetchApi<EventType[]>('/public/event-types');
}

export async function getEventType(id: string): Promise<EventType> {
	return fetchApi<EventType>(`/public/event-types/${id}`);
}

export async function getSlots(eventTypeId: string, date?: string): Promise<Slot[]> {
	const params = date ? `?date=${date}` : '';
	return fetchApi<Slot[]>(`/public/event-types/${eventTypeId}/slots${params}`);
}

export async function getCalendar(eventTypeId: string, month: number, year: number): Promise<CalendarDaySlots[]> {
	return fetchApi<CalendarDaySlots[]>(`/public/event-types/${eventTypeId}/calendar?month=${month}&year=${year}`);
}

export async function createBooking(eventTypeId: string, body: CreateBookingRequest): Promise<Booking> {
	return fetchApi<Booking>(`/public/event-types/${eventTypeId}/bookings`, {
		method: 'POST',
		body: JSON.stringify(body)
	});
}
