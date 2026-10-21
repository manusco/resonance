export async function charge(order: Order) {
  const key = `order:${order.id}`;
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      return await payments.charge(order, { idempotencyKey: key });
    } catch (error) {
      if (!isTransient(error) || attempt === 2) throw error;
      await sleep(100 * 2 ** attempt);
    }
  }
}
