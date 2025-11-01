import { Request, Response, NextFunction } from 'express';
import { OAuth2Client } from 'google-auth-library';
import { config } from '../config';

const client = new OAuth2Client(config.googleClientId);

export interface AuthenticatedRequest extends Request {
  userEmail?: string;
}

export async function verifyGoogleToken(req: AuthenticatedRequest, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing or invalid authorization header' });
  }

  const token = authHeader.substring(7);

  try {
    const ticket = await client.verifyIdToken({
      idToken: token,
      audience: config.googleClientId,
    });
    
    const payload = ticket.getPayload();
    if (!payload || !payload.email) {
      return res.status(401).json({ error: 'Invalid token payload' });
    }

    req.userEmail = payload.email;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid Google ID token' });
  }
}

export function requireCouncil(req: AuthenticatedRequest, res: Response, next: NextFunction) {
  if (!req.userEmail) {
    return res.status(401).json({ error: 'User not authenticated' });
  }

  if (!config.councilAllowlist.includes(req.userEmail)) {
    return res.status(403).json({ error: 'Council access required' });
  }

  next();
}

export function requireSeedbringer(req: AuthenticatedRequest, res: Response, next: NextFunction) {
  if (!req.userEmail) {
    return res.status(401).json({ error: 'User not authenticated' });
  }

  if (!config.seedbringerAllowlist.includes(req.userEmail)) {
    return res.status(403).json({ error: 'Seedbringer access required' });
  }

  next();
}
