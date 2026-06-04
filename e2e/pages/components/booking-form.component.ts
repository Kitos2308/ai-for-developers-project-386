import { Page, Locator } from '@playwright/test';

export class BookingFormComponent {
  readonly page: Page;
  readonly guestNameInput: Locator;
  readonly guestEmailInput: Locator;
  readonly notesTextarea: Locator;
  readonly submitButton: Locator;
  readonly backButton: Locator;
  readonly selectedTimeLabel: Locator;

  constructor(page: Page) {
    this.page = page;
    this.guestNameInput = page.locator('input').filter({ has: page.locator('~ Имя') }).first();
    this.guestEmailInput = page.locator('input[type="email"]').first();
    this.notesTextarea = page.getByPlaceholder(/Дополнительная информация/i);
    this.submitButton = page.getByRole('button', { name: /Забронировать/i });
    this.backButton = page.getByRole('button', { name: /Назад/i }).first();
    this.selectedTimeLabel = page.getByText(/Выбранное время/i);
  }

  async fillForm(data: { guestName?: string; guestEmail?: string; notes?: string }) {
    const nameInput = this.page.locator('input').first();
    if (data.guestName) await nameInput.fill(data.guestName);

    const emailInputs = this.page.locator('input[type="email"]');
    if (data.guestEmail && (await emailInputs.count()) > 0) {
      await emailInputs.first().fill(data.guestEmail);
    }

    if (data.notes) await this.notesTextarea.fill(data.notes);
  }

  async submit() {
    await this.submitButton.click();
  }

  async goBack() {
    await this.backButton.click();
  }
}