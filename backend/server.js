const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Mock product database
const products = {
  phones: [
    {
      id: '1',
      name: 'iPhone 15 Pro',
      price: 999,
      image: 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=300&h=300&fit=crop',
      description: 'Latest iPhone with advanced camera system',
      category: 'phones'
    },
    {
      id: '2',
      name: 'Samsung Galaxy S24',
      price: 899,
      image: 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop',
      description: 'Premium Android experience',
      category: 'phones'
    }
  ],
  laptops: [
    {
      id: '3',
      name: 'MacBook Pro 14"',
      price: 1999,
      image: 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300&h=300&fit=crop',
      description: 'Powerful laptop for professionals',
      category: 'laptops'
    },
    {
      id: '4',
      name: 'Dell XPS 13',
      price: 1299,
      image: 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=300&h=300&fit=crop',
      description: 'Ultra-thin and lightweight',
      category: 'laptops'
    }
  ],
  headphones: [
    {
      id: '5',
      name: 'Sony WH-1000XM5',
      price: 349,
      image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=300&fit=crop',
      description: 'Industry-leading noise cancellation',
      category: 'headphones'
    },
    {
      id: '6',
      name: 'AirPods Pro',
      price: 249,
      image: 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=300&h=300&fit=crop',
      description: 'Seamless Apple ecosystem integration',
      category: 'headphones'
    }
  ]
};

// Chatbot response logic
function generateBotResponse(userInput) {
  const input = userInput.toLowerCase();
  
  // Product recommendations based on user input
  if (input.includes('phone') || input.includes('smartphone')) {
    return {
      content: 'I found some great smartphones for you!',
      products: products.phones
    };
  }

  if (input.includes('laptop') || input.includes('computer')) {
    return {
      content: 'Here are some excellent laptops!',
      products: products.laptops
    };
  }

  if (input.includes('headphone') || input.includes('earphone')) {
    return {
      content: 'Check out these amazing audio devices!',
      products: products.headphones
    };
  }

  // Default responses
  const defaultResponses = [
    "I'd be happy to help you find what you're looking for! Could you tell me more about what you need?",
    "Great question! Let me help you discover some amazing products. What category interests you?",
    "I'm here to make your shopping experience better! What can I help you find today?",
    "Thanks for reaching out! I can help you with product recommendations, pricing, or any questions you might have.",
  ];

  return {
    content: defaultResponses[Math.floor(Math.random() * defaultResponses.length)],
    products: []
  };
}

// API Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Chatbot API is running' });
});

app.post('/api/chat', (req, res) => {
  try {
    const { message } = req.body;
    
    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // Simulate processing delay
    setTimeout(() => {
      const response = generateBotResponse(message);
      res.json({
        success: true,
        response: {
          id: Date.now().toString(),
          type: 'bot',
          content: response.content,
          timestamp: new Date(),
          products: response.products
        }
      });
    }, 1000 + Math.random() * 2000); // Random delay between 1-3 seconds

  } catch (error) {
    console.error('Chat API error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/api/products', (req, res) => {
  try {
    const { category } = req.query;
    
    if (category && products[category]) {
      res.json({ products: products[category] });
    } else {
      // Return all products if no category specified
      const allProducts = Object.values(products).flat();
      res.json({ products: allProducts });
    }
  } catch (error) {
    console.error('Products API error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Chatbot API server running on port ${PORT}`);
  console.log(`📡 Health check: http://localhost:${PORT}/api/health`);
  console.log(`💬 Chat endpoint: http://localhost:${PORT}/api/chat`);
  console.log(`🛍️ Products endpoint: http://localhost:${PORT}/api/products`);
}); 