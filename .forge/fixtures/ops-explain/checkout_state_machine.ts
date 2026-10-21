type State = 'pending' | 'paid' | 'reserved' | 'confirmed' | 'cancelled';

export async function confirm(order: Order) {
  if (order.state !== 'pending') throw new Error('invalid state');
  await payments.capture(order.paymentId);
  order.state = 'paid';
  await inventory.reserve(order.items);
  order.state = 'reserved';
  await orders.confirm(order.id);
  order.state = 'confirmed';
}
