// Supplied excerpt: middleware is composed through Express RequestHandler.
import { randomUUID } from "node:crypto";
import type { RequestHandler } from "express";

export const requestContextMiddleware: RequestHandler = (_req, res, next) => {
  res.locals.requestId = randomUUID();
  next();
};
