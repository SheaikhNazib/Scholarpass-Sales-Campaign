# ScholarPass - Sales Campaign Management

A Next.js web application for managing sales campaigns and opportunity pipelines.

## Features

- 🎯 My Opportunity Pipeline List - Manage your assigned opportunities
- 📊 Opportunity Pipeline List - View all opportunities in the system
- 📋 My Campaign List - Manage your assigned campaigns
- 🚀 Campaign List - View all campaigns in the system

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Axios

## Getting Started

### Prerequisites

- Node.js 18.x or higher
- npm or yarn

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env.local` file with your environment variables:
```env
API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Running the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

### Building for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── src/
│   ├── app/                      # Next.js App Router pages
│   │   ├── campaigns/            # All campaigns page
│   │   ├── my-campaigns/         # My campaigns page
│   │   ├── opportunity-pipelines/# All opportunity pipelines page
│   │   ├── my-opportunity-pipelines/ # My opportunity pipelines page
│   │   ├── layout.tsx            # Root layout
│   │   ├── page.tsx              # Home page
│   │   └── globals.css           # Global styles
│   └── components/
│       └── layout/
│           └── Sidebar.tsx       # Navigation sidebar
├── public/                       # Static files
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
└── README.md
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## API Integration

The application is configured to connect to the backend API at `http://localhost:8000`. Update the `API_BASE_URL` in `.env.local` to point to your backend server.

## License

Private - ScholarPass 2026
