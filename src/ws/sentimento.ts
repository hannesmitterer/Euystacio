import { IncomingMessage, Server as HTTPServer } from 'http';
import { WebSocketServer, WebSocket } from 'ws';
import { SentimentoLiveEvent } from '../types/sentimento';

/**
 * Seed-003 metrics tracker
 */
class Seed003Metrics {
  private samples: Array<{ hope: number; sorrow: number; timestamp: number }> = [];
  private readonly windowMs = 60000; // 1 minute rolling window

  pushSample(sorrow: number, hope: number): void {
    const now = Date.now();
    this.samples.push({ hope, sorrow, timestamp: now });
    
    // Clean old samples outside window
    this.samples = this.samples.filter(s => now - s.timestamp < this.windowMs);
  }

  getSampleCount(): number {
    return this.samples.length;
  }

  getHopeRatio(): number {
    if (this.samples.length === 0) return 0;
    
    const totalHope = this.samples.reduce((sum, s) => sum + s.hope, 0);
    const totalSorrow = this.samples.reduce((sum, s) => sum + s.sorrow, 0);
    const total = totalHope + totalSorrow;
    
    return total > 0 ? totalHope / total : 0;
  }
}

/**
 * SentimentoWSHub manages WebSocket connections for real-time sentimento broadcasts
 * 
 * Features:
 * - Attaches to HTTP server on /api/v2/sentimento/live
 * - Manages connected clients with backpressure handling
 * - Broadcasts SentimentoLiveEvent as JSON
 * - Integrates with Seed-003 metrics via pushSample()
 */
export class SentimentoWSHub {
  private wss: WebSocketServer;
  private clients: Set<WebSocket> = new Set();
  private sequence = 0;
  private seed003 = new Seed003Metrics();
  private bufferMaxKb: number;

  constructor(server: HTTPServer, options?: { broadcastHz?: number; bufferMaxKb?: number }) {
    // Store bufferMaxKb for backpressure handling
    this.bufferMaxKb = options?.bufferMaxKb ?? 512;

    // Create WebSocket server with path filter
    this.wss = new WebSocketServer({ 
      noServer: true,
      perMessageDeflate: false // Disable compression for lower latency
    });

    // Handle HTTP upgrade requests
    server.on('upgrade', (request: IncomingMessage, socket, head) => {
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
      this.clients.add(ws);
      console.log(`[SentimentoWSHub] Client connected. Total: ${this.clients.size}`);

      ws.on('close', () => {
        this.clients.delete(ws);
        console.log(`[SentimentoWSHub] Client disconnected. Total: ${this.clients.size}`);
      });

      ws.on('error', (err) => {
        console.error('[SentimentoWSHub] WebSocket error:', err);
        this.clients.delete(ws);
      });

      // Send initial connection acknowledgment
      this.sendToClient(ws, {
        timestamp: new Date().toISOString(),
        composites: { hope: 0, sorrow: 0 },
        sequence: this.sequence,
        seed003: {
          sampleCount: this.seed003.getSampleCount(),
          hopeRatio: this.seed003.getHopeRatio()
        }
      });
    });
  }

  /**
   * Broadcast a sentimento event to all connected clients
   * Applies backpressure drop: skips clients with full buffers
   */
  broadcast(hope: number, sorrow: number): void {
    // Push to Seed-003 metrics
    this.seed003.pushSample(sorrow, hope);

    this.sequence++;

    const event: SentimentoLiveEvent = {
      timestamp: new Date().toISOString(),
      composites: { hope, sorrow },
      sequence: this.sequence,
      seed003: {
        sampleCount: this.seed003.getSampleCount(),
        hopeRatio: this.seed003.getHopeRatio()
      }
    };

    const payload = JSON.stringify(event);

    // Apply backpressure drop logic
    for (const client of this.clients) {
      if (client.readyState === WebSocket.OPEN) {
        // Check buffered amount
        const bufferedKb = client.bufferedAmount / 1024;
        
        if (bufferedKb < this.bufferMaxKb) {
          try {
            client.send(payload);
          } catch (err) {
            console.error('[SentimentoWSHub] Send error:', err);
            this.clients.delete(client);
          }
        } else {
          // Drop message for this client due to backpressure
          console.warn(`[SentimentoWSHub] Dropping message for client (buffer: ${bufferedKb.toFixed(1)}KB)`);
        }
      }
    }
  }

  /**
   * Send event to a specific client
   */
  private sendToClient(client: WebSocket, event: SentimentoLiveEvent): void {
    if (client.readyState === WebSocket.OPEN) {
      try {
        client.send(JSON.stringify(event));
      } catch (err) {
        console.error('[SentimentoWSHub] Send error:', err);
        this.clients.delete(client);
      }
    }
  }

  /**
   * Get current Seed-003 metrics
   */
  getSeed003Metrics(): { sampleCount: number; hopeRatio: number } {
    return {
      sampleCount: this.seed003.getSampleCount(),
      hopeRatio: this.seed003.getHopeRatio()
    };
  }

  /**
   * Get connected client count
   */
  getClientCount(): number {
    return this.clients.size;
  }

  /**
   * Close all connections and shut down
   */
  close(): void {
    for (const client of this.clients) {
      client.close();
    }
    this.clients.clear();
    this.wss.close();
  }
}
