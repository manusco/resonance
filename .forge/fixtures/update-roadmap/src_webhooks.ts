export async function handlePaymentEvent(event: PaymentEvent) {
  if (await eventStore.exists(event.id)) return { duplicate: true };
  await eventStore.record(event.id);
  await applyPayment(event);
  return { duplicate: false };
}
