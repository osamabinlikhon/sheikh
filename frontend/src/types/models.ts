export interface User {
  id: string;
  username: string;
  email: string;
}

export interface Message {
  id: string;
  role: 'user' | 'agent';
  content: string;
  timestamp: string;
}

export interface Session {
  id: string;
  name: string;
  messages: Message[];
}

export interface ToolOutput {
  toolName: string;
  output: any;
}
