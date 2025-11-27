# NexaForge Dashboard - React Edition

Modern, enterprise-grade AI monitoring system dashboard built with React and 25+ cutting-edge libraries.

## 🚀 Tech Stack

### Core Framework
- ⚛️ **React 18.3** - UI Library
- ⚡ **Vite 5.4** - Lightning-fast build tool
- 🎨 **Tailwind CSS 3.4** - Utility-first CSS

### State Management & Data Fetching
- 🐻 **Zustand** - Lightweight state management
- 🔄 **TanStack Query (React Query)** - Server state management
- 📡 **Axios** - HTTP client

### Routing & Navigation
- 🧭 **React Router v6** - Client-side routing

### UI Components & Styling
- 🎭 **Framer Motion** - Production-ready animations
- 🎯 **Radix UI** - Accessible component primitives
  - Dropdown Menu
  - Tooltip
  - Dialog
  - Tabs
- 🎨 **clsx + tailwind-merge** - Conditional className utilities

### Data Visualization
- 📊 **Chart.js 4** - Flexible charting library
- 📈 **React ChartJS 2** - React wrapper for Chart.js
- 📉 **Recharts** - Composable charting library

### Utilities & Helpers
- 📅 **date-fns** - Modern date utility library
- 🔧 **react-use** - Essential React hooks collection
- 🎪 **React Icons** - Popular icon packs
- 🍞 **React Hot Toast** - Beautiful notifications
- 🔔 **Sonner** - Opinionated toast component
- 🗃️ **React Virtuoso** - Powerful virtual scrolling
- 🎭 **Vaul** - Drawer component for React

### Developer Experience
- 🛡️ **React Error Boundary** - Error handling
- 📝 **ESLint** - Code linting
- 💎 **React Loading Skeleton** - Loading states
- ⚡ **React Helmet Async** - Document head management

## 📁 Project Structure

```
dashboard-react/
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.jsx       # Top navigation
│   │   │   └── Sidebar.jsx      # Side navigation
│   │   └── dashboard/
│   │       ├── StatsCards.jsx   # Metric cards
│   │       └── MetricsChart.jsx # Real-time charts
│   ├── pages/
│   │   └── Dashboard.jsx        # Main dashboard
│   ├── store/
│   │   ├── themeStore.js        # Theme state
│   │   └── dashboardStore.js    # Dashboard state
│   ├── hooks/                   # Custom React hooks
│   ├── utils/                   # Utility functions
│   ├── services/                # API services
│   ├── App.jsx                  # Main app component
│   ├── main.jsx                 # Entry point
│   └── index.css                # Global styles
├── public/                      # Static assets
├── index.html                   # HTML template
├── vite.config.js              # Vite configuration
├── tailwind.config.js          # Tailwind configuration
├── postcss.config.js           # PostCSS configuration
└── package.json                # Dependencies

```

## 🎯 Features

### ✨ Modern UI/UX
- 🌓 **Dark/Light Mode** - Smooth theme transitions
- 📱 **Fully Responsive** - Mobile, tablet, desktop
- 🎨 **Beautiful Animations** - Framer Motion powered
- 🎭 **Loading States** - Skeleton screens
- 🔔 **Toast Notifications** - User feedback

### 📊 Real-time Monitoring
- 📈 **Live Charts** - Auto-updating metrics
- 💾 **Stats Cards** - Key performance indicators
- 📝 **System Logs** - Real-time log streaming
- ⏱️ **Events Timeline** - Chronological events
- 🌐 **Workflow Graph** - Node visualization

### 🛠️ Developer Features
- 🔥 **Hot Module Replacement** - Instant updates
- 🐛 **Error Boundaries** - Graceful error handling
- 🎯 **Path Aliases** - Clean imports (@components, @pages, etc.)
- 📦 **Code Splitting** - Optimized bundles
- 🚀 **Production Ready** - Optimized builds

## 🚀 Getting Started

### Installation

```bash
cd dashboard-react
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### Build for Production

```bash
npm run build
npm run preview
```

### Lint Code

```bash
npm run lint
```

## 🎨 Color System

### Dark Mode (Default)
```css
Background: #0D0D0D
Panel: #1A1A1A
Accent: #03DAC6 (Cyan)
Success: #0AFF99
```

### Light Mode
```css
Background: #FFFFFF
Panel: #F5F5F5
Accent: #0F8B8D (Teal)
Success: #1C9B5B
```

## 📚 Library Overview

| Category | Libraries | Purpose |
|----------|-----------|---------|
| **Core** | React, React DOM, Vite | Foundation |
| **Routing** | React Router | Navigation |
| **State** | Zustand | Global state |
| **Data** | TanStack Query, Axios | Server state & HTTP |
| **Charts** | Chart.js, Recharts | Visualization |
| **Animation** | Framer Motion | Smooth transitions |
| **UI Components** | Radix UI | Accessible primitives |
| **Styling** | Tailwind CSS | Utility classes |
| **Icons** | React Icons | Icon library |
| **Utilities** | date-fns, react-use | Helpers |
| **Notifications** | React Hot Toast, Sonner | User feedback |
| **Performance** | React Virtuoso | Virtual scrolling |

## 🎯 Path Aliases

```javascript
@ → src/
@components → src/components/
@pages → src/pages/
@hooks → src/hooks/
@utils → src/utils/
@store → src/store/
@services → src/services/
@assets → src/assets/
```

## 🔥 Key Features

- ✅ **25+ Production-Ready Libraries**
- ✅ **Type-Safe** (ESLint configured)
- ✅ **Optimized Bundle** (Code splitting)
- ✅ **Accessible** (Radix UI primitives)
- ✅ **Responsive Design** (Mobile-first)
- ✅ **Theme Persistence** (localStorage)
- ✅ **Real-time Updates** (Auto-refresh)
- ✅ **Error Handling** (Boundaries)
- ✅ **Loading States** (Skeletons)
- ✅ **SEO Ready** (React Helmet)

## 📖 Documentation

For detailed documentation on each library:

- [React](https://react.dev/)
- [Vite](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Zustand](https://zustand-demo.pmnd.rs/)
- [TanStack Query](https://tanstack.com/query/)
- [Framer Motion](https://www.framer.com/motion/)
- [Radix UI](https://www.radix-ui.com/)

## 🤝 Contributing

This is an enterprise monitoring dashboard. Follow best practices and maintain code quality.

## 📄 License

MIT License - NexaForge AI Monitoring System

---

Built with ❤️ using React + 25 Modern Libraries
