# Requirements Document

## Introduction

The E-commerce Price Tracker is a web-based system that enables users to monitor product prices across multiple e-commerce platforms (Lazada, Shopee, and TikTok Shop). The system automatically tracks price changes for saved products and notifies users via email when prices drop below their specified thresholds.

## Glossary

- **Price_Tracker_System**: The complete web application including search, tracking, and notification components
- **Product_Search_Engine**: Component responsible for querying e-commerce platforms and retrieving product information
- **Price_Monitor**: Component that periodically checks saved products for price changes
- **Notification_Service**: Component that sends email alerts to users
- **User**: A person who uses the system to track product prices
- **Tracked_Product**: A product that a user has saved for price monitoring
- **Price_Threshold**: The maximum price at which a user wants to be notified about a product
- **E-commerce_Platform**: External shopping websites (Lazada, Shopee, TikTok Shop)
- **Price_Drop**: An event where a product's current price falls below the user's specified threshold

## Requirements

### Requirement 1: Multi-Platform Product Search

**User Story:** As a user, I want to search for products across multiple e-commerce platforms simultaneously, so that I can compare prices and find the best deals without visiting each platform separately.

#### Acceptance Criteria

1. WHEN a user submits a search query, THE Product_Search_Engine SHALL retrieve product results from Lazada
2. WHEN a user submits a search query, THE Product_Search_Engine SHALL retrieve product results from Shopee
3. WHEN a user submits a search query, THE Product_Search_Engine SHALL retrieve product results from TikTok Shop
4. THE Product_Search_Engine SHALL return results within 10 seconds of receiving a search query
5. FOR ALL search results, THE Product_Search_Engine SHALL include product name, current price, platform name, and product URL
6. WHEN a search query returns no results from any platform, THE Price_Tracker_System SHALL display a message indicating no products were found

### Requirement 2: Product Tracking Management

**User Story:** As a user, I want to save products I'm interested in with a target price, so that I can monitor them for price drops without manually checking each day.

#### Acceptance Criteria

1. WHEN a user selects a product from search results, THE Price_Tracker_System SHALL allow the user to save the product for tracking
2. WHEN saving a product, THE Price_Tracker_System SHALL require the user to specify a price threshold
3. THE Price_Tracker_System SHALL store the product name, current price, platform, product URL, and price threshold for each tracked product
4. WHEN a user views their tracked products, THE Price_Tracker_System SHALL display all saved products with their current prices and thresholds
5. WHEN a user requests to remove a tracked product, THE Price_Tracker_System SHALL delete the product from their tracking list
6. THE Price_Tracker_System SHALL associate each tracked product with the user who saved it

### Requirement 3: Automatic Price Monitoring

**User Story:** As a user, I want the system to automatically check prices of my tracked products, so that I don't miss price drops while I'm away from the website.

#### Acceptance Criteria

1. THE Price_Monitor SHALL check the current price of each tracked product at least once every 24 hours
2. WHEN checking a tracked product, THE Price_Monitor SHALL retrieve the current price from the product's e-commerce platform
3. WHEN a price check completes, THE Price_Monitor SHALL update the stored current price for the tracked product
4. IF a price cannot be retrieved from an e-commerce platform, THEN THE Price_Monitor SHALL log the error and retry on the next scheduled check
5. THE Price_Monitor SHALL maintain a price history for each tracked product showing price changes over time

### Requirement 4: Price Drop Notifications

**User Story:** As a user, I want to receive email notifications when tracked product prices drop below my threshold, so that I can purchase products at my desired price point.

#### Acceptance Criteria

1. WHEN a tracked product's current price falls below the user's price threshold, THE Notification_Service SHALL send an email to the user
2. THE Notification_Service SHALL include the product name, old price, new price, price threshold, and product URL in the email
3. THE Notification_Service SHALL send the email within 1 hour of detecting the price drop
4. WHEN multiple tracked products drop below their thresholds simultaneously, THE Notification_Service SHALL send a single consolidated email listing all price drops
5. THE Notification_Service SHALL send at most one notification per tracked product per price drop event
6. WHEN a product price rises above the threshold and then drops below it again, THE Notification_Service SHALL send a new notification

