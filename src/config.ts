import dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();

interface Config {
  port: number;
  nodeEnv: string;
  googleClientId: string;
  seedbringerEmails: string[];
  councilEmails: string[];
  requiredScopesSeedbringer: string[];
  requiredScopesCouncil: string[];
}

function parseEmailList(emailString: string | undefined): string[] {
  if (!emailString) return [];
  return emailString.split(',').map(email => email.trim()).filter(email => email.length > 0);
}

function parseScopeList(scopeString: string | undefined): string[] {
  if (!scopeString) return [];
  return scopeString.split(' ').map(scope => scope.trim()).filter(scope => scope.length > 0);
}

const config: Config = {
  port: parseInt(process.env.PORT || '3000', 10),
  nodeEnv: process.env.NODE_ENV || 'development',
  googleClientId: process.env.GOOGLE_CLIENT_ID || '',
  seedbringerEmails: parseEmailList(process.env.SEEDBRINGER_EMAILS),
  councilEmails: parseEmailList(process.env.COUNCIL_EMAILS),
  requiredScopesSeedbringer: parseScopeList(process.env.REQUIRED_SCOPES_SEEDBRINGER),
  requiredScopesCouncil: parseScopeList(process.env.REQUIRED_SCOPES_COUNCIL),
};

// Validate required configuration
if (!config.googleClientId) {
  console.warn('Warning: GOOGLE_CLIENT_ID is not set. Authentication will not work.');
}

if (config.seedbringerEmails.length === 0) {
  console.warn('Warning: No Seedbringer emails configured.');
}

if (config.councilEmails.length === 0) {
  console.warn('Warning: No Council emails configured.');
}

export default config;
