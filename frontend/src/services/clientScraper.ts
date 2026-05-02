/**
 * Client-side scraper that runs in the user's browser
 * This avoids server-side scraping and bot detection issues
 */

export interface ScrapedProduct {
  platform: string;
  product_name: string;
  current_price: number;
  currency: string;
  product_url: string;
  image_url: string | null;
  availability: boolean;
}

export interface ScrapeResult {
  query: string;
  total_results: number;
  page: number;
  results: ScrapedProduct[];
  search_time_seconds: number;
}

/**
 * Scrape Lazada products using an iframe in the user's browser
 */
export async function scrapeLazada(
  query: string,
  page: number = 1,
  maxResults: number = 40,
  sortBy: string = 'best_match'
): Promise<ScrapeResult> {
  const startTime = Date.now();
  
  try {
    // Build Lazada search URL
    const sortMap: Record<string, string> = {
      'price_asc': 'priceasc',
      'price_desc': 'pricedesc'
    };
    
    const params = new URLSearchParams({
      q: query,
      page: page.toString()
    });
    
    if (sortBy in sortMap) {
      params.append('sortBy', sortMap[sortBy]);
    }
    
    // Use proxy endpoint to avoid CORS issues
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const proxyUrl = `${API_URL}/api/proxy/lazada?${params.toString()}`;
    
    // Fetch the page HTML via proxy
    const response = await fetch(proxyUrl, {
      method: 'GET',
      headers: {
        'Accept': 'text/html',
      },
    });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch: ${response.status}`);
    }
    
    const html = await response.text();
    
    // Parse HTML using DOMParser
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    
    // Extract total count
    const bodyText = doc.body.textContent || '';
    const totalMatch = bodyText.match(/(\d+)\s+items?\s+found/i);
    const totalResults = totalMatch ? parseInt(totalMatch[1]) : 0;
    
    // Extract products
    const products: ScrapedProduct[] = [];
    const productCards = doc.querySelectorAll('[data-tracking="product-card"]');
    
    productCards.forEach((card, index) => {
      if (index >= maxResults) return;
      
      try {
        // Extract product URL
        const link = card.querySelector('a[href]') as HTMLAnchorElement;
        if (!link) return;
        
        let productUrl = link.href;
        if (productUrl.startsWith('//')) {
          productUrl = 'https:' + productUrl;
        } else if (productUrl.startsWith('/')) {
          productUrl = 'https://www.lazada.com.ph' + productUrl;
        }
        
        // Extract product name
        const titleElem = card.querySelector('a[title]');
        let productName = titleElem?.getAttribute('title') || '';
        
        if (!productName) {
          const cardHtml = card.innerHTML;
          const titleMatch = cardHtml.match(/title="([^"]+)"/);
          if (titleMatch) {
            productName = titleMatch[1].replace(/&quot;/g, '"').replace(/&amp;/g, '&');
          }
        }
        
        if (!productName || productName.length < 5) return;
        
        // Extract price
        const priceElem = card.querySelector('[class*="ooOxS"], .price, [class*="price"]');
        const priceText = priceElem?.textContent || '';
        
        let price: number | null = null;
        if (priceText && priceText.includes('₱')) {
          const priceMatch = priceText.replace(/[₱,]/g, '').match(/[\d.]+/);
          if (priceMatch) {
            price = parseFloat(priceMatch[0]);
          }
        }
        
        if (price === null) return;
        
        // Extract image URL
        let imageUrl: string | null = null;
        const imgs = card.querySelectorAll('img');
        
        for (const img of imgs) {
          for (const attr of ['src', 'data-src', 'data-lazy-src']) {
            const url = img.getAttribute(attr);
            if (url && url.includes('lazcdn.com') && !url.startsWith('data:')) {
              imageUrl = url.split('?')[0];
              break;
            }
          }
          if (imageUrl) break;
        }
        
        products.push({
          platform: 'lazada',
          product_name: productName,
          current_price: price,
          currency: 'PHP',
          product_url: productUrl,
          image_url: imageUrl,
          availability: true
        });
      } catch (error) {
        console.warn('Failed to parse product card:', error);
      }
    });
    
    const searchTime = (Date.now() - startTime) / 1000;
    
    return {
      query,
      total_results: totalResults,
      page,
      results: products,
      search_time_seconds: parseFloat(searchTime.toFixed(2))
    };
    
  } catch (error) {
    console.error('Scraping error:', error);
    throw new Error(`Failed to scrape Lazada: ${error}`);
  }
}
