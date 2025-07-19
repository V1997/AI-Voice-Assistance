'use client'

import React, { useState, useRef, useEffect } from 'react'
import { MessageCircle, X, Send, ShoppingBag } from 'lucide-react'
import ChatMessage from './ChatMessage'
import ProductCard from './ProductCard'
import { Message, Product } from '@/types/chat'

const ChatbotWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'bot',
      content: 'Hi there! Looking for something special today?',
      timestamp: new Date(),
    },
  ])
  const [inputValue, setInputValue] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isOpen])

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputValue,
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsTyping(true)

    // Simulate API call
    setTimeout(() => {
      const botResponse = generateBotResponse(inputValue)
      setMessages(prev => [...prev, botResponse])
      setIsTyping(false)
    }, 1000 + Math.random() * 2000) // Random delay between 1-3 seconds
  }

  const generateBotResponse = (userInput: string): Message => {
    const input = userInput.toLowerCase()
    
    // Product recommendations based on user input
    if (input.includes('phone') || input.includes('smartphone')) {
      return {
        id: Date.now().toString(),
        type: 'bot',
        content: 'I found some great smartphones for you!',
        timestamp: new Date(),
        products: [
          {
            id: '1',
            name: 'iPhone 15 Pro',
            price: 999,
            image: 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=300&h=300&fit=crop',
            description: 'Latest iPhone with advanced camera system',
          },
          {
            id: '2',
            name: 'Samsung Galaxy S24',
            price: 899,
            image: 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop',
            description: 'Premium Android experience',
          },
        ],
      }
    }

    if (input.includes('laptop') || input.includes('computer')) {
      return {
        id: Date.now().toString(),
        type: 'bot',
        content: 'Here are some excellent laptops!',
        timestamp: new Date(),
        products: [
          {
            id: '3',
            name: 'MacBook Pro 14"',
            price: 1999,
            image: 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300&h=300&fit=crop',
            description: 'Powerful laptop for professionals',
          },
          {
            id: '4',
            name: 'Dell XPS 13',
            price: 1299,
            image: 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=300&h=300&fit=crop',
            description: 'Ultra-thin and lightweight',
          },
        ],
      }
    }

    if (input.includes('headphone') || input.includes('earphone')) {
      return {
        id: Date.now().toString(),
        type: 'bot',
        content: 'Check out these amazing audio devices!',
        timestamp: new Date(),
        products: [
          {
            id: '5',
            name: 'Sony WH-1000XM5',
            price: 349,
            image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=300&fit=crop',
            description: 'Industry-leading noise cancellation',
          },
          {
            id: '6',
            name: 'AirPods Pro',
            price: 249,
            image: 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=300&h=300&fit=crop',
            description: 'Seamless Apple ecosystem integration',
          },
        ],
      }
    }

    // Default responses
    const defaultResponses = [
      "I'd be happy to help you find what you're looking for! Could you tell me more about what you need?",
      "Great question! Let me help you discover some amazing products. What category interests you?",
      "I'm here to make your shopping experience better! What can I help you find today?",
      "Thanks for reaching out! I can help you with product recommendations, pricing, or any questions you might have.",
    ]

    return {
      id: Date.now().toString(),
      type: 'bot',
      content: defaultResponses[Math.floor(Math.random() * defaultResponses.length)],
      timestamp: new Date(),
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <>
      {/* Floating Chat Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-primary-600 hover:bg-primary-700 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-300 z-50 flex items-center justify-center group"
        aria-label="Open chat"
      >
        <MessageCircle className="w-6 h-6" />
        <div className="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white text-xs rounded-full flex items-center justify-center animate-bounce">
          1
        </div>
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 w-96 h-[500px] bg-white rounded-lg shadow-2xl border border-gray-200 z-50 animate-bounce-in">
          {/* Header */}
          <div className="bg-primary-600 text-white p-4 rounded-t-lg flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                <ShoppingBag className="w-4 h-4" />
              </div>
              <div>
                <h3 className="font-semibold">Store Assistant</h3>
                <p className="text-xs text-primary-100">Online now</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:text-gray-200 transition-colors"
              aria-label="Close chat"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Messages */}
          <div className="h-80 overflow-y-auto p-4 chat-scrollbar">
            <div className="space-y-4">
              {messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))}
              {isTyping && (
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-typing"></div>
                  </div>
                  <div className="bg-gray-100 rounded-lg px-3 py-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-typing"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-typing" style={{ animationDelay: '0.2s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-typing" style={{ animationDelay: '0.4s' }}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 border-t border-gray-200">
            <div className="flex space-x-2">
              <input
                ref={inputRef}
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-gray-900 placeholder-gray-500 bg-white"
                disabled={isTyping}
              />
              <button
                onClick={handleSendMessage}
                disabled={!inputValue.trim() || isTyping}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                aria-label="Send message"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

export default ChatbotWidget 