export async function retry(job: Job, error: Error) {
  if (!isTransient(error) || job.attempts >= 3) return markFailed(job.id, error);
  return enqueue(job, { attempts: job.attempts + 1, delayMs: 100 * 2 ** job.attempts });
}
