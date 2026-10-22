export async function runOne(job: Job, handler: Handler, store: JobStore) {
  try {
    await handler(job.payload);
    await store.ack(job.id);
  } catch (error) {
    await store.release(job.id, { attempts: job.attempts + 1 });
    throw error;
  }
}
