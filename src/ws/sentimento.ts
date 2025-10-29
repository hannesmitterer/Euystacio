/**
 * SentimentoWSHub: WebSocket hub for broadcasting SentimentoLiveEvent
 * Manages client connections, handles backpressure, and feeds Seed-003 metrics
 */

import * as http from 'http';
import * as WebSocket from 'ws';
import { SentimentoLiveEvent } from '../types/sentimento';
import { seed003Metrics } from '../metrics/seed003';
import { Config } from '../config';

export class SentimentoWSHub {
  private wss: WebSocket.Server;
  private clients: Set<WebSocket> = new Set();
  private config: Config;
  private sequenceNumber = 0;

  constructor(server: http.Server, config: Config) {
    this.config = config;
    this.wss = new WebSocket.Server({ noServer: true });

    // Handle upgrade requests for WebSocket
    server.on('upgrade', (request, socket, head) => {
      const pathname = request.url || '';
      
      if (pathname === '/api/v2/sentimento/live') {
        this.wss.handleUpgrade(request, socket, head, (ws) => {
          this.wss.emit('connection', ws, request);
        });
      } else {
        socket.destroy();
      }
    });

    // Handle new WebSocket connections
    this.wss.on('connection', (ws: WebSocket) => {
      console.log('New WebSocket client connected');
      this.clients.add(ws);

      // Send welcome message
      const welcomeEvent: SentimentoLiveEvent = {
        timestamp: new Date().toISOString(),
        composites: { hope: 0, sorrow: 0 },
        source: 'welcome',
      };
      this.sendToClient(ws, welcomeEvent);

      // Handle client disconnect
      ws.on('close', () => {
        console.log('WebSocket client disconnected');
        this.clients.delete(ws);
      });

      // Handle errors
      ws.on('error', (error) => {
        console.error('WebSocket client error:', error);
        this.clients.delete(ws);
      });
    });
  }

  /**
   * Broadcast an event to all connected clients
   * Applies backpressure control and feeds Seed-003 metrics
   */
  broadcast(event: SentimentoLiveEvent): void {
    // Add sequence number
    const eventWithSequence: SentimentoLiveEvent = {
      ...event,
      sequence: ++this.sequenceNumber,
      timestamp: event.timestamp || new Date().toISOString(),
    };

    // Feed to Seed-003 metrics
    seed003Metrics.pushSample(
      eventWithSequence.composites.sorrow,
      eventWithSequence.composites.hope
    );

    // Broadcast to all clients
    const payload = JSON.stringify(eventWithSequence);
    const bufferMaxBytes = this.config.sentimentoBufferMaxKb * 1024;

    this.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        this.sendToClient(client, eventWithSequence, bufferMaxBytes);
      }
    });

    console.log(`Broadcast event ${this.sequenceNumber} to ${this.clients.size} clients`);
  }

  /**
   * Send event to a single client with backpressure control
   */
  private sendToClient(
    client: WebSocket,
    event: SentimentoLiveEvent,
    maxBuffer?: number
  ): void {
    try {
      // Check backpressure if limit specified
      if (maxBuffer && client.bufferedAmount > maxBuffer) {
        console.warn('Client buffer exceeded, dropping send');
        return;
      }

      const payload = JSON.stringify(event);
      client.send(payload);
    } catch (error) {
      console.error('Error sending to client:', error);
      this.clients.delete(client);
    }
  }

  /**
   * Get current client count
   */
  getClientCount(): number {
    return this.clients.size;
  }

  /**
   * Close all connections and shut down
   */
  shutdown(): void {
    this.clients.forEach((client) => {
      client.close();
    });
    this.wss.close();
  }
}
