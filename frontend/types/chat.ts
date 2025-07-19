export interface Product {
  id: string
  name: string
  price: number
  image: string
  description: string
}

export interface Message {
  id: string
  type: 'user' | 'bot'
  content: string
  timestamp: Date
  products?: Product[]
} 