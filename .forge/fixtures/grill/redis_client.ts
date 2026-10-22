// Supplied excerpt: the Redis client boundary available to middleware.
export interface RedisClient {
  eval(script: string, numberOfKeys: number, ...keysAndArgs: string[]): Promise<unknown>;
}

export declare const redis: RedisClient;
