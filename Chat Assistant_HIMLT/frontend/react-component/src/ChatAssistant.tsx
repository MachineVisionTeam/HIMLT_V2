/**
 * ChatAssistant - popup in right corner, expandable.
 * Drop-in component for React apps. Uses same-origin /api by default.
 */

import { useState, useEffect, useRef } from 'react';
import { MessageCircle, X, Maximize2, Minimize2 } from 'lucide-react';

export interface ChatAssistantProps {
  /** API base URL (default: '' for same-origin) */
  apiBase?: string;
  /** Context sent to backend (e.g. 'himlt' for app-specific prompts) */
  context?: string;
  /** Placeholder text when empty */
  placeholder?: string;
  /** Title in header */
  title?: string;
  /** Greeting when chat opens (e.g. "How can I help you today?") */
  greeting?: string;
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  fallback?: boolean;
}

function escapeHtml(s: string): string {
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}

function renderMarkdown(s: string): string {
  if (!s) return '';
  let t = escapeHtml(s);
  t = t.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  t = t.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  t = t.replace(/^# (.+)$/gm, '<h1>$1</h1>');
  t = t.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  t = t.replace(/\*(.+?)\*/g, '<em>$1</em>');
  t = t.replace(/`([^`]+)`/g, '<code>$1</code>');
  t = t.replace(/^[-*]\s+/gm, '• ');
  t = t.replace(/\n/g, '<br>');
  return t;
}

export default function ChatAssistant({
  apiBase = '',
  context = '',
  placeholder = 'Type a message...',
  title = 'Chat Assistant',
  greeting = 'How can I help you today?',
}: ChatAssistantProps = {}) {
  const [open, setOpen] = useState(false);
  const [expanded, setExpanded] = useState(false);
  const [models, setModels] = useState<{ id: string; name: string }[]>([]);
  const [modelId, setModelId] = useState('auto');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<'ok' | 'error'>('ok');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (!open) return;
    let cancelled = false;
    (async () => {
      try {
        const r = await fetch(`${apiBase}/api/models`);
        const data = await r.json();
        if (cancelled) return;
        if (r.ok && data.models) {
          setModels(data.models.map((m: { id: string; name: string }) => ({ id: m.id, name: m.name })));
          setStatus('ok');
        } else {
          setStatus('error');
        }
      } catch {
        if (!cancelled) setStatus('error');
      }
    })();
    return () => { cancelled = true; };
  }, [open, apiBase]);

  const send = async () => {
    const text = input.trim();
    if (!text || loading) return;
    setInput('');
    setLoading(true);
    const userMsg: ChatMessage = { role: 'user', content: text };
    const msgs = [...messages, userMsg];
    setMessages(msgs);
    setMessages((m) => [...m, { role: 'assistant', content: '', fallback: false }]);

    try {
      const r = await fetch(`${apiBase}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model_id: modelId,
          messages: msgs.map(({ role, content }) => ({ role, content })),
          context: context || undefined,
        }),
      });

      const data = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(data.error || 'Request failed');

      const content = data.response || '';
      const usedFallback = data.fallback || false;
      setMessages((m) => {
        const next = [...m];
        const last = next[next.length - 1];
        if (last.role === 'assistant') {
          next[next.length - 1] = { ...last, content, fallback: usedFallback };
        }
        return next;
      });
    } catch (e) {
      setMessages((m) => {
        const next = [...m];
        const last = next[next.length - 1];
        if (last.role === 'assistant' && !last.content) {
          next[next.length - 1] = { ...last, content: 'Error: ' + (e as Error).message };
        }
        return next;
      });
    } finally {
      setLoading(false);
    }
  };

  const containerClass = expanded
    ? 'fixed inset-4 z-[9999] rounded-xl shadow-2xl'
    : 'fixed bottom-6 right-6 z-[9999] w-[380px] max-w-[calc(100vw-3rem)] rounded-xl shadow-2xl';

  return (
    <>
      {!open && (
        <button
          onClick={() => setOpen(true)}
          className="fixed bottom-6 right-6 z-[9998] flex h-14 w-14 items-center justify-center rounded-full bg-indigo-600 text-white shadow-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          aria-label="Open chat"
        >
          <MessageCircle size={24} />
        </button>
      )}

      {open && (
        <div
          className={`${containerClass} flex flex-col bg-white border border-gray-200`}
          style={expanded ? { maxHeight: 'calc(100vh - 2rem)' } : { maxHeight: 'min(560px, 80vh)' }}
        >
          <div className="flex items-center justify-between border-b border-gray-200 bg-gray-50 px-4 py-2 rounded-t-xl">
            <h3 className="font-semibold text-gray-800">{title}</h3>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setExpanded((e) => !e)}
                className="rounded p-1.5 text-gray-500 hover:bg-gray-200 hover:text-gray-700"
                aria-label={expanded ? 'Collapse' : 'Expand'}
              >
                {expanded ? <Minimize2 size={18} /> : <Maximize2 size={18} />}
              </button>
              <button
                onClick={() => setOpen(false)}
                className="rounded p-1.5 text-gray-500 hover:bg-gray-200 hover:text-gray-700"
                aria-label="Close"
              >
                <X size={18} />
              </button>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2 border-b border-gray-100 px-4 py-2 bg-gray-50/50">
            <select
              value={modelId}
              onChange={(e) => setModelId(e.target.value)}
              className="rounded border border-gray-300 px-2 py-1.5 text-sm"
            >
              {models.map((m) => (
                <option key={m.id} value={m.id}>{m.name}</option>
              ))}
            </select>
            {status === 'error' && (
              <span className="text-xs text-red-600">Offline</span>
            )}
          </div>

          <div
            className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50/30"
            style={{ minHeight: expanded ? 400 : 200 }}
          >
            {messages.length === 0 && (
              <div className="text-sm text-gray-600 space-y-2">
                <p className="font-medium">{greeting}</p>
                <p className="text-xs text-gray-400">Ask about the app workflow, outputs, or how to use it.</p>
                <p className="text-xs text-gray-400">Try: &quot;What are the steps?&quot; or &quot;What do the colors mean?&quot;</p>
              </div>
            )}
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[85%] rounded-lg px-3 py-2 text-sm ${
                    msg.role === 'user'
                      ? 'bg-indigo-100 text-indigo-900'
                      : 'bg-white border border-gray-200 text-gray-800'
                  }`}
                >
                  <div
                    className="whitespace-pre-wrap break-words chat-assistant-message"
                    dangerouslySetInnerHTML={{
                      __html: msg.role === 'user'
                        ? escapeHtml(msg.content)
                        : msg.content
                          ? renderMarkdown(msg.content)
                          : '<span class="thinking-dots">Thinking<span>.</span><span>.</span><span>.</span></span>',
                    }}
                  />
                  {msg.role === 'assistant' && msg.fallback && (
                    <p className="mt-1 text-xs text-amber-600">[Auto fallback]</p>
                  )}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <div className="border-t border-gray-200 p-3 bg-white rounded-b-xl">
            {loading && (
              <p className="text-xs text-gray-500 mb-2 flex items-center gap-1">
                <span className="thinking-dots">Thinking<span>.</span><span>.</span><span>.</span></span>
              </p>
            )}
            <div className="flex gap-2">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    send();
                  }
                }}
                placeholder={placeholder}
                rows={1}
                className="flex-1 rounded border border-gray-300 px-3 py-2 text-sm resize-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
                disabled={loading}
              />
              <button
                onClick={send}
                disabled={!input.trim() || loading}
                className="rounded bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? '…' : 'Send'}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
