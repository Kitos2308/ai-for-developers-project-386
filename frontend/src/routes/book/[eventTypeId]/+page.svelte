<script lang="ts">
	import Container from '$lib/components/layout/Container.svelte';
	import Card from '$lib/components/ui/Card.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Calendar from '$lib/components/booking/Calendar.svelte';
	import BookingForm from '$lib/components/booking/BookingForm.svelte';
	import { getEventType, getSlots, createBooking } from '$lib/api/public';
	import type { EventType, Slot } from '$lib/types';

	let { eventTypeId } = $props();

	let eventType = $state<EventType | null>(null);
	let selectedDate = $state<string | undefined>();
	let selectedSlot = $state<Slot | undefined>();
	let showBookingForm = $state(false);
	let bookingSuccess = $state(false);
	let loading = $state(true);
	let error = $state<string | null>(null);

	$effect(() => {
		async function loadEventType() {
			try {
				loading = true;
				eventType = await getEventType(eventTypeId);
			} catch (e) {
				error = e instanceof Error ? e.message : 'Не удалось загрузить тип события';
			} finally {
				loading = false;
			}
		}
		loadEventType();
	});

	function handleDateSelect(date: string) {
		selectedDate = date;
		selectedSlot = undefined;
	}

	function handleSlotSelect(slot: Slot) {
		selectedSlot = slot;
	}

	function handleContinue() {
		if (selectedSlot) {
			showBookingForm = true;
		}
	}

	function handleBack() {
		showBookingForm = false;
	}

	async function handleBooking(data: { guestName?: string; guestEmail?: string; notes?: string }) {
		if (!eventType || !selectedSlot) return;
		try {
			await createBooking(eventTypeId, {
				startTime: selectedSlot.startTime,
				...data
			});
			bookingSuccess = true;
		} catch (e) {
			error = e instanceof Error ? e.message : 'Не удалось создать бронирование';
		}
	}
</script>

<Container>
	<div class="py-8">
		{#if loading}
			<div class="flex justify-center py-12">
				<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
			</div>
		{:else if error}
			<div class="text-center py-12 text-red-500">{error}</div>
		{:else if bookingSuccess}
			<Card padding="p-8 max-w-lg mx-auto text-center">
				<div class="w-16 h-16 rounded-full bg-green-100 dark:bg-green-900 flex items-center justify-center mx-auto mb-4">
					<svg class="w-8 h-8 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
					</svg>
				</div>
				<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">Бронирование подтверждено!</h2>
				<p class="text-gray-500 dark:text-gray-400 mb-6">
					Ваша встреча забронирована на {selectedSlot ? new Date(selectedSlot.startTime).toLocaleString('ru-RU') : ''}
				</p>
			<a href="/book">
				<Button variant="primary">Записаться ещё</Button>
			</a>
			</Card>
		{:else if showBookingForm && selectedSlot}
			<BookingForm slot={selectedSlot} onBack={handleBack} onSubmit={handleBooking} />
		{:else if eventType}
			<h1 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-gray-100 mb-8">
				{eventType.title}
			</h1>
			<Calendar
				eventTypeId={eventTypeId}
				durationMinutes={eventType.durationMinutes}
				onDateSelect={handleDateSelect}
				onSlotSelect={handleSlotSelect}
				selectedDate={selectedDate}
				selectedSlot={selectedSlot}
			/>
			<div class="flex justify-end mt-6">
				<Button variant="primary" disabled={!selectedSlot} onclick={handleContinue}>
					Продолжить
				</Button>
			</div>
		{/if}
	</div>
</Container>
