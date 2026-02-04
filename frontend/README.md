# Agent Sheikh - Frontend

This is the frontend for Agent Sheikh, a modern web application for interacting with an AI agent. It is built using Vue 3 and the Ant Design X component library.

## Features

- **Modern AI Chat Interface**: Powered by Ant Design X for superior AI interaction.
- **Real-time Tool Viewing**: Integrated VNC viewer (noVNC) and Terminal emulator (xterm.js).
- **Streaming Responses**: Real-time message streaming from the agent.
- **File Management**: Interface for managing files within the agent's sandbox.
- **Rich Markdown Support**: Support for complex markdown rendering including code blocks and math.

## Tech Stack

- **Framework**: Vue 3 (Composition API)
- **State Management**: Pinia
- **UI Components**: Ant Design Vue & Ant Design X
- **Terminal**: xterm.js
- **VNC Viewer**: noVNC
- **Build Tool**: Vite
- **Language**: TypeScript

## Project Structure

```
frontend/
├── src/
│   ├── components/     # UI components (chat, tools, layout)
│   ├── stores/         # Pinia state stores
│   ├── services/       # API and WebSocket clients
│   ├── assets/         # Static assets
│   ├── types/          # TypeScript type definitions
│   ├── App.vue         # Root component
│   └── main.ts         # Application entry point
├── public/             # Public assets
├── Dockerfile          # Container definition
├── package.json        # Dependencies and scripts
├── tsconfig.json       # TypeScript configuration
└── vite.config.ts      # Vite configuration
```

## Setup & Installation

### Prerequisites

- Node.js 18+
- npm

### Local Development

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment variables**:
   Create a `.env` file (you can use `.env.example` as a template if it exists):
   ```bash
   VITE_API_BASE_URL=http://localhost:8000
   ```

4. **Start the development server**:
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:5173`.

## Building for Production

To build the application for production:

```bash
npm run build
```

The output will be in the `dist/` directory.

## Testing

Run unit tests with `vitest`:

```bash
npm run test
```

## Linting and Formatting

```bash
# Run linting
npm run lint

# Format code
npm run format
```
