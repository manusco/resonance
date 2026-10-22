export async function refreshSession(token: string) {
  const claims = verifyRefreshToken(token);
  await refreshTokenStore.consume(claims.jti);
  return issueTokenPair(claims.userId);
}
