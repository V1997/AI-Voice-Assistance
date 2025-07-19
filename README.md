# AI Voice Assistance - E-commerce Chatbot

A responsive chatbot component built with Next.js, React, and Tailwind CSS that provides an interactive shopping assistant for e-commerce stores.

## Features

- 🎯 **Floating Widget**: Appears as a floating chat button on the bottom-right of the screen
- 💬 **Interactive Chat**: Full chat window with smooth animations
- 🤖 **AI Assistant**: Intelligent responses with product recommendations
- 📱 **Mobile Responsive**: Optimized for all device sizes
- 🎨 **Modern UI**: Beautiful design with Tailwind CSS
- ⚡ **Real-time**: Typing indicators and loading states
- 🛍️ **Product Cards**: Rich product recommendations with images and buy buttons
- ♿ **Accessible**: Built with accessibility in mind

## Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **React 18** - UI library with hooks
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Beautiful icons

### Backend
- **Node.js** - JavaScript runtime
- **Express.js** - Web framework
- **CORS** - Cross-origin resource sharing

## Project Structure

```
AI Voice Assistance/
├── frontend/                 # Next.js frontend application
│   ├── app/                 # App Router pages
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home page
│   │   └── globals.css      # Global styles
│   ├── components/          # React components
│   │   ├── ChatbotWidget.tsx    # Main chatbot component
│   │   ├── ChatMessage.tsx      # Individual message component
│   │   └── ProductCard.tsx      # Product recommendation card
│   ├── types/               # TypeScript type definitions
│   │   └── chat.ts          # Chat and product types
│   └── package.json         # Frontend dependencies
├── backend/                 # Express.js API server
│   ├── server.js            # Main server file
│   └── package.json         # Backend dependencies
└── README.md               # This file
```

## Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn

### 1. Clone and Setup

```bash
# Navigate to the project directory
cd "AI Voice Assistance"

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
npm install
```

### 2. Start the Backend Server

```bash
# From the backend directory
cd backend
npm run dev
```

The backend server will start on `http://localhost:3001`

### 3. Start the Frontend Development Server

```bash
# From the frontend directory (in a new terminal)
cd frontend
npm run dev
```

The frontend will start on `http://localhost:3000`

### 4. Open Your Browser

Visit `http://localhost:3000` to see the chatbot in action!

## Usage

### Chatbot Features

1. **Floating Button**: Click the chat icon in the bottom-right corner
2. **Welcome Message**: The bot greets you with "Hi there! Looking for something special today?"
3. **Product Recommendations**: Ask about:
   - "phones" or "smartphones"
   - "laptops" or "computers" 
   - "headphones" or "earphones"
4. **Interactive Responses**: The bot provides relevant product recommendations with images and prices
5. **Buy Now Buttons**: Click to simulate adding products to cart

### API Endpoints

The backend provides these endpoints:

- `GET /api/health` - Health check
- `POST /api/chat` - Send chat messages
- `GET /api/products` - Get product listings

## Customization

### Adding New Product Categories

1. Update the `products` object in `backend/server.js`
2. Add new condition in the `generateBotResponse` function
3. Update the frontend response handling if needed

### Styling

The chatbot uses Tailwind CSS classes. You can customize:
- Colors in `tailwind.config.js`
- Animations in the config file
- Component styles in individual component files

### Integration with Real APIs

To integrate with OpenAI or other AI services:

1. Replace the mock response logic in `backend/server.js`
2. Add your API keys to environment variables
3. Update the frontend to handle the new response format

## Development

### Available Scripts

**Frontend:**
```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint
```

**Backend:**
```bash
npm run dev      # Start with nodemon
npm start        # Start production server
```

### Environment Variables

Create a `.env` file in the backend directory:

```env
PORT=3001
NODE_ENV=development
```

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - feel free to use this project for your own applications!

## Support

If you have any questions or need help, please open an issue on GitHub. 