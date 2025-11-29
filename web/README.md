# Deklutter Web App

Beautiful React web app for Deklutter - AI-powered Gmail cleaner.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🛠️ Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Routing
- **Lucide React** - Icons
- **Recharts** - Charts (for future analytics)

## 📁 Project Structure

```
web/
├── src/
│   ├── pages/
│   │   ├── LandingPage.jsx    # Home page with hero & features
│   │   ├── Dashboard.jsx       # Scan & clean interface
│   │   └── Callback.jsx        # OAuth callback handler
│   ├── App.jsx                 # Main app with routing
│   ├── main.jsx                # Entry point
│   └── index.css               # Global styles
├── index.html                  # HTML template
├── vite.config.js              # Vite configuration
├── tailwind.config.js          # Tailwind configuration
└── package.json                # Dependencies
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
VITE_API_URL=https://api.deklutter.co
```

### API Proxy

The Vite dev server proxies `/api/*` requests to the production API:

```javascript
proxy: {
  '/api': {
    target: 'https://api.deklutter.co',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, '')
  }
}
```

## 📦 Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod
```

### Build Output

```bash
npm run build
# Output: dist/
```

## 🎨 Features

- ✅ Beautiful landing page with gradient hero
- ✅ OAuth integration with Gmail
- ✅ Dashboard for scanning inbox
- ✅ Visual email categorization (Delete/Review/Keep)
- ✅ Sample email previews
- ✅ One-click cleanup
- ✅ Responsive design
- ✅ Modern UI with Tailwind CSS

## 🔐 Security

- JWT tokens stored in localStorage
- All API calls use Bearer authentication
- HTTPS only in production
- No sensitive data stored client-side

## 📝 License

MIT
