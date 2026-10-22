it('marks a job failed on the third failed attempt', async () => {
  await retry(job, { attempts: 2 }, error);
  expect(queue.enqueue).not.toHaveBeenCalled();
  expect(store.markFailed).toHaveBeenCalledWith(job.id, error);
});