### Requirement 5: User Authentication and Data Isolation

**User Story:** As a user, I want to create an account and log in, so that my tracked products and preferences are private and accessible only to me.

#### Acceptance Criteria

1. THE Price_Tracker_System SHALL allow users to create an account with an email address and password
2. WHEN a user creates an account, THE Price_Tracker_System SHALL validate that the email address is in a valid format
3. WHEN a user creates an account, THE Price_Tracker_System SHALL require a password with at least 8 characters
4. THE Price_Tracker_System SHALL allow users to log in using their email address and password
5. WHEN a user logs in with correct credentials, THE Price_Tracker_System SHALL grant access to their tracked products
6. WHEN a user logs in with incorrect credentials, THE Price_Tracker_System SHALL deny access and display an error message
7. THE Price_Tracker_System SHALL ensure that each user can only view and manage their own tracked products

### Requirement 6: Search Result Accuracy and Data Quality

**User Story:** As a user, I want search results to accurately reflect current product information, so that I can make informed decisions about which products to track.

#### Acceptance Criteria

1. FOR ALL search results, THE Product_Search_Engine SHALL retrieve the most current price available from each e-commerce platform
2. WHEN a product is unavailable or out of stock, THE Product_Search_Engine SHALL exclude it from search results
3. THE Product_Search_Engine SHALL handle special characters and non-English text in search queries
4. WHEN an e-commerce platform returns an error, THE Product_Search_Engine SHALL continue searching other platforms and log the error
5. THE Product_Search_Engine SHALL return at least 10 results per platform when available

### Requirement 7: Email Notification Configuration

**User Story:** As a user, I want to configure my email notification preferences, so that I receive alerts in a way that suits my needs.

#### Acceptance Criteria

1. THE Price_Tracker_System SHALL allow users to update their notification email address
2. WHEN a user updates their email address, THE Price_Tracker_System SHALL validate that the new email is in a valid format
3. THE Price_Tracker_System SHALL use the user's current email address for all price drop notifications
4. WHEN a user's email address is invalid or bounces, THE Notification_Service SHALL log the delivery failure

### Requirement 8: Price Threshold Modification

**User Story:** As a user, I want to update the price threshold for my tracked products, so that I can adjust my target price as market conditions change.

#### Acceptance Criteria

1. WHEN a user views a tracked product, THE Price_Tracker_System SHALL allow the user to modify the price threshold
2. WHEN a user updates a price threshold, THE Price_Tracker_System SHALL validate that the threshold is a positive number
3. WHEN a price threshold is updated, THE Price_Monitor SHALL use the new threshold for future price drop detection
4. WHEN a product's current price is already below a newly set threshold, THE Notification_Service SHALL send an immediate notification

### Requirement 9: Platform Connection Resilience

**User Story:** As a user, I want the system to handle e-commerce platform outages gracefully, so that temporary issues don't prevent me from tracking products or receiving notifications.

#### Acceptance Criteria

1. IF an e-commerce platform is unreachable during a search, THEN THE Product_Search_Engine SHALL return results from available platforms and display a warning about the unavailable platform
2. IF an e-commerce platform is unreachable during price monitoring, THEN THE Price_Monitor SHALL retry the price check up to 3 times with exponential backoff
3. IF all retry attempts fail, THEN THE Price_Monitor SHALL skip that product for the current monitoring cycle and attempt again in the next cycle
4. THE Price_Tracker_System SHALL log all platform connection failures with timestamps for debugging

### Requirement 10: Data Persistence and Reliability

**User Story:** As a user, I want my tracked products and price history to be reliably stored, so that I don't lose my tracking data due to system issues.

#### Acceptance Criteria

1. THE Price_Tracker_System SHALL persist all user accounts, tracked products, and price history to a database
2. WHEN a user saves a tracked product, THE Price_Tracker_System SHALL confirm successful storage before displaying a success message
3. IF a database write operation fails, THEN THE Price_Tracker_System SHALL display an error message to the user and log the failure
4. THE Price_Tracker_System SHALL maintain data integrity such that each tracked product references a valid user account
5. THE Price_Tracker_System SHALL maintain data integrity such that price history entries reference valid tracked products
