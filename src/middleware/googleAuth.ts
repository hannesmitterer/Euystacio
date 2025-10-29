import { Request, Response, NextFunction } from 'express';
import { OAuth2Client } from 'google-auth-library';
import config from '../config';

const client = new OAuth2Client(config.googleClientId);

export enum Role {
  SEEDBRINGER = 'seedbringer',
  COUNCIL = 'council',
}

interface AuthenticatedRequest extends Request {
  user?: {
    email: string;
    role: Role;
    name?: string;
  };
}

/**
 * Verifies Google ID token and attaches user info to request
 */
async function verifyGoogleToken(token: string): Promise<{ email: string; name?: string } | null> {
  try {
    const ticket = await client.verifyIdToken({
      idToken: token,
      audience: config.googleClientId,
    });
    
    const payload = ticket.getPayload();
    if (!payload || !payload.email) {
      return null;
    }

    return {
      email: payload.email,
      name: payload.name,
    };
  } catch (error) {
    console.error('Token verification failed:', error);
    return null;
  }
}

/**
 * Determines user role based on email address
 */
function determineRole(email: string): Role | null {
  // Check if user is Seedbringer (has highest privileges)
  if (config.seedbringerEmails.includes(email)) {
    return Role.SEEDBRINGER;
  }
  
  // Check if user is Council member
  if (config.councilEmails.includes(email)) {
    return Role.COUNCIL;
  }
  
  // User is not authorized
  return null;
}

/**
 * Middleware to authenticate and authorize requests
 * @param allowedRoles - Array of roles allowed to access the endpoint
 */
export function requireAuth(allowedRoles: Role[]) {
  return async (req: AuthenticatedRequest, res: Response, next: NextFunction): Promise<void> => {
    try {
      // Extract token from Authorization header
      const authHeader = req.headers.authorization;
      if (!authHeader || !authHeader.startsWith('Bearer ')) {
        res.status(401).json({ error: 'No authorization token provided' });
        return;
      }

      const token = authHeader.substring(7); // Remove 'Bearer ' prefix

      // Verify Google ID token
      const userInfo = await verifyGoogleToken(token);
      if (!userInfo) {
        res.status(401).json({ error: 'Invalid or expired token' });
        return;
      }

      // Determine user role
      const role = determineRole(userInfo.email);
      if (!role) {
        res.status(403).json({ 
          error: 'Access denied',
          message: 'Your email is not authorized to access this system' 
        });
        return;
      }

      // Check if user's role is allowed for this endpoint
      if (!allowedRoles.includes(role)) {
        res.status(403).json({ 
          error: 'Insufficient permissions',
          message: `This endpoint requires one of the following roles: ${allowedRoles.join(', ')}` 
        });
        return;
      }

      // Attach user info to request
      req.user = {
        email: userInfo.email,
        role: role,
        name: userInfo.name,
      };

      next();
    } catch (error) {
      console.error('Authentication error:', error);
      res.status(500).json({ error: 'Internal server error during authentication' });
    }
  };
}

// Export the AuthenticatedRequest type for use in other modules
export type { AuthenticatedRequest };
