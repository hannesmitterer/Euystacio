import dotenv from 'dotenv';

dotenv.config();

export const config = {
  googleClientId: process.env.GOOGLE_CLIENT_ID || '',
  councilAllowlist: (process.env.COUNCIL_ALLOWLIST || '').split(',').map(e => e.trim()).filter(e => e),
  seedbringerAllowlist: (process.env.SEEDBRINGER_ALLOWLIST || '').split(',').map(e => e.trim()).filter(e => e),
  port: parseInt(process.env.PORT || '3000', 10),
};

export function validateConfig() {
  if (!config.googleClientId) {
    throw new Error('GOOGLE_CLIENT_ID is required');
  }
  if (config.councilAllowlist.length === 0) {
    console.warn('Warning: COUNCIL_ALLOWLIST is empty');
  }
  if (config.seedbringerAllowlist.length === 0) {
    console.warn('Warning: SEEDBRINGER_ALLOWLIST is empty');
  }
}
