import React from 'react'
import { Product } from '@/types/chat'

interface ProductCardProps {
  product: Product
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const handleBuyNow = () => {
    // In a real app, this would redirect to the product page or add to cart
    alert(`Added ${product.name} to cart!`)
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-3 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex space-x-3">
        <div className="flex-shrink-0">
          <img
            src={product.image}
            alt={product.name}
            className="w-16 h-16 object-cover rounded-md"
            loading="lazy"
          />
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-medium text-gray-900 truncate">
            {product.name}
          </h4>
          <p className="text-xs text-gray-500 mt-1 line-clamp-2">
            {product.description}
          </p>
          <div className="flex items-center justify-between mt-2">
            <span className="text-sm font-semibold text-primary-600">
              ${product.price}
            </span>
            <button
              onClick={handleBuyNow}
              className="px-3 py-1 text-xs bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-1"
            >
              Buy Now
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProductCard 