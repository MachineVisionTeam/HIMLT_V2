# Chat Assistant

Drop-in React chat component. Uses `/api/models` and `/api/chat` endpoints.

## Integration

**1. Install**
```bash
npm install file:../chat-assistant
# or copy chat-assistant folder and: npm install ./chat-assistant
```

**2. Add CSS** (thinking-dots animation) to your app's global CSS:
```css
.thinking-dots span { display: inline-block; }
.thinking-dots span:nth-child(2) { animation: dotPulse 1.4s ease-in-out infinite; }
.thinking-dots span:nth-child(3) { animation: dotPulse 1.4s ease-in-out 0.2s infinite; }
.thinking-dots span:nth-child(4) { animation: dotPulse 1.4s ease-in-out 0.4s infinite; }
@keyframes dotPulse { 0%, 60%, 100% { opacity: 0.3; } 30% { opacity: 1; } }
```

**3. Use**
```tsx
import { ChatAssistant } from '@tab/chat-assistant';

<ChatAssistant
  apiBase=""           // same-origin default
  context="himlt"      // optional: backend context for app-specific prompts
  title="Chat"
  placeholder="Type..."
/>
```

**Props:** `apiBase`, `context`, `title`, `placeholder`

**Requirements:** React 18+, Tailwind CSS, lucide-react
