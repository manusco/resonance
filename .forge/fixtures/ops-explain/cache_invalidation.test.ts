it('returns the updated profile on the next read', async () => {
  await updateProfile(user.id, { name: 'New name' });
  expect(await getProfile(user.id)).toMatchObject({ name: 'New name' });
});
