/**
 * Mock data for demonstration purposes
 * Used when real scraping is blocked by bot detection
 */

import { ScrapedProduct } from './clientScraper';

const MOCK_PRODUCTS: Record<string, ScrapedProduct[]> = {
  phone: [
    {
      platform: 'lazada',
      product_name: 'Samsung Galaxy A54 5G 8GB+256GB | 50MP OIS Camera | 5000mAh Battery | Exynos 1380',
      current_price: 19990,
      currency: 'PHP',
      product_url: 'https://www.lazada.com.ph/products/samsung-galaxy-a54-5g',
      image_url: 'https://img.lazcdn.com/g/p/0e8c8f5e5c5e5e5e5e5e5e5e5e5e5e5e.jpg',
      availability: true
    },
    {
      platform: 'lazada',
      product_name: 'Xiaomi Redmi Note 13 Pro 8GB+256GB | 200MP Camera | 67W Fast Charging',
      current_price: 14999,
      currency: 'PHP',
      product_url: 'https://www.lazada.com.ph/products/xiaomi-redmi-note-13-pro',
      image_url: 'https://img.lazcdn.com/g/p/1f9d9e6f6d6e6e6e6e6e6e6e6e6e6e6e.jpg',
      availability: true
    },
    {
      platform: 'lazada',
      product_name: 'iPhone 15 Pro Max 256GB | A17 Pro Chip | Titanium Design',
      current_price: 74990,
      currency: 'PHP',
      product_url: 'https://www.lazada.com.ph/products/iphone-15-pro-max',
      image_url: 'https://img.lazcdn.com/g/p/2g0e0f7g7e7f7f7f7f7f7f7f7f7f7f7f.jpg',
      availability: true
    },
  ],
  laptop: [
    {
      platform: 'lazada',
      product_name: 'ASUS VivoBook 15 Intel Core i5-1235U 8GB RAM 512GB SSD 15.6" FHD',
      current_price: 32995,
      currency: 'PHP',
      product_url: 'https://www.lazada.com.ph/products/asus-vivobook-15',
      image_url: 'https://img.lazcdn.com/g/p/3h1f1g8h8f8g8g8g8g8g8g8g8g8g8g8g.jpg',
      availability: true
    },
    {
      platform: 'lazada',
      product_name: 'Lenovo IdeaPad 3 AMD Ryzen 5 5500U 8GB 256GB SSD 14" FHD',
      current_price: 24999,
      currency: 'PHP',
      product_url: 'https://www.lazada.com.ph/products/lenovo-ideapad-3',
      image_url: 'https://img.lazcdn.com/g/p/4i2g2h9i9g9h9h9h9h9h9h9h9h9h9h9h.jpg',
      availability: true
    },
  ],
  default: [
    {
      platform: 'lazada',
      product_name: 'Product Search Demo - Real scraping blocked by Lazada',
      current_price: 999,
      currency: 'PHP',
      product_url: 'https://www.lazada.com.ph',
      image_url: null,
      availability: true
    },
  ]
};

export function getMockProducts(query: string, maxResults: number = 40): ScrapedProduct[] {
  const lowerQuery = query.toLowerCase();
  
  // Find matching category
  for (const [key, products] of Object.entries(MOCK_PRODUCTS)) {
    if (lowerQuery.includes(key)) {
      return products.slice(0, maxResults);
    }
  }
  
  // Return default
  return MOCK_PRODUCTS.default.slice(0, maxResults);
}
